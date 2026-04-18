import requests
import os
from django.conf import settings

def search_openalex(disease: str, location: str = "", max_results: int = 50) -> list:
    """
    Search OpenAlex for medical research papers.
    """
    OPENALEX_BASE = getattr(settings, 'OPENALEX_BASE_URL', 'https://api.openalex.org')
    headers = {'User-Agent': getattr(settings, 'DEFAULT_USER_AGENT', 'CuraLink/1.0')}
    
    query = f"{disease}"
    if location:
        query += f", {location}"

    if not disease or len(disease) < 2:
        return []

    params = {
        "search": query,
        "per_page": max_results,
        "filter": "type:article",
    }

    try:
        response = requests.get(f"{OPENALEX_BASE}/works", params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"OpenAlex error: {e}")
        return []

    articles = []
    for work in data.get("results", []):
        articles.append({
            "source": "OpenAlex",
            "id": work.get("id"),
            "title": work.get("display_name", "No title"),
            "authors": [a.get("author", {}).get("display_name") for a in work.get("authorships", [])],
            "journal": work.get("primary_location", {}).get("source", {}).get("display_name", ""),
            "pubdate": work.get("publication_date", ""),
            "abstract": "",  # OpenAlex uses inverted index for abstracts, complex to reconstruct
            "url": work.get("doi") or work.get("id"),
        })

    return articles
