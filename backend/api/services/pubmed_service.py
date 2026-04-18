import requests
import os
from django.conf import settings

def search_pubmed(disease: str, location: str = "", max_results: int = 50) -> list:
    """
    Search PubMed for research publications related to disease + location.
    Returns list of article metadata dicts.
    """
    PUBMED_BASE = getattr(settings, 'PUBMED_BASE_URL', 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils')
    headers = {'User-Agent': getattr(settings, 'DEFAULT_USER_AGENT', 'CuraLink/1.0')}
    
    query = f"{disease}"
    if location:
        query += f" {location}"

    if not disease or len(disease) < 2:
        return []

    # Step 1: Get IDs
    search_url = f"{PUBMED_BASE}/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance",
    }

    try:
        search_resp = requests.get(search_url, params=search_params, headers=headers, timeout=15)
        search_resp.raise_for_status()
        resp_json = search_resp.json()
        ids = resp_json.get("esearchresult", {}).get("idlist", [])
    except Exception as e:
        print(f"PubMed search error for query '{query}': {e}")
        return []

    if not ids:
        return []

    # Step 2: Fetch summaries
    summary_url = f"{PUBMED_BASE}/esummary.fcgi"
    summary_params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "json",
    }

    try:
        summary_resp = requests.get(summary_url, params=summary_params, headers=headers, timeout=15)
        summary_resp.raise_for_status()
        result_data = summary_resp.json().get("result", {})
    except Exception as e:
        print(f"PubMed summary error: {e}")
        return []

    articles = []
    for uid in ids:
        item = result_data.get(uid, {})
        if not item:
            continue
        articles.append({
            "source": "PubMed",
            "id": uid,
            "title": item.get("title", "No title"),
            "authors": [a.get("name") for a in item.get("authors", [])],
            "journal": item.get("fulljournalname", ""),
            "pubdate": item.get("pubdate", ""),
            "abstract": "",   # fetched separately if needed
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
        })

    return articles

def fetch_abstract(pubmed_id: str) -> str:
    """Fetch abstract text for a single PubMed article."""
    PUBMED_BASE = getattr(settings, 'PUBMED_BASE_URL', 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils')
    headers = {'User-Agent': getattr(settings, 'DEFAULT_USER_AGENT', 'CuraLink/1.0')}
    
    fetch_url = f"{PUBMED_BASE}/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": pubmed_id,
        "rettype": "abstract",
        "retmode": "text",
    }
    try:
        resp = requests.get(fetch_url, params=params, headers=headers, timeout=10)
        return resp.text.strip()
    except:
        return ""
