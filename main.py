from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import os
import requests


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
TMDB_BACKDROP_URL = "https://image.tmdb.org/t/p/original"


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="Netflix DevSecOps API",
    version="4.0.0",
    description="Netflix-style movie and series API powered by TMDB"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# STARTUP MESSAGE
# ============================================================

if TMDB_API_KEY:

    print("--------------------------------------")
    print("Netflix DevSecOps API")
    print("TMDB API KEY LOADED")
    print("API READY")
    print("--------------------------------------")

else:

    print("--------------------------------------")
    print("WARNING: TMDB_API_KEY NOT FOUND")
    print("Check .env file")
    print("--------------------------------------")


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Netflix DevSecOps API",
        "status": "running",
        "tmdb": "connected" if TMDB_API_KEY else "not configured"
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "Netflix DevSecOps API"
    }


# ============================================================
# TMDB REQUEST
# ============================================================

def tmdb_request(endpoint: str, params=None):

    if not TMDB_API_KEY:

        raise HTTPException(
            status_code=500,
            detail="TMDB_API_KEY is missing. Check .env file."
        )

    if params is None:
        params = {}

    params["api_key"] = TMDB_API_KEY

    try:

        response = requests.get(
            f"{TMDB_BASE_URL}{endpoint}",
            params=params,
            timeout=15
        )

    except requests.RequestException as error:

        raise HTTPException(
            status_code=503,
            detail=f"TMDB connection failed: {str(error)}"
        )

    if response.status_code != 200:

        raise HTTPException(
            status_code=response.status_code,
            detail="TMDB API request failed"
        )

    return response.json()


# ============================================================
# POSTER
# ============================================================

def get_poster(poster_path):

    if poster_path:

        return f"{TMDB_IMAGE_URL}{poster_path}"

    return None


# ============================================================
# BACKDROP
# ============================================================

def get_backdrop(backdrop_path):

    if backdrop_path:

        return f"{TMDB_BACKDROP_URL}{backdrop_path}"

    return None


# ============================================================
# YEAR
# ============================================================

def get_year(date_value):

    if not date_value:
        return None

    try:

        return int(date_value[:4])

    except (ValueError, TypeError):

        return None


# ============================================================
# FORMAT MOVIE
# ============================================================

def format_movie(movie, category="Movie"):

    release_date = movie.get(
        "release_date",
        ""
    )

    genres = movie.get(
        "genres",
        []
    )

    genre_names = [
        genre.get("name")
        for genre in genres
        if genre.get("name")
    ]

    return {

        "id": movie.get("id"),

        "title": movie.get(
            "title",
            movie.get(
                "name",
                "Unknown"
            )
        ),

        "category": category,

        "genre": (
            ", ".join(genre_names)
            if genre_names
            else "Unknown"
        ),

        "year": get_year(
            release_date
        ),

        "poster": get_poster(
            movie.get("poster_path")
        ),

        "backdrop": get_backdrop(
            movie.get("backdrop_path")
        ),

        "overview": movie.get(
            "overview",
            ""
        ),

        "rating": movie.get(
            "vote_average",
            0
        )

    }


# ============================================================
# ALL MOVIES
# ============================================================

@app.get("/api/movies")
def get_movies():

    movies = []


    # ========================================================
    # ENGLISH MOVIES
    # ========================================================

    english_data = tmdb_request(
        "/discover/movie",
        {
            "language": "en-US",
            "sort_by": "popularity.desc",
            "page": 1,
            "with_original_language": "en",
            "include_adult": False
        }
    )

    english_results = english_data.get(
        "results",
        []
    )

    for movie in english_results[:10]:

        movies.append(
            format_movie(
                movie,
                "English"
            )
        )


    # ========================================================
    # HINDI MOVIES
    #
    # IMPORTANT:
    # language = en-US
    # means titles like:
    #
    # Jawan
    # Dangal
    # 3 Idiots
    #
    # NOT:
    #
    # जवान
    # दंगल
    #
    # with_original_language = hi
    # keeps the movies Hindi.
    # ========================================================

    hindi_data = tmdb_request(
        "/discover/movie",
        {
            "language": "en-US",
            "sort_by": "popularity.desc",
            "page": 1,
            "with_original_language": "hi",
            "include_adult": False
        }
    )

    hindi_results = hindi_data.get(
        "results",
        []
    )

    for movie in hindi_results[:10]:

        movies.append(
            format_movie(
                movie,
                "Hindi"
            )
        )


    return {

        "count": len(movies),

        "movies": movies

    }


# ============================================================
# HINDI MOVIES ONLY
# ============================================================

@app.get("/api/movies/hindi")
def get_hindi_movies():

    data = tmdb_request(
        "/discover/movie",
        {
            "language": "en-US",
            "sort_by": "popularity.desc",
            "page": 1,
            "with_original_language": "hi",
            "include_adult": False
        }
    )

    results = data.get(
        "results",
        []
    )

    movies = []

    for movie in results[:20]:

        movies.append(
            format_movie(
                movie,
                "Hindi"
            )
        )

    return {

        "count": len(movies),

        "movies": movies

    }


# ============================================================
# ENGLISH MOVIES ONLY
# ============================================================

@app.get("/api/movies/english")
def get_english_movies():

    data = tmdb_request(
        "/discover/movie",
        {
            "language": "en-US",
            "sort_by": "popularity.desc",
            "page": 1,
            "with_original_language": "en",
            "include_adult": False
        }
    )

    results = data.get(
        "results",
        []
    )

    movies = []

    for movie in results[:20]:

        movies.append(
            format_movie(
                movie,
                "English"
            )
        )

    return {

        "count": len(movies),

        "movies": movies

    }


