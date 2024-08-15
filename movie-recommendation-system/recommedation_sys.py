from fastapi import HTTPException
from pydantic import BaseModel
import aiohttp
import asyncio
import pandas as pd
import pickle
import time
from typing import List, Dict
from cachetools import TTLCache


# Cache for movie data and actor details (TTL cache with a time-to-live of 10 minutes)
cache = TTLCache(maxsize=100, ttl=600)

class RecommendationSys:
    def __init__(self, df: pd.DataFrame, api_key: str, cosine_sims: list):
        self.df = df
        self.api_key = api_key
        self.content_based_cosine_sim = cosine_sims[0]
        self.prod_company_cosine_sim = cosine_sims[1]
        self.df_indexed = df.set_index("original_title")
        self.api_base_url = "https://api.themoviedb.org/3"

    def check_movie(self, title: str):
        return title in self.df_indexed.index

    def content_based_recommendation(self, title: str):
        idx = self.df_indexed.index.get_loc(title)
        scores = pd.Series(self.content_based_cosine_sim[idx]).sort_values(ascending=False)
        top_indices = scores.iloc[0:13].index

        recommended_movies = self.df.loc[top_indices, "original_title"].tolist()
        recommended_movies_ids = self.df.loc[top_indices, "id"].tolist()

        return recommended_movies_ids[0], recommended_movies[1:], recommended_movies_ids[1:]
    
    def prod_company_based_recommendation(self, title: str):
        idx = self.df_indexed.index.get_loc(title)
        scores = pd.Series(self.prod_company_cosine_sim[idx]).sort_values(ascending=False)
        top_indices = scores.iloc[0:50].index
        # print(f"a : {top_indices.max()}, b :{self.df.index.max()}")
        valid_indices = [idx for idx in top_indices if 0 <= idx < len(self.df)]
        movies = self.df.iloc[valid_indices].copy()
        movies = movies.sort_values('weighted_rating', ascending=False)
        movies = movies[movies["original_title"] != title]
        movies = movies[movies["weighted_rating"] > 5.8]
        random_movie = movies.sample(n=12)
        recommended_movies = self.df.loc[random_movie.index, "original_title"].tolist()
        recommended_movies_ids = self.df.loc[random_movie.index, "id"].tolist()
        
        return recommended_movies, recommended_movies_ids
        
    
    async def get_content_based_recommended_details(self, movie_title: str):
        if not self.check_movie(movie_title):
            raise HTTPException(status_code=404, detail="Movie not found in our database")

        movie_id, recommended_movies, recommended_movies_ids = self.content_based_recommendation(movie_title)
        return await self.get_recommended_details(movie_title,movie_id, recommended_movies, recommended_movies_ids)
    
    async def get_prod_company_based_recommended_details(self, movie_title: str):
        if not self.check_movie(movie_title):
            raise HTTPException(status_code=404, detail="Movie not found in our database")

        recommended_movies, recommended_movies_ids = self.prod_company_based_recommendation(movie_title)
        
        async with aiohttp.ClientSession() as session:
            rec_posters = await self.get_recommended_movies_posters(session, recommended_movies_ids)
            
        return {
            "rec_movies": recommended_movies,
            "rec_posters": rec_posters,
        }
        
    async def get_recommended_details(self,movie_title, movie_id, recommended_movies, recommended_movies_ids):
        async with aiohttp.ClientSession() as session:
            # Check if movie data is in cache
            movie_data = cache.get(movie_id)
            if not movie_data:
                movie_data = await self._fetch_movie_data(session, movie_id)
                if movie_data:
                    cache[movie_id] = movie_data

            if not movie_data:
                raise HTTPException(status_code=404, detail="Movie data not found")

            casts = await self.top_casts(session, movie_id)
            rec_posters = await self.get_recommended_movies_posters(session, recommended_movies_ids)

        # total_time = time.time() - start_time
        # print(f"Total time to get recommended details: {total_time:.2f} seconds")

        return {
            "title": movie_title,
            "poster": movie_data["poster"],
            "imdb_id": movie_data["imdb_id"],
            "genres": movie_data["genres"],
            "overview": movie_data["overview"],
            "rating": movie_data["rating"],
            "vote_count": movie_data["vote_count"],
            "release_date": movie_data["release_date"],
            "runtime": movie_data["runtime"],
            "status": movie_data["status"],
            "casts_ids": casts["casts_ids"],
            "casts_names": casts["casts_names"],
            "casts_chars": casts["casts_chars"],
            "casts_profiles": casts["casts_profiles"],
            "casts_biographys": casts["casts_biographys"],
            "casts_birthdays": casts["casts_birthdays"],
            "casts_place_of_births": casts["casts_place_of_births"],
            "casts_genders": casts["casts_genders"],
            "rec_movies": recommended_movies,
            "rec_posters": rec_posters,
        }

    async def _fetch_movie_data(self, session, movie_id: int):
        url = f"{self.api_base_url}/movie/{movie_id}"
        params = {"api_key": self.api_key}

        async with session.get(url, params=params) as response:
            if response.status != 200:
                print(f"Error: {response.status}")
                return None

            data = await response.json()
            runtime = (
                f"{data['runtime']//60} hour(s) {data['runtime']%60} min(s)"
                if data["runtime"] % 60 != 0
                else f"{data['runtime']//60} hour(s)"
            )
                
            return {
                "poster": f"https://image.tmdb.org/t/p/original{data['poster_path']}",
                "imdb_id": data.get("imdb_id", "N/A"),
                "genres": ",".join([genre["name"] for genre in data["genres"]]),
                "overview": data["overview"],
                "rating": data["vote_average"],
                "vote_count": data["vote_count"],
                "release_date": data["release_date"],
                "runtime": runtime,
                "status": data["status"],
            }

    async def top_casts(self, session, movie_id: int):
        url = f"{self.api_base_url}/movie/{movie_id}/credits"
        params = {"api_key": self.api_key}

        async with session.get(url, params=params) as response:
            if response.status != 200:
                print(f"Error: {response.status}")
                return {}

            data = await response.json()
            top_casts = sorted(data["cast"], key=lambda x: x["order"])[:8]

            casts_ids = [cast["id"] for cast in top_casts]
            casts_names = [cast["name"] for cast in top_casts]
            casts_chars = [cast["character"] for cast in top_casts]
            casts_profiles = [
                f"https://image.tmdb.org/t/p/original{cast['profile_path']}"
                for cast in top_casts
            ]

            # Fetch actor details concurrently
            actor_details = await asyncio.gather(
                *(self.get_actor_details(session, cast_id) for cast_id in casts_ids)
            )

            casts_biographys = [details["biography"] for details in actor_details]
            casts_birthdays = [details["birthday"] for details in actor_details]
            casts_place_of_births = [details["place_of_birth"] for details in actor_details]
            casts_genders = [details["gender"] for details in actor_details]

            return {
                "casts_ids": casts_ids,
                "casts_names": casts_names,
                "casts_chars": casts_chars,
                "casts_profiles": casts_profiles,
                "casts_biographys": casts_biographys,
                "casts_birthdays": casts_birthdays,
                "casts_place_of_births": casts_place_of_births,
                "casts_genders": casts_genders,
            }

    async def get_actor_details(self, session, actor_id: int):
        url = f"{self.api_base_url}/person/{actor_id}"
        params = {"api_key": self.api_key}

        async with session.get(url, params=params) as response:
            if response.status != 200:
                print(f"Error: {response.status}")
                return {}

            data = await response.json()
            return {
                "biography": data.get("biography", "N/A"),
                "birthday": data.get("birthday", "N/A"),
                "place_of_birth": data.get("place_of_birth", "N/A"),
                "gender": "Male" if data["gender"] == 2 else "Female",
            }

    async def get_recommended_movies_posters(self, session, movie_ids: list):
        tasks = [self._fetch_movie_data(session, movie_id) for movie_id in movie_ids]
        results = await asyncio.gather(*tasks)
        return [result["poster"] for result in results if result]

# API Endpoint
class MovieRequest(BaseModel):
    title: str

