
from datetime import datetime
import time

# ✅ 計算滑價百分比
def calc_slippage_pct(entry_price: float, actual_price: float) -> float:
    if entry_price == 0:
        return 0
    return round((actual_price - entry_price) / entry_price * 100, 4)

# ✅ 計算滑價 tick 數
def calc_slippage_tick(entry_price: float, actual_price: float, tick_size: float) -> float:
    if tick_size == 0:
        return 0
    return round((actual_price - entry_price) / tick_size, 2)

# ✅ 計算 webhook 與系統時間的延遲（秒）
def calc_lag_sec(webhook_timestamp: int) -> int:
    now = int(time.time())
    return now - webhook_timestamp

# ✅ 統一解析 webhook payload（含欄位檢查）
def parse_webhook(data: dict) -> dict:
    required_fields = ["strategy_name", "passphrase", "qty", "action", "price"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"缺少必要欄位: {field}")
    return {
        "strategy": data["strategy_name"],
        "symbol": data.get("symbol", ""),
        "exchange": data.get("exchange", "binance"),
        "action": data["action"].lower(),
        "qty": float(data["qty"]),
        "price": float(data["price"]),
        "tp1": float(data.get("tp1", 0)),
        "tp2": float(data.get("tp2", 0)),
        "sl": float(data.get("stop_loss", 0)),
        "qty1": float(data.get("qty1", 0.5)),
        "qty2": float(data.get("qty2", 0.5)),
        "exit": data.get("exit", False),
        "timestamp": int(data.get("timestamp", time.time()))
    }
