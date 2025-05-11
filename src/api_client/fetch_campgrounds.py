import requests
from typing import List, Dict, Any

API_URL = (
    "https://thedyrt.com/api/v6/campground-search-results?"
    "filter%5Bsearch%5D%5Bbooking-method%5D=ridb&"
    "filter%5Bsearch%5D%5Brecommended%5D=1&"
    "filter%5Bsearch%5D%5Borigin%5D=32.82%2C39.94&"
    "page%5Bnumber%5D={page}&page%5Bsize%5D={size}"
)

def fetch_campgrounds(page: int = 1, size: int = 10) -> List[Dict[str, Any]]:
    """
    API'den kamp alanı verilerini çeker.
    """
    url = API_URL.format(page=page, size=size)
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("data", []) 