import os
import csv
import traceback
from datetime import datetime

LOG_DIR = "log"
TRADE_LOG_FILE = os.path.join(LOG_DIR, "trade_log.csv")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")
INFO_LOG_FILE = os.path.join(LOG_DIR, "info.log")

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
    _write_log("ERROR", msg, ERROR_LOG_FILE, include_trace=True)

def log_info(msg):
    _write_log("INFO", msg, INFO_LOG_FILE)

def log_warn(msg):
    _write_log("WARN", msg, INFO_LOG_FILE)

def _write_log(level, msg, file_path, include_trace=False):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, mode="a") as f:
        f.write(f"[{timestamp}] [{level}] {msg}\n")
        if include_trace:
            f.write(traceback.format_exc())
            f.write("\n")
