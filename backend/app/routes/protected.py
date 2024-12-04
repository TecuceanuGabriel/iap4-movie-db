from flask import Blueprint, request, jsonify

from app.extensions import mongo
from app.services.auth_service import verify_token

protected = Blueprint("protected", __name__)


@protected.route("/profile", methods=["GET"])
def get_profile():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    email = payload["email"]

    user = mongo.db.users.find_one(
        {"email": email}, {"password": 0, "_id": 0, "watchlist": 0}
    )

    return jsonify(user), 200


@protected.route("/watchlist/movie/add", methods=["POST"])
def add_to_watchlist():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    email = payload["email"]

    data = request.json
    movie_id = data.get("movie_id")

    if not movie_id:
        return jsonify({"error": "Movie ID is required"}), 400

    user = mongo.db.users.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404

    watchlist = user.get("movie_watchlist", [])

    if movie_id in watchlist:
        return jsonify({"error": "Movie already in watchlist"}), 400

    watchlist.append(movie_id)

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"movie_watchlist": watchlist}},
    )

    return jsonify({"message": "Movie added to watchlist"}), 200


@protected.route("/watchlist/movie/remove", methods=["POST"])
def remove_from_watchlist():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    email = payload["email"]

    data = request.json
    movie_id = data.get("movie_id")

    if not movie_id:
        return jsonify({"error": "Movie ID is required"}), 400

    user = mongo.db.users.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404

    watchlist = user.get("movie_watchlist", [])

    if movie_id not in watchlist:
        return jsonify({"error": "Movie not in watchlist"}), 400

    watchlist.remove(movie_id)

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"movie_watchlist": watchlist}},
    )

    return jsonify({"message": "Movie removed from watchlist"}), 200


@protected.route("/watchlist/movie", methods=["GET"])
def get_watchlist():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    email = payload["email"]

    user = mongo.db.users.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404

    watchlist = user.get("movie_watchlist", [])

    return jsonify(watchlist), 200


@protected.route("/watchlist/tv/add", methods=["POST"])
def add_tv_to_watchlist():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    email = payload["email"]

    data = request.json
    tv_id = data.get("tv_id")

    if not tv_id:
        return jsonify({"error": "TV ID is required"}), 400

    user = mongo.db.users.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404

    watchlist = user.get("tv_watchlist", [])

    if tv_id in watchlist:
        return jsonify({"error": "TV show already in watchlist"}), 400

    watchlist.append(tv_id)

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"tv_watchlist": watchlist}},
    )

    return jsonify({"message": "TV show added to watchlist"}), 200


@protected.route("/watchlist/tv/remove", methods=["POST"])
def remove_tv_from_watchlist():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    email = payload["email"]

    data = request.json
    tv_id = data.get("tv_id")

    if not tv_id:
        return jsonify({"error": "TV ID is required"}), 400

    user = mongo.db.users.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404

    watchlist = user.get("tv_watchlist", [])

    if tv_id not in watchlist:
        return jsonify({"error": "TV show not in watchlist"}), 400

    watchlist.remove(tv_id)

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"tv_watchlist": watchlist}},
    )

    return jsonify({"message": "TV show removed from watchlist"}), 200


@protected.route("/watchlist/tv", methods=["GET"])
def get_tv_watchlist():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    email = payload["email"]

    user = mongo.db.users.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404

    watchlist = user.get("tv_watchlist", [])

    return jsonify(watchlist), 200
