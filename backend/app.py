from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

from dotenv import load_dotenv

import jwt

import os
import datetime

from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["JWT_SECRET"] = os.environ.get("JWT_SECRET")

mongo = PyMongo(app)


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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
