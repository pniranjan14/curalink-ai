import requests
from django.conf import settings

def search_openalex(disease: str, location: str = "", max_results: int = 50) -> list:
    """
    Search OpenAlex for open-access research works related to the disease.
    """
    OPENALEX_BASE = settings.OPENALEX_BASE_URL
    query = f"{disease}"
    if location:
        query += f" {location}"

    url = f"{OPENALEX_BASE}/works"
    params = {
        "search": query,
        "per-page": max_results,
        "sort": "relevance_score:desc",
        "filter": "is_oa:true",   # only open access
        "select": "id,title,authorships,publication_year,primary_location,abstract_inverted_index,doi",
    }

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        works = resp.json().get("results", [])
    except Exception as e:
        print(f"OpenAlex error: {e}")
        return []

    results = []
    for work in works:
        authors = [
            a.get("author", {}).get("display_name", "")
            for a in work.get("authorships", [])
        ]
        location_info = work.get("primary_location") or {}
        source = location_info.get("source") or {}
        results.append({
            "source": "OpenAlex",
            "id": work.get("id", ""),
            "title": work.get("title", "No title"),
            "authors": authors,
            "journal": source.get("display_name", ""),
            "pubdate": str(work.get("publication_year", "")),
            "abstract": _reconstruct_abstract(work.get("abstract_inverted_index", {})),
            "url": work.get("doi", work.get("id", "")),
        })

    return results

def _reconstruct_abstract(inverted_index: dict) -> str:
    """OpenAlex stores abstracts as inverted index — reconstruct to string."""
    if not inverted_index:
        return ""
    positions = {}
    for word, pos_list in inverted_index.items():
        for pos in pos_list:
            positions[pos] = word
    return " ".join(positions[k] for k in sorted(positions.keys()))
