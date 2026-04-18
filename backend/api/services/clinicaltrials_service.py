import requests
from django.conf import settings

def search_clinical_trials(disease: str, location: str = "", max_results: int = 30) -> list:
    """
    Search ClinicalTrials.gov for studies related to disease + location.
    """
    CLINICALTRIALS_BASE = settings.CLINICALTRIALS_BASE_URL
    url = f"{CLINICALTRIALS_BASE}/studies"
    params = {
        "query.cond": disease,
        "query.locn": location if location else None,
        "pageSize": max_results,
        "format": "json",
        "fields": "NCTId,BriefTitle,OverallStatus,Phase,StartDate,CompletionDate,"
                  "BriefSummary,Condition,InterventionName,LocationCity,LocationCountry",
    }
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        studies = resp.json().get("studies", [])
    except Exception as e:
        print(f"ClinicalTrials error: {e}")
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
            "phase": ", ".join(design_module.get("phases", [])),
            "start_date": status_module.get("startDateStruct", {}).get("date", ""),
            "completion_date": status_module.get("completionDateStruct", {}).get("date", ""),
            "summary": desc_module.get("briefSummary", ""),
            "url": f"https://clinicaltrials.gov/study/{id_module.get('nctId', '')}",
        })

    return results
