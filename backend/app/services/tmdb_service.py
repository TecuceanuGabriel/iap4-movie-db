import requests
import hashlib
import json

from app.config import Config
from app.extensions import request_cache


def generate_cache_key(endpoint, params):
    params_str = json.dumps(params, sort_keys=True)
    url = f"{endpoint}?{params_str}"
    return hashlib.md5(url.encode()).hexdigest()


def fetch_tmdb_data(endpoint, params=None):
    cache_key = generate_cache_key(endpoint, params)
    cached_data = request_cache.get(cache_key)
    if cached_data:
        return json.loads(cached_data), 200

    endpoint.lstrip("/")
    url = f"{Config.TMDB_BASE_URL}/{endpoint}"
    headers = {"Authorization": f"Bearer {Config.TMDB_API_KEY}"}
    params = params or {}

    response = requests.get(url, headers=headers, params=params, timeout=10)
    if response.status_code != 200:
        return {
            "error": f"TMDB API error: {response.text}"
        }, response.status_code

    request_cache.set(cache_key, json.dumps(response.json()), ex=3600)

    return response.json(), 200
