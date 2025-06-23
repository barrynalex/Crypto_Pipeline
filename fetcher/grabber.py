import requests
import time
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class CryptoFetcher:
    def __init__(self, base_url: str = "https://api.coingecko.com/api/v3"):
        self.base_url = base_url

    def _request(self, url: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        url = f"{self.base_url}{url}"
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch data: {e}")
            return []


    def get_coin_list(self) -> List[str]:
        url = "/coins/list"
        
        return self._request(url)

    def fetch_market_data(
        self,
        vs_currency: str = "usd",
        symbols: List[str] = ["btc", "eth", "ada"],
        per_page: int = 100,
        page: int = 1
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch market data from CoinGecko.
        """
        url = "/coins/markets"
        params = {
            "vs_currency": vs_currency,
            "symbols": ",".join(symbols),
            "order": "market_cap_desc",
            "per_page": per_page,
            "page": page,
            "sparkline": False
        }

        return self._request(url, params)

if __name__ == "__main__":
    fetcher = CryptoFetcher()
    # symbols = ["bitcoin", "ethereum", "solana"]
    data = fetcher.fetch_market_data()

    if data:
        for coin in data:
            print({
                "id": coin.get("id"),
                "symbol": coin.get("symbol"),
                "current_price": coin.get("current_price"),
                "market_cap": coin.get("market_cap"),
                "volume": coin.get("total_volume"),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
