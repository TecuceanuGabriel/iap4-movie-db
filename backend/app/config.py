import os


class Config(object):
    MONGO_URI = os.environ.get("MONGO_URI")
    JWT_SECRET = os.environ.get("JWT_SECRET")
    TMDB_BASE_URL = os.environ.get("TMDB_BASE_URL")
    TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
    SCHEDULER_API_ENABLED = os.environ.get("SCHEDULER_API_ENABLED")
    SCHEDULER_TIMEZONE = os.environ.get("SCHEDULER_TIMEZONE")
    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PORT = os.environ.get("REDIS_PORT")
