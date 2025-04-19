# logger.py
import os
import csv
import traceback
from datetime import datetime

LOG_DIR = "log"
TRADE_LOG_FILE = os.path.join(LOG_DIR, "trade_log.csv")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")

os.makedirs(LOG_DIR, exist_ok=True)

def log_trade(strategy_name, action, result):
    try:
        with open(TRADE_LOG_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(["timestamp", "strategy", "action", "price", "qty", "order_id", "status"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                strategy_name,
                action,
                result.get("executed_price"),
                result.get("qty"),
                result.get("order_id"),
                result.get("status")
            ])
    except Exception as e:
        log_error(f"log_trade 錯誤: {e}")

def log_error(msg):
    with open(ERROR_LOG_FILE, mode="a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
        f.write(traceback.format_exc())
        f.write("\n")
