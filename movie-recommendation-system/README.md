```markdown
# Movie Recommendation System

## Overview

The Movie Recommendation System provides personalized movie suggestions based on user input and preferences. By combining web scraping for data collection, natural language processing (NLP), machine learning models, Flask and FastAPI for backend services, and a dynamic frontend, this system delivers a robust and engaging user experience.

## Features

- **Search Functionality**: Autocomplete suggestions and search form for movie queries.
- **Movie Details**: Display detailed information including posters, overviews, ratings, and more.
- **Recommendations**: Curated lists of recommended movies based on user preferences.
- **User Reviews**: View and share comments on movies.
- **Top Cast Members**: Detailed information about cast members with modal views.

## Tech Stack

- **Web Scraping**: Python with BeautifulSoup and Requests
- **NLP**: Python's `nltk` library for text processing, `sklearn` for feature extraction
- **Machine Learning**: Multinomial Naive Bayes classifier
- **Cosine Similarity**: For measuring movie similarity
- **Backend**: Flask and FastAPI for building high-performance APIs
- **Frontend**: HTML, CSS, JavaScript, Bootstrap for responsive design
- **Model Persistence**: `pickle` for saving and loading models and vectorizers

## Installation

### Prerequisites

- Python 3.7+
- `pip` for installing Python packages

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/aiBard101/Machine-Learning-Projects.git
   cd Machine-Learning-Projects/movie-recommendation-system
   ```

2. **Install Dependencies**

   Install the required Python packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare Data**

   Ensure you have the dataset `TestReviews.csv` in the `datasets` directory. If you need to scrape additional data, follow the web scraping guidelines in the project.

4. **Run the Backend**

   Run the application:

   ```bash
   python app.py
   ```

5. **Run the Frontend**

   Open a web browser and navigate to http://localhost:5000.

## Project Structure

```
movie-recommendation-system/
├── app.py          
├── recommedation_sys.py
├── reviews.py
├── static/
│   ├── styles.css        # CSS for styling
│   └── script.js         # JavaScript for interactivity
|── templates/
|    └── index.html        # HTML for the frontend
├── notebooks/
│   ├── MovieRecommendation.ipynb  
│   └── nlp_model.ipynb        
├── models/
│   ├── cosine_sim_prod.pkl
|   ├── cosine_sim.pkl
|   ├── nlp_model.pkl
│   └── tranform.pkl 
└── datasets/
    ├── main_df.csv
    ├── TestReviews.csv
    ├── tmdb_5000_credits.csv
    └── tmdb_5000_movies.csv
```

## Usage

1. **Search for Movies**

   Use the search bar to input movie titles and get autocomplete suggestions. Submit the query to fetch relevant movie details.

2. **View Movie Details**

   Click on a movie to view detailed information such as the poster, overview, rating, and more.

3. **Get Recommendations**

   View top recommended movies based on user preferences or movies produced by the same production companies.

4. **Read and Share Reviews**

   Check out user reviews and share your own comments on the movie page.

5. **Explore Cast Members**

   Click on cast names to view detailed information in a modal.

## APIs

- **Search API**: Provides autocomplete suggestions and handles search queries.
- **Movie Details API**: Fetches detailed movie information.
- **Cast Details API**: Retrieves information about cast members.
- **Recommendations API**: Provides movie recommendations based on various criteria.

## Models

- **Text Classification**: Multinomial Naive Bayes model for classifying movie reviews.
- **Cosine Similarity**: Measures the similarity between movies for recommendation purposes.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the powerful and fast backend framework.
- [Scikit-learn](https://scikit-learn.org/) for machine learning tools.
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping.
- [Bootstrap](https://getbootstrap.com/) for frontend styling.

## Contact

For any questions or feedback, please contact:

- **Email**: [aibard.annonymousasquare@gmail.com](aibard.annonymousasquare@gmail.com)
- **GitHub**: [aiBard](https://github.com/aiBard101/)
- **X**: [aiBard001](https://x.com/aiBard001)
- **Telegram**: [aiBard001](https://t.me/aiBard101)
- **LinkedIn**: [aiBard](https://www.linkedin.com/in/george-junior-alainengiya-5b44b5251/)
- **WhatsApp**: [aiBard](https://%20https://wa.me/message/AL5IJZCUYD6LG1)
- **Visit my Website**: [Website](https://aibard.code.blog/).

---
Watch the [YouTube video](https://youtu.be/M-sHa80d1Oc) demonstrating the application.