# ============================================================
# SERIES
# ============================================================

@app.get("/api/series")
def get_series():

    data = tmdb_request(
        "/trending/tv/week",
        {
            "language": "en-US"
        }
    )

    results = data.get(
        "results",
        []
    )

    series = []

    for item in results[:20]:

        first_air_date = item.get(
            "first_air_date",
            ""
        )

        series.append({

            "id": item.get(
                "id"
            ),

            "title": item.get(
                "name",
                "Unknown"
            ),

            "category": "Series",

            "genre": "Series",

            "year": get_year(
                first_air_date
            ),

            "poster": get_poster(
                item.get(
                    "poster_path"
                )
            ),

            "backdrop": get_backdrop(
                item.get(
                    "backdrop_path"
                )
            ),

            "overview": item.get(
                "overview",
                ""
            ),

            "rating": item.get(
                "vote_average",
                0
            )

        })

    return {

        "count": len(series),

        "series": series

    }


# ============================================================
# MOVIE DETAILS
# ============================================================

@app.get("/api/movies/{movie_id}")
def get_movie(movie_id: int):

    data = tmdb_request(
        f"/movie/{movie_id}",
        {
            "language": "en-US"
        }
    )

    if not data.get("id"):

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return format_movie(
        data,
        "Movie"
    )


# ============================================================
# SEARCH
# ============================================================

@app.get("/api/search")
def search_movies(q: str):

    if not q.strip():

        return {
            "query": q,
            "count": 0,
            "results": []
        }


    data = tmdb_request(
        "/search/multi",
        {
            "query": q,
            "language": "en-US",
            "page": 1,
            "include_adult": False
        }
    )


    results = data.get(
        "results",
        []
    )

    search_results = []


    for item in results:

        media_type = item.get(
            "media_type"
        )


        # ====================================================
        # MOVIE
        # ====================================================

        if media_type == "movie":

            release_date = item.get(
                "release_date",
                ""
            )

            search_results.append({

                "id": item.get(
                    "id"
                ),

                "title": item.get(
                    "title",
                    "Unknown"
                ),

                "category": "Movie",

                "genre": "Movie",

                "year": get_year(
                    release_date
                ),

                "poster": get_poster(
                    item.get(
                        "poster_path"
                    )
                ),

                "backdrop": get_backdrop(
                    item.get(
                        "backdrop_path"
                    )
                ),

                "overview": item.get(
                    "overview",
                    ""
                ),

                "rating": item.get(
                    "vote_average",
                    0
                )

            })


        # ====================================================
        # SERIES
        # ====================================================

        elif media_type == "tv":

            first_air_date = item.get(
                "first_air_date",
                ""
            )

            search_results.append({

                "id": item.get(
                    "id"
                ),

                "title": item.get(
                    "name",
                    "Unknown"
                ),

                "category": "Series",

                "genre": "Series",

                "year": get_year(
                    first_air_date
                ),

                "poster": get_poster(
                    item.get(
                        "poster_path"
                    )
                ),

                "backdrop": get_backdrop(
                    item.get(
                        "backdrop_path"
                    )
                ),

                "overview": item.get(
                    "overview",
                    ""
                ),

                "rating": item.get(
                    "vote_average",
                    0
                )

            })


    return {

        "query": q,

        "count": len(search_results),

        "results": search_results

    }


# ============================================================
# CATEGORIES
# ============================================================

@app.get("/api/categories")
def get_categories():

    return {

        "categories": [

            "Hindi",

            "English",

            "Series",

            "Action",

            "Comedy",

            "Drama",

            "Fantasy",

            "Sci-Fi",

            "Romance"

        ]

    }


# ============================================================
# TRENDING
# ============================================================

@app.get("/api/trending")
def get_trending():

    data = tmdb_request(
        "/trending/all/week",
        {
            "language": "en-US"
        }
    )

    results = data.get(
        "results",
        []
    )

    trending = []


    for item in results[:20]:

        media_type = item.get(
            "media_type"
        )


        # ----------------------------------------------------
        # TRENDING MOVIE
        # ----------------------------------------------------

        if media_type == "movie":

            release_date = item.get(
                "release_date",
                ""
            )

            trending.append({

                "id": item.get(
                    "id"
                ),

                "title": item.get(
                    "title",
                    "Unknown"
                ),

                "category": "Movie",

                "year": get_year(
                    release_date
                ),

                "poster": get_poster(
                    item.get(
                        "poster_path"
                    )
                ),

                "backdrop": get_backdrop(
                    item.get(
                        "backdrop_path"
                    )
                ),

                "overview": item.get(
                    "overview",
                    ""
                ),

                "rating": item.get(
                    "vote_average",
                    0
                )

            })


        # ----------------------------------------------------
        # TRENDING SERIES
        # ----------------------------------------------------

        elif media_type == "tv":

            first_air_date = item.get(
                "first_air_date",
                ""
            )

            trending.append({

                "id": item.get(
                    "id"
                ),

                "title": item.get(
                    "name",
                    "Unknown"
                ),

                "category": "Series",

                "year": get_year(
                    first_air_date
                ),

                "poster": get_poster(
                    item.get(
                        "poster_path"
                    )
                ),

                "backdrop": get_backdrop(
                    item.get(
                        "backdrop_path"
                    )
                ),

                "overview": item.get(
                    "overview",
                    ""
                ),

                "rating": item.get(
                    "vote_average",
                    0
                )

            })


    return {

        "count": len(trending),

        "results": trending

    }