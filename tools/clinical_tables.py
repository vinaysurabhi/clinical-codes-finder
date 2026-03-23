import requests
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_URL = "https://clinicaltables.nlm.nih.gov/api"


def query_clinical_tables(
    endpoint: str,
    search_term: str,
    max_results: int = 5,
    extra_params: Optional[dict] = None
) -> List[dict]:
    """
    Generic NLM Clinical Tables API query.
    
    Args:
        endpoint: API path, e.g. 'icd10cm/v3/search'
        search_term: The clinical term to search for
        max_results: Max number of results to return
        extra_params: Additional query parameters
    
    Returns:
        List of result dicts with 'code', 'display', and optional metadata
    """
    params = {
        "terms": search_term,
        "maxList": max_results,
        "df": "",   # display fields
    }
    if extra_params:
        params.update(extra_params)

    url = f"{BASE_URL}/{endpoint}"
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        logger.error(f"API call to {url} failed: {e}")
        return []
