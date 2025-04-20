from collections import defaultdict
import time
import hmac
import hashlib
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# === 本地策略倉位追蹤 ===

_position_map = defaultdict(float)

def update_position(strategy_name, action, qty):
    qty = float(qty)
    if action.upper() == "LONG":
        _position_map[strategy_name] += qty
    elif action.upper() == "SHORT":
        _position_map[strategy_name] -= qty
    elif action.upper() == "EXIT":
        _position_map[strategy_name] = 0

def get_position(strategy_name):
    return _position_map[strategy_name]

def get_all_positions():
    return dict(_position_map)

def get_long_short_ratio():
    long_total = sum(v for v in _position_map.values() if v > 0)
    short_total = abs(sum(v for v in _position_map.values() if v < 0))
    total = long_total + short_total
    if total == 0:
        return {"long_pct": 0, "short_pct": 0}
    return {
        "long_pct": round(long_total / total * 100, 2),
        "short_pct": round(short_total / total * 100, 2)
    }

# === Binance Futures 倉位即時查詢（總體風控用） ===

def get_binance_position_summary():
    try:
        api_key = os.getenv("BINANCE_TEST_API_KEY") if os.getenv("USE_TESTNET", "true") == "true" else os.getenv("BINANCE_LIVE_API_KEY")
        secret_key = os.getenv("BINANCE_TEST_API_SECRET") if os.getenv("USE_TESTNET", "true") == "true" else os.getenv("BINANCE_LIVE_API_SECRET")
        base_url = "https://testnet.binancefuture.com" if os.getenv("USE_TESTNET", "true") == "true" else "https://fapi.binance.com"

        ts = int(time.time() * 1000)
        query_string = f"timestamp={ts}"
        signature = hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()

        url = f"{base_url}/fapi/v2/account?{query_string}&signature={signature}"
        headers = {"X-MBX-APIKEY": api_key}
        resp = requests.get(url, headers=headers)

        if resp.status_code != 200:
            return {"error": "API error", "detail": resp.text}

        data = resp.json()
        positions = data.get("positions", [])

        total_long, total_short, unrealized_pnl = 0.0, 0.0, 0.0

        for pos in positions:
            amt = float(pos["positionAmt"])
            notional = float(pos["notional"])
            upnl = float(pos["unrealizedProfit"])
            if amt > 0:
                total_long += notional
            elif amt < 0:
                total_short += abs(notional)
            unrealized_pnl += upnl

        return {
            "total_long": total_long,
            "total_short": total_short,
            "net_position": total_long - total_short,
            "unrealized_pnl": unrealized_pnl
        }
    except Exception as e:
        return {"error": str(e)}
