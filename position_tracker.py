import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
BASE_URL = "https://fapi.binance.com"

class BinancePositionTracker:
    def __init__(self):
        self.api_key = API_KEY
        self.api_secret = API_SECRET

    def _get_timestamp(self):
        return int(time.time() * 1000)

    def _sign(self, query_string):
        return hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def _headers(self):
        return {"X-MBX-APIKEY": self.api_key}

    def _signed_request(self, endpoint):
        timestamp = self._get_timestamp()
        query_string = f"timestamp={timestamp}"
        signature = self._sign(query_string)
        url = f"{BASE_URL}{endpoint}?{query_string}&signature={signature}"

        try:
            response = requests.get(url, headers=self._headers())
            if response.status_code != 200:
                print(f"[BinancePositionTracker] Error: {response.status_code} - {response.text}")
                return None
            return response.json()
        except Exception as e:
            print(f"[BinancePositionTracker] Exception: {e}")
            return None

    def get_position_summary(self):
        data = self._signed_request("/fapi/v2/account")
        if not data:
            return {"error": "API failure"}

        positions = data.get("positions", [])
        total_long = 0.0
        total_short = 0.0
        unrealized_pnl = 0.0

        for pos in positions:
            amt = float(pos.get("positionAmt", 0))
            if amt == 0:
                continue
            notional = float(pos.get("notional", 0))
            upnl = float(pos.get("unrealizedProfit", 0))
            unrealized_pnl += upnl

            if amt > 0:
                total_long += notional
            elif amt < 0:
                total_short += abs(notional)

        return {
            "total_long": total_long,
            "total_short": total_short,
            "unrealized_pnl": unrealized_pnl,
            "net_position": total_long - total_short,
            "timestamp": int(time.time() * 1000)
        }
