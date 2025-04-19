import csv
from datetime import datetime
import os

PERFORMANCE_LOG = "log/performance.csv"

# 確保 log 資料夾存在
os.makedirs("log", exist_ok=True)

# 初始表頭（僅首次寫入）
if not os.path.exists(PERFORMANCE_LOG):
    with open(PERFORMANCE_LOG, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "strategy", "symbol", "action", "side", "entry_price", "market_price",
            "quantity", "tp1", "tp2", "stop_loss", "slippage_pct"
        ])

def record_trade(strategy, symbol, action, side, entry_price, market_price, qty, tp1, tp2, sl, slippage_pct):
    with open(PERFORMANCE_LOG, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.utcnow().isoformat(),
            strategy,
            symbol,
            action,
            side,
            entry_price,
            market_price,
            qty,
            tp1,
            tp2,
            sl,
            round(slippage_pct, 4)
        ])
