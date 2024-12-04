import os

class Config(object):
    MONGO_URI = os.environ.get("MONGO_URI")
    JWT_SECRET = os.environ.get("JWT_SECRET")
    TMDB_BASE_URL = os.environ.get("TMDB_BASE_URL")
    TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
    
