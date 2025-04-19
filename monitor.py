from flask import Blueprint, jsonify
from binance_future import BinanceFutureHttpClient
from config import strategies, get_strategy_config, MAX_TOTAL_POSITION_PCT
from util import get_open_position_value, get_total_balance
from decimal import Decimal
import os

monitor_bp = Blueprint("monitor", __name__)
binance = BinanceFutureHttpClient(
    api_key=os.getenv("BINANCE_API_KEY"),
    secret=os.getenv("BINANCE_API_SECRET")
)

@monitor_bp.route("/monitor", methods=["GET"])
def monitor():
    results = []
    total_used = Decimal("0")
    total_balance = get_total_balance(binance)

    for strategy_name, config_override in strategies.items():
        config = get_strategy_config(strategy_name)
        symbol = strategy_name.split("_")[0] + "USDT"

        used = get_open_position_value(binance, symbol)
        total_used += used

        results.append({
            "strategy": strategy_name,
            "symbol": symbol,
            "capital_pct": config["capital_pct"],
            "leverage": config["leverage"],
            "used_value": float(used)
        })

    percent_used = (total_used / total_balance * 100).quantize(Decimal("0.01")) if total_balance > 0 else 0

    return jsonify({
        "total_balance": float(total_balance),
        "total_used": float(total_used),
        "used_pct": float(percent_used),
        "max_pct_allowed": float(MAX_TOTAL_POSITION_PCT * 100),
        "strategies": results
    })
