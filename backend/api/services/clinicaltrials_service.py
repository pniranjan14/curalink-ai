import requests
from django.conf import settings

def search_clinical_trials(disease: str, location: str = "", max_results: int = 30) -> list:
    """
    Search ClinicalTrials.gov for studies related to disease + location.
    """
    CLINICALTRIALS_BASE = getattr(settings, 'CLINICALTRIALS_BASE_URL', 'https://clinicaltrials.gov/api/v2')
    headers = {'User-Agent': getattr(settings, 'DEFAULT_USER_AGENT', 'CuraLink/1.0')}
    
    url = f"{CLINICALTRIALS_BASE}/studies"
    
    # Improved query handling: location is optional but helpful
    params = {
        "query.cond": disease,
        "pageSize": max_results,
        "format": "json",
    }
    
    if location and len(location) > 1:
        params["query.locn"] = location

    if not disease or len(disease) < 2:
        return []

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        studies = data.get("studies", [])
    except Exception as e:
        print(f"ClinicalTrials error with params {params}: {e}")
        return []

    results = []
    for study in studies:
        proto = study.get("protocolSection", {})
        id_module = proto.get("identificationModule", {})
        status_module = proto.get("statusModule", {})
        desc_module = proto.get("descriptionModule", {})
        design_module = proto.get("designModule", {})

        results.append({
            "source": "ClinicalTrials",
            "nct_id": id_module.get("nctId", ""),
            "title": id_module.get("briefTitle", "No title"),
            "status": status_module.get("overallStatus", ""),
            "phase": ", ".join(design_module.get("phases", []) if design_module else []),
            "start_date": status_module.get("startDateStruct", {}).get("date", ""),
            "completion_date": status_module.get("completionDateStruct", {}).get("date", ""),
            "summary": desc_module.get("briefSummary", ""),
            "url": f"https://clinicaltrials.gov/study/{id_module.get('nctId', '')}",
        })

    return results
