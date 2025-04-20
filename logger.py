
import os
from datetime import datetime

LOG_DIR = "log"
os.makedirs(LOG_DIR, exist_ok=True)

def _write_log(filename, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(LOG_DIR, filename), "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def log_info(msg):
    _write_log("system.log", f"[INFO] {msg}")

def log_warning(msg):
    _write_log("system.log", f"[WARNING] {msg}")

def log_error(msg):
    _write_log("error.log", f"[ERROR] {msg}")

def log_trade(strategy, action, symbol, price, qty):
    msg = f"Strategy: {strategy} | Action: {action} | Symbol: {symbol} | Price: {price} | Qty: {qty}"
    _write_log("trades.log", msg)
