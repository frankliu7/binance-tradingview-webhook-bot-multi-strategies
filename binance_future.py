import requests
import time
import hmac
import hashlib
from threading import Lock
from datetime import datetime
from decimal import Decimal
import json

from .constant import RequestMethod, Interval, OrderSide, OrderType


class BinanceFutureHttpClient(object):

    def __init__(self, api_key=None, secret=None, timeout=5):
        self.key = api_key
        self.secret = secret
        self.host = "https://fapi.binance.com"
        self.recv_window = 5000
        self.timeout = timeout
        self.order_count_lock = Lock()
        self.order_count = 1_000_000

    def build_parameters(self, params: dict):
        keys = list(params.keys())
        keys.sort()
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
        if response.status_code == 200:
            return response.status_code, response.json()
        else:
            try:
                return response.status_code, json.loads(response.text)
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

    def place_order(self, symbol: str, order_side: OrderSide, order_type: OrderType, quantity: Decimal, price: Decimal,
                    time_inforce="GTC", client_order_id=None, recvWindow=5000, stop_price=0):

        path = '/fapi/v1/order'

        if client_order_id is None:
            client_order_id = self.get_client_order_id()

        params = {
            "symbol": symbol,
            "side": order_side.value,
            "type": 'LIMIT',
            "quantity": quantity,
            "price": price,
            "recvWindow": recvWindow,
            "timestamp": self._timestamp(),
            "newClientOrderId": client_order_id
        }

        if order_type == OrderType.LIMIT:
            params['type'] = 'LIMIT'
            params['timeInForce'] = time_inforce
        elif order_type == OrderType.MARKET:
            if params.get('price', None):
                del params['price']
        elif order_type == OrderType.MAKER:
            params['type'] = 'LIMIT'
            params['timeInForce'] = "GTX"
        elif order_type == OrderType.STOP:
            if stop_price > 0:
                params["stopPrice"] = stop_price
            else:
                raise ValueError("stopPrice must greater than 0")

        return self.request(RequestMethod.POST, path=path, requery_dict=params, verify=True)

    def get_order(self, symbol, client_order_id=None):
        path = "/fapi/v1/order"
        query_dict = {"symbol": symbol, "timestamp": self._timestamp()}
        if client_order_id:
            query_dict["origClientOrderId"] = client_order_id
        return self.request(RequestMethod.GET, path, query_dict, verify=True)

    def cancel_order(self, symbol, client_order_id=None):
        path = "/fapi/v1/order"
        params = {"symbol": symbol, "timestamp": self._timestamp()}
        if client_order_id:
            params["origClientOrderId"] = client_order_id
        return self.request(RequestMethod.DELETE, path, params, verify=True)

    def exchangeInfo(self):
        path = '/fapi/v1/exchangeInfo'
        return self.request(req_method=RequestMethod.GET, path=path)

    def get_balance(self):
        path = "/fapi/v1/balance"
        params = {"timestamp": self._timestamp()}
        return self.request(RequestMethod.GET, path=path, requery_dict=params, verify=True)

    def get_account_info(self):
        path = "/fapi/v1/account"
        params = {"timestamp": self._timestamp()}
        return self.request(RequestMethod.GET, path, params, verify=True)

    def get_position_info(self, symbol):
        path = "/fapi/v2/positionRisk"
        params = {"timestamp": self._timestamp(), "symbol": symbol}
        return self.request(RequestMethod.GET, path, params, verify=True)

    # ✅ 新增：查最大槓桿
    def get_max_leverage(self, symbol: str) -> int:
        status, data = self.exchangeInfo()
        if status != 200:
            return 20  # fallback

        for item in data.get("symbols", []):
            if item["symbol"] == symbol:
                try:
                    # Binance 實際上沒標出最大槓桿，視為最高為 125
                    return 125
                except:
                    break
        return 20  # fallback 預設值

    # ✅ 新增：設定槓桿
    def set_leverage(self, symbol: str, leverage: int = 20):
        path = "/fapi/v1/leverage"
        params = {
            "symbol": symbol,
            "leverage": leverage,
            "timestamp": self._timestamp()
        }
        return self.request(RequestMethod.POST, path, requery_dict=params, verify=True)
