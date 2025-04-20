import requests
import time
import hmac
import hashlib
from threading import Lock
from datetime import datetime
from decimal import Decimal
import json

from enum import Enum

class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"

class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    MAKER = "MAKER"
    STOP = "STOP"

class BinanceFutureHttpClient:
    host = "https://fapi.binance.com"  # 預設為正式環境，config 可改 testnet

    def __init__(self, api_key=None, secret=None, timeout=5):
        self.key = api_key
        self.secret = secret
        self.recv_window = 5000
        self.timeout = timeout
        self.order_count_lock = Lock()
        self.order_count = 1_000_000

    def build_parameters(self, params: dict):
        keys = sorted(params.keys())
        return '&'.join([f"{key}={params[key]}" for key in keys])

    def request(self, req_method: RequestMethod, path: str, requery_dict=None, verify=False):
        url = self.host + path

        if verify:
            query_str = self._sign(requery_dict)
            url += '?' + query_str
        elif requery_dict:
            url += '?' + self.build_parameters(requery_dict)
        headers = {"X-MBX-APIKEY": self.key}

        response = requests.request(req_method.value, url=url, headers=headers, timeout=self.timeout)
        try:
            return response.status_code, response.json()
        except Exception as error:
            return response.status_code, {"msg": response.text, 'error': str(error)}

    def _timestamp(self):
        return int(time.time() * 1000)

    def _sign(self, params):
        requery_string = self.build_parameters(params)
        hexdigest = hmac.new(self.secret.encode('utf8'), requery_string.encode("utf-8"), hashlib.sha256).hexdigest()
        return requery_string + '&signature=' + str(hexdigest)

    def get_client_order_id(self):
        with self.order_count_lock:
            self.order_count += 1
            return "x-cLbi5uMH" + str(self._timestamp()) + str(self.order_count)

    def get_latest_price(self, symbol):
        return self.request(RequestMethod.GET, "/fapi/v1/ticker/price", {"symbol": symbol})

    def get_position_info(self, symbol):
        return self.request(RequestMethod.GET, "/fapi/v2/positionRisk", {"timestamp": self._timestamp(), "symbol": symbol}, verify=True)

    def get_balance(self):
        return self.request(RequestMethod.GET, "/fapi/v1/balance", {"timestamp": self._timestamp()}, verify=True)

    def get_account_info(self):
        return self.request(RequestMethod.GET, "/fapi/v1/account", {"timestamp": self._timestamp()}, verify=True)

    def set_leverage(self, symbol, leverage):
        path = "/fapi/v1/leverage"
        params = {
            "symbol": symbol,
            "leverage": leverage,
            "timestamp": self._timestamp()
        }
        return self.request(RequestMethod.POST, path, requery_dict=params, verify=True)

    def get_max_leverage(self, symbol):
        code, data = self.request(RequestMethod.GET, "/fapi/v1/exchangeInfo")
        if code != 200:
            return None
        for s in data["symbols"]:
            if s["symbol"] == symbol:
                for f in s.get("filters", []):
                    if f.get("filterType") == "LEVERAGE":
                        return int(f["maxLeverage"])
        return None

    def place_market_order(self, symbol: str, side: str, quantity: float):
        path = "/fapi/v1/order"
        params = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": quantity,
            "timestamp": self._timestamp(),
            "newClientOrderId": self.get_client_order_id()
        }
        return self.request(RequestMethod.POST, path, requery_dict=params, verify=True)

    def close_position(self, symbol: str, position_side: str):
        path = "/fapi/v1/order"
        side = "SELL" if position_side == "LONG" else "BUY"
        qty = self._get_position_qty(symbol)
        if qty == 0:
            return 400, {"msg": "No open position to close."}
        params = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": qty,
            "timestamp": self._timestamp(),
            "reduceOnly": True
        }
        return self.request(RequestMethod.POST, path, requery_dict=params, verify=True)

    def _get_position_qty(self, symbol: str):
        code, data = self.get_position_info(symbol)
        if code == 200:
            for pos in data:
                if pos["symbol"] == symbol and float(pos["positionAmt"]) != 0:
                    return abs(float(pos["positionAmt"]))
        return 0
