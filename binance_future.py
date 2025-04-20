import os
import time
import hmac
import hashlib
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
BASE_URL = "https://fapi.binance.com"
MAX_TOTAL_LEVERAGE = float(os.getenv("MAX_TOTAL_LEVERAGE", 3.0))

class BinanceFutureHttpClient:
    def __init__(self):
        self.api_key = API_KEY
        self.api_secret = API_SECRET

    def _get_timestamp(self):
        return int(time.time() * 1000)

    def _sign(self, query_string):
        return hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def _headers(self):
        return {"X-MBX-APIKEY": self.api_key}

    def _request(self, method, path, params=None, signed=False):
        url = BASE_URL + path
        if params is None:
            params = {}

        if signed:
            params["timestamp"] = self._get_timestamp()
            query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
            params["signature"] = self._sign(query_string)

        try:
            if method == "GET":
                response = requests.get(url, headers=self._headers(), params=params)
            elif method == "POST":
                response = requests.post(url, headers=self._headers(), params=params)
            else:
                raise ValueError("Unsupported method")
        except Exception as e:
            return {"code": -1, "msg": str(e)}

        if response.status_code != 200:
            return {"code": response.status_code, "msg": response.text}

        return response.json()

    def get_position_info(self):
        return self._request("GET", "/fapi/v2/positionRisk", signed=True)

    def check_total_leverage_limit(self):
        data = self.get_position_info()
        total_leverage = 0.0
        for pos in data:
            amt = float(pos.get("positionAmt", 0))
            if amt == 0:
                continue
            notional = float(pos.get("notional", 0))
            margin = float(pos.get("isolatedMargin", 1)) or 1
            total_leverage += abs(notional / margin)

        if total_leverage > MAX_TOTAL_LEVERAGE:
            print(f"[LeverageLimit] 超出總槓桿限制: {total_leverage:.2f} > {MAX_TOTAL_LEVERAGE}")
            return False
        return True

    def create_order(self, symbol, side, quantity, strategy_name="unknown"):
        if not self.check_total_leverage_limit():
            self.log_order("REJECTED", symbol, side, quantity, strategy_name, reason="Leverage limit exceeded")
            return {"status": "rejected", "reason": "leverage limit exceeded"}

        try:
            data = {
                "symbol": symbol,
                "side": side,
                "type": "MARKET",
                "quantity": quantity,
                "timestamp": self._get_timestamp()
            }
            query_string = '&'.join([f"{k}={v}" for k, v in data.items()])
            signature = self._sign(query_string)
            data["signature"] = signature

            url = BASE_URL + "/fapi/v1/order"
            response = requests.post(url, headers=self._headers(), params=data)

            if response.status_code == 200:
                self.log_order("SUCCESS", symbol, side, quantity, strategy_name)
                return {"status": "success", "order": response.json()}
            else:
                self.log_order("FAILED", symbol, side, quantity, strategy_name, reason=response.text)
                return {"status": "error", "reason": response.text}
        except Exception as e:
            self.log_order("ERROR", symbol, side, quantity, strategy_name, reason=str(e))
            return {"status": "error", "reason": str(e)}

    def log_order(self, status, symbol, side, quantity, strategy_name, reason=""):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"[{now}] [{status}] Strategy: {strategy_name} | Symbol: {symbol} | Side: {side} | Qty: {quantity}"
        if reason:
            msg += f" | Reason: {reason}"
        print(msg)
        with open("order.log", "a") as f:
            f.write(msg + "\n")
