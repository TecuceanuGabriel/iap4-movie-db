from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

from dotenv import load_dotenv

import jwt

import os
import datetime
import requests

from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["JWT_SECRET"] = os.environ.get("JWT_SECRET")

mongo = PyMongo(app)


# app
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


@app.route("/")
def hello_world():
    return "Discombobulated"


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


# tmdb
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
TMDB_BASE_URL = os.environ.get("TMDB_BASE_URL")


def fetch_tmdb_data(endpoint, params=None):
    url = f"{TMDB_BASE_URL}/{endpoint}"
    headers = {"Authorization": f"Bearer {TMDB_API_KEY}"}
    params = params or {}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return {
            "error": f"TMDB API error: {response.text}"
        }, response.status_code

    return response.json(), 200


@app.route("/configuration", methods=["GET"])
def get_configuration():
    data, status_code = fetch_tmdb_data("configuration")
    return jsonify(data), status_code


# movies
@app.route("/movie/popular", methods=["GET"])
def get_popular_movies():
    data, status_code = fetch_tmdb_data(
        "movie/popular", {"page": request.args.get("page")}
    )
    return jsonify(data), status_code


@app.route("/movie/top_rated", methods=["GET"])
def get_top_rated_movies():
    data, status_code = fetch_tmdb_data(
        "movie/top_rated", {"page": request.args.get("page")}
    )
    return jsonify(data), status_code


@app.route("/movie/upcoming", methods=["GET"])
def get_upcoming_movies():
    data, status_code = fetch_tmdb_data(
        "movie/upcoming", {"page": request.args.get("page")}
    )
    return jsonify(data), status_code


@app.route("/movie/<int:movie_id>/images", methods=["GET"])
def get_movie_images(movie_id):
    data, status_code = fetch_tmdb_data(f"movie/{movie_id}/images")
    return jsonify(data), status_code


# tv shows
@app.route("/tv/popular", methods=["GET"])
def get_popular_tv():
    data, status_code = fetch_tmdb_data(
        "tv/popular", {"page": request.args.get("page")}
    )
    return jsonify(data), status_code


@app.route("/tv/top_rated", methods=["GET"])
def get_top_rated_tv():
    data, status_code = fetch_tmdb_data(
        "tv/top_rated", {"page": request.args.get("page")}
    )
    return jsonify(data), status_code


# search
@app.route("/search/multi", methods=["GET"])
def search_multi():
    query = request.args.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    data, status_code = fetch_tmdb_data(
        "search/multi", {"query": query, "page": request.args.get("page")}
    )
    return jsonify(data), status_code


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
