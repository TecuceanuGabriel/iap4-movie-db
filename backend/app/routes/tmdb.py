from flask import Blueprint, request, jsonify

from app.services.tmdb_service import fetch_tmdb_data

tmdb = Blueprint("tmdb", __name__)


@tmdb.route("/configuration", methods=["GET"])
def get_configuration():
    return fetch_tmdb_data("configuration")


@tmdb.route("/genre/movie/list", methods=["GET"])
def get_movie():
    return fetch_tmdb_data("genre/movie/list")


@tmdb.route("/genre/tv/list", methods=["GET"])
def get_tv_genres():
    return fetch_tmdb_data("genre/tv/list")


# movies
@tmdb.route("/movie/details/<int:movie_id>")
def get_movie_details(movie_id):
    return fetch_tmdb_data(f"movie/{movie_id}")


@tmdb.route("/movie/popular/<int:page>", methods=["GET"])
def get_popular_movies(page):
    data, status_code = fetch_tmdb_data("movie/popular", {"page": page})
    if status_code != 200:
        return data, status_code

    for result in data["results"]:
        movie_details, movie_status_code = get_movie_details(result["id"])
        if movie_status_code == 200:
            result["runtime"] = movie_details.get("runtime")
        else:
            result["runtime"] = None

    return data, status_code


@tmdb.route("/movie/top_rated/<int:page>", methods=["GET"])
def get_top_rated_movies(page):
    return fetch_tmdb_data("movie/top_rated", {"page": page})


@tmdb.route("/movie/upcoming/<int:page>", methods=["GET"])
def get_upcoming_movies(page):
    return fetch_tmdb_data("movie/upcoming", {"page": page})


@tmdb.route("/movie/<int:movie_id>/images", methods=["GET"])
def get_movie_images(movie_id):
    return fetch_tmdb_data(f"movie/{movie_id}/images")


# tv shows
@tmdb.route("/tv/popular/<int:page>", methods=["GET"])
def get_popular_tv(page):
    return fetch_tmdb_data("tv/popular", {"page": page})


@tmdb.route("/tv/top_rated/<int:page>", methods=["GET"])
def get_top_rated_tv(page):
    return fetch_tmdb_data("tv/top_rated", {"page": page})


# find
@tmdb.route("/search/multi/<string:query>/<int:page>", methods=["GET"])
def search_multi(query, page):
    return fetch_tmdb_data("search/multi", {"query": query, "page": page})


@tmdb.route("/search/movie/<string:query>/<int:page>", methods=["GET"])
def search_movie(query, page=1):
    genres = request.args.get("genres")

    data, status_code = fetch_tmdb_data(
        "search/movie", {"query": query, "page": page}
    )

    if status_code != 200:
        return data, status_code

    movies = data.get("results", [])

    if genres:
        genres = set(map(int, genres.split(",")))
        movies = [
            movie
            for movie in movies
            if genres.issubset(set(movie.get("genre_ids", [])))
        ]

    return jsonify({"results": movies}), 200


@tmdb.route("/search/tv/<string:query>/<int:page>", methods=["GET"])
def search_tv(query, page=1):
    genres = request.args.get("genres")

    data, status_code = fetch_tmdb_data(
        "search/tv", {"query": query, "page": page}
    )

    if status_code != 200:
        return data, status_code

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
