import requests
from typing import Dict, Any
from config import API_KEY, API_URL_TEMPLATE

class NasaClient:
    def __init__(self, api_key: str = None):
        # Eğer dışarıdan key verilmezse config içindeki API_KEY kullanılır
        self.api_key = api_key or API_KEY
        self.url = API_URL_TEMPLATE.format(api_key=self.api_key)

    def fetch(self, timeout: int = 20) -> Dict[str, Any]:
        """
        NASA InSight API'den veriyi çekip JSON döndürür.
        """
        r = requests.get(self.url, timeout=timeout)
        r.raise_for_status()
        return r.json()
