from flask import Blueprint, jsonify

from app.extensions import mongo


info = Blueprint("info", __name__)


@info.route("/", methods=["GET"])
def index():
    return jsonify({"message": "server is online"}), 200


@info.route("/get_all", methods=["GET"])
def get_all_users():
    users = mongo.db.users.find(
        {},
        {
            "_id": 0,
            "password": 0,
            "email": 0,
            "favourite_people": 0,
            "movie_finished": 0,
            "movie_watchlist": 0,
            "tv_finished": 0,
            "tv_watchlist": 0,
            "feed": 0,
        },
    )

    return jsonify(list(users)), 200
