import requests
import os

# Defina sua chave de API
GOOGLE_PLACES_API_KEY = "AIzaSyD-6ZNY60WO084dc27zSUZTEYDxDwH5PtQ"

def search_places(query: str, location: str, place_type: str = "tourist_attraction", max_results=5):
    """Busca lugares usando a Google Places API."""
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{query} in {location}",
        "type": place_type,
        "key": GOOGLE_PLACES_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" in data:
        results = [
            {
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "rating": place.get("rating"),
                "user_ratings_total": place.get("user_ratings_total"),
            }
            for place in data["results"][:max_results]
        ]
        return results
    else:
        return {"error": "No results found"}

# Teste para buscar atrações turísticas em Paris
print(search_places("landmarks", "Paris"))
