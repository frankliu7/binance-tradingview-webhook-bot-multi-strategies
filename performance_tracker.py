import csv
from datetime import datetime
import os

PERFORMANCE_LOG = "log/performance.csv"

os.makedirs("log", exist_ok=True)

if not os.path.exists(PERFORMANCE_LOG):
    with open(PERFORMANCE_LOG, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "strategy", "symbol", "action", "side", "entry_price", "market_price",
            "quantity", "tp1", "tp2", "stop_loss", "slippage_pct",
            "exit_time", "holding_secs", "pnl_pct", "tp_hit", "is_win"
        ])

def record_trade(strategy, symbol, action, side, entry_price, market_price, qty, tp1, tp2, sl, slippage_pct, extra=None):
    extra = extra or {}
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
            round(slippage_pct, 4),
            extra.get("exit_time", ""),
            extra.get("holding_secs", ""),
            extra.get("pnl_pct", ""),
            extra.get("tp_hit", ""),
            extra.get("is_win", "")
        ])
