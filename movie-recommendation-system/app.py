from flask import Flask, render_template, jsonify, request
from recommedation_sys import RecommendationSys
import pandas as pd
import asyncio
import aiohttp
import pickle
from reviews import Reviews
from random import randint

df = pd.read_csv("datasets/main_df.csv")

with open("models/cosine_sim.pkl", "rb") as file:
    cosine_sim = pickle.load(file)

with open("models/cosine_sim_prod.pkl", "rb") as file:
    cosine_sim_prod_com = pickle.load(file)

cosine_sims = [cosine_sim, cosine_sim_prod_com]

api_key = "" 

sys = RecommendationSys(df, api_key, cosine_sims)
reviews = Reviews()

app = Flask(__name__, template_folder="templates",static_folder="static")

global rec

async def get_movies_posters(movies_ids):
    async with aiohttp.ClientSession() as session:
        posters = await sys.get_recommended_movies_posters(session, movies_ids)
    return posters

async def get_movie_details(query):
    global rec
    query = " ".join(str(query).split("_"))
    try:
        rec = await sys.get_content_based_recommended_details(query)
        prod_company_rec = await sys.get_prod_company_based_recommended_details(query)
        movie_details = {
            "title": rec["title"],
            "overview": rec["overview"],
            "rating": rec["rating"],
            "genre": rec["genres"],
            "release_date": rec["release_date"],
            "runtime": rec["runtime"],
            "status": rec["status"],
            "poster": rec["poster"],
        }

        top_cast = [
            {"id": int(cast_id), "name": name, "role": role, "image": image}
            for cast_id, name, role, image in zip(
                rec["casts_ids"],
                rec["casts_names"],
                rec["casts_chars"],
                rec["casts_profiles"],
            )
        ]

        top_recommended_movies = [
            {"title": title, "image": image}
            for title, image in zip(rec["rec_movies"], rec["rec_posters"])
        ]
        
        prod_company_rec_movies = [
            {"title": title, "image": image}
            for title, image in zip(prod_company_rec["rec_movies"], prod_company_rec["rec_posters"])
        ]

        rev = reviews.get_reviews(rec["imdb_id"])
        comments_and_reviews = [
            {"comment": comment, "review": review}
            for comment, review in zip(rev[0], rev[1])
        ]
        
        return rec, movie_details, top_cast, top_recommended_movies, prod_company_rec_movies, comments_and_reviews
    
    except Exception as e:
        print(f"Error fetching movie details: {e}")
        return None, None, None, None, None, None

@app.route("/")
def index():
    try:
        random_numbers = [randint(0, len(df)) for _ in range(16)]
        idxs = df[df.index.isin(random_numbers)]
        movie_ids = list(idxs["id"])
        movie_names = list(idxs["original_title"])
        posters = asyncio.run(get_movies_posters(movie_ids))
        movies = [
            {"title": title, "image": image} for title, image in zip(movie_names, posters)
        ]

        return render_template(
            "index.html",
            top_recommended_movies=movies,
        )
    except Exception as e:
        print(f"Error loading index page: {e}")
        return render_template("error.html", error_message="An error occurred while loading recommendations.")

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "")
    rec, movie_details, top_cast, top_recommended_movies, prod_company_rec_movies, comments_and_reviews = asyncio.run(get_movie_details(query))

    if not movie_details:
        return render_template("error.html", error_message="Movie not found in our database.")

    return render_template(
        "recommend.html",
        movie_details=movie_details,
        top_cast=top_cast,
        top_recommended_movies=top_recommended_movies,
        prod_company_rec_movies=prod_company_rec_movies,
        comments_and_reviews=comments_and_reviews,
    )


@app.route("/movie/<title>", methods=["GET"])
def movie_details(title):
    rec, movie_details, top_cast, top_recommended_movies, prod_company_rec_movies, comments_and_reviews = asyncio.run(get_movie_details(title))

    if not movie_details:
        return render_template("error.html", error_message="Movie not found in our database.")

    return render_template(
        "recommend.html",
        movie_details=movie_details,
        top_cast=top_cast,
        top_recommended_movies=top_recommended_movies,
        prod_company_rec_movies=prod_company_rec_movies,
        comments_and_reviews=comments_and_reviews,
    )


@app.route("/api/cast/<int:cast_id>", methods=["GET"])
def get_cast_details(cast_id):
    try:
        casts_ids = rec["casts_ids"]
        casts_names = rec["casts_names"]
        casts_chars = rec["casts_chars"]
        casts_birthdays = rec["casts_birthdays"]
        casts_biographys = rec["casts_biographys"]
        casts_place_of_births = rec["casts_place_of_births"]
        casts_genders = rec["casts_genders"]

        cast_details = {
            int(cid): {
                "name": name,
                "role": role,
                "gender": gender,
                "bday": bday,
                "place": place,
                "bio": bio,
            }
            for cid, name, role, gender, bday, place, bio in zip(
                casts_ids,
                casts_names,
                casts_chars,
                casts_genders,
                casts_birthdays,
                casts_place_of_births,
                casts_biographys,
            )
        }

        cast = cast_details.get(cast_id, {})
        return jsonify(cast)
    except Exception as e:
        print(f"Error fetching cast details: {e}")
        return jsonify({}), 500

@app.route("/api/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query", "")
    if not query:
        return jsonify([])

    matching_movies = df[df["original_title"].str.contains(query, case=False, na=False)]
    suggestions = [{"title": title} for title in matching_movies["original_title"].head(10)]
    return jsonify(suggestions)

if __name__ == "__main__":
    app.run(debug=True)
