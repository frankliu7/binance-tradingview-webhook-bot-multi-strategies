# monitor.py
import time
from decimal import Decimal
from config import strategy_config
from util import get_position_amount
from api.binance_future import BinanceFutureHttpClient
from config import API_KEY, API_SECRET

# 用於查詢倉位與組合狀態
client = BinanceFutureHttpClient(api_key=API_KEY, secret=API_SECRET)

# 暫存滑價異常紀錄
_slippage_alerts = {}

def record_slippage_alert(strategy_name, result):
    _slippage_alerts[strategy_name] = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "slippage_pct": result.get("slippage_pct"),
        "signal_price": result.get("signal_price"),
        "executed_price": result.get("executed_price"),
        "order_id": result.get("order_id")
    }

def get_monitor_status():
    status = {}
    for strategy, cfg in strategy_config.items():
        symbol = cfg["symbol"]
        enabled = cfg.get("enabled", True)
        capital_pct = cfg.get("capital_pct", 0)
        max_usdt = cfg.get("max_position_usdt", 0)
        leverage = cfg.get("leverage", 1)
        max_slippage_pct = cfg.get("max_slippage_pct", 0.5)

        # 查詢實際倉位
        position_amt = get_position_amount(client, symbol)

        # 加入狀態輸出
        status[strategy] = {
            "enabled": enabled,
            "symbol": symbol,
            "capital_pct": capital_pct,
            "max_position_usdt": max_usdt,
            "leverage": leverage,
            "current_position": position_amt,
            "max_slippage_pct": max_slippage_pct,
            "slippage_alert": _slippage_alerts.get(strategy, None)
        }

    return status
