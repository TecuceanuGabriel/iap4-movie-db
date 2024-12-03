from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_pymongo import PyMongo
from flask_cors import CORS

from dotenv import load_dotenv

import jwt

import requests
import datetime
import os

from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(_name_)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
app.config["JWT_SECRET"] = os.environ.get("JWT_SECRET")

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_API_KEY = os.environ.get("VITE_TMDB_KEY")

def generate_token(email):
    return jwt.encode(
        {
            "email": email,
            "exp": datetime.datetime.now() + datetime.timedelta(days=1),
        },
        app.config["JWT_SECRET"],
        algorithm="HS256",
    )


def verify_token(token):
    try:
        return (
            jwt.decode(token, app.config["JWT_SECRET"], algorithms=["HS256"]),
            None,
        )
    except jwt.ExpiredSignatureError:
        return None, {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return None, {"error": "Invalid token"}


@app.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username:
        return jsonify({"error": "Username is required"}), 400
    if not email:
        return jsonify({"error": "Email is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400

    if mongo.db.users.find_one({"email": email}):
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = generate_password_hash(password)

    mongo.db.users.insert_one(
        {
            "username": username,
            "email": email,
            "password": hashed_password,
        }
    )

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    if not email:
        return jsonify({"error": "Email is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400

    user = mongo.db.users.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid password"}), 400

    return jsonify({"token": generate_token(email)}), 200


@app.route("/profile", methods=["GET"])
def get_profile():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    email = payload["email"]

    user = mongo.db.users.find_one({"email": email}, {"password": 0, "_id": 0})

    return jsonify(user), 200

def fetch_tmdb_data(endpoint, params=None):
    endpoint.lstrip("/")
    url = f"{TMDB_BASE_URL}/{endpoint}"
    headers = {"Authorization": f"Bearer {TMDB_API_KEY}"}
    params = params or {}

    response = requests.get(url, headers=headers, params=params, timeout=10)
    if response.status_code != 200:
        return {
            "error": f"TMDB API error: {response.text}"
        }, response.status_code

    return response.json(), 200


@app.route("/configuration", methods=["GET"])
def get_configuration():
    data, status_code = fetch_tmdb_data("configuration")
    return jsonify(data), status_code


@app.route("/genre/movie/list", methods=["GET"])
def get_movie():
    data, status_code = fetch_tmdb_data("genre/movie/list")
    return jsonify(data), status_code


@app.route("/genre/tv/list", methods=["GET"])
def get_tv_genres():
    data, status_code = fetch_tmdb_data("genre/tv/list")
    return jsonify(data), status_code


# movies
@app.route("/movie/details/<int:movie_id>")
def get_movie_details(movie_id, jsonify=True):
    data, status_code = fetch_tmdb_data(f"movie/{movie_id}")
    if status_code != 200:
        return data["error"], status_code
    if (jsonify):
        return jsonify(data), status_code
    else:
        return data, status_code


@app.route("/movie/popular/<int:page>", methods=["GET"])
def get_popular_movies(page):
    data, status_code = fetch_tmdb_data(f"movie/popular?page={page}")
    if status_code != 200:
        return data["error"], status_code

    for result in data["results"]:
        movie_details, movie_status_code = get_movie_details(result["id"], False)
        if movie_status_code == 200:
            result["runtime"] = movie_details["runtime"]
        else:
            result["runtime"] = None

    return jsonify(data), status_code


@app.route("/movie/top_rated/<int:page>", methods=["GET"])
def get_top_rated_movies(page):
    data, status_code = fetch_tmdb_data(
        "movie/top_rated", {"page": page}
    )
    return jsonify(data), status_code


@app.route("/movie/upcoming/<int:page>", methods=["GET"])
def get_upcoming_movies(page):
    data, status_code = fetch_tmdb_data(
        "movie/upcoming", {"page": page}
    )
    return jsonify(data), status_code


@app.route("/movie/<int:movie_id>/images", methods=["GET"])
def get_movie_images(movie_id):
    data, status_code = fetch_tmdb_data(f"movie/{movie_id}/images")
    return jsonify(data), status_code


# tv shows
@app.route("/tv/popular/<int:page>", methods=["GET"])
def get_popular_tv(page):
    data, status_code = fetch_tmdb_data(
        "tv/popular", {"page": page}
    )
    return jsonify(data), status_code


@app.route("/tv/top_rated/<int:page>", methods=["GET"])
def get_top_rated_tv(page):
    data, status_code = fetch_tmdb_data(
        "tv/top_rated", {"page": page}
    )
    return jsonify(data), status_code


# find
@app.route("/search/multi/<string:query>/<int:page>", methods=["GET"])
def search_multi(query, page):
    if not query:
        return jsonify({"error": "Query is required"}), 400

    data, status_code = fetch_tmdb_data(
        "search/multi", {"query": query, "page": page}
    )
    return jsonify(data), status_code


@app.route("/search/movie/<string:query>/<int:page>", methods=["GET"])
def search_movie(query, page=0):
    genres = request.args.get("genres")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    data, status_code = fetch_tmdb_data(
        "search/movie", {"query": query, "page": page}
    )

    if status_code != 200:
        return jsonify(data), status_code

    movies = data.get("results", [])

    if genres:
        genres = set(map(int, genres.split(",")))
        movies = [
            movie
            for movie in movies
            if genres.issubset(set(movie.get("genre_ids", [])))
        ]

    return jsonify({"results": movies}), 200


@app.route("/search/tv/<string:query>/<int:page>", methods=["GET"])
def search_tv(query, page):
    genres = request.args.get("genres")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    data, status_code = fetch_tmdb_data(
        "search/tv", {"query": query, "page": page}
    )

    if status_code != 200:
        return jsonify(data), status_code

    shows = data.get("results", [])

    if genres:
        genres = genres.split(",")
        genres = set(map(int, genres))
        shows = [
            show
            for show in shows
            if genres.issubset(set(show.get("genre_ids", [])))
        ]

    return jsonify({"results": shows}), 200

if _name_ == "_main_":
    app.run(debug=True, host="0.0.0.0", port=5000)