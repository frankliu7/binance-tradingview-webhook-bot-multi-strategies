# performance_tracker.py
import os
import csv
from datetime import datetime
from collections import defaultdict

LOG_DIR = "log"
PERF_FILE = os.path.join(LOG_DIR, "performance_log.csv")
os.makedirs(LOG_DIR, exist_ok=True)

# 暫存每個策略的開倉記錄 {strategy: {"price": ..., "qty": ..., "timestamp": ...}}
_open_trades = defaultdict(dict)

def record_trade(strategy, action, qty, entry_price, timestamp=None):
    """
    記錄每次開倉交易
    """
    if action.upper() not in ["LONG", "SHORT"]:
        return
    _open_trades[strategy] = {
        "side": action.upper(),
        "qty": float(qty),
        "price": float(entry_price),
        "timestamp": timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def record_exit(strategy, qty, exit_price, timestamp=None):
    """
    當平倉時，根據開倉記錄計算損益，並寫入績效紀錄表
    """
    entry = _open_trades.get(strategy)
    if not entry:
        return  # 無對應進場記錄

    pnl = 0
    side = entry["side"]
    entry_price = entry["price"]
    qty = float(qty)
    exit_price = float(exit_price)

    if side == "LONG":
        pnl = (exit_price - entry_price) * qty
    elif side == "SHORT":
        pnl = (entry_price - exit_price) * qty

    duration = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(PERF_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["timestamp", "strategy", "side", "entry_price", "exit_price", "qty", "pnl"])
        writer.writerow([
            duration,
            strategy,
            side,
            entry_price,
            exit_price,
            qty,
            round(pnl, 4)
        ])

    # 平倉後清除該策略的開倉紀錄
    _open_trades.pop(strategy, None)
