import requests

from app.config import Config


def fetch_tmdb_data(endpoint, params=None):
    endpoint.lstrip("/")
    url = f"{Config.TMDB_BASE_URL}/{endpoint}"
    headers = {"Authorization": f"Bearer {Config.TMDB_API_KEY}"}
    params = params or {}

    response = requests.get(url, headers=headers, params=params, timeout=10)
    if response.status_code != 200:
        return {
            "error": f"TMDB API error: {response.text}"
        }, response.status_code

    return response.json(), 200
