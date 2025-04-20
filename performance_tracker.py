import csv
from datetime import datetime
import os

PERFORMANCE_LOG = "log/performance.csv"
os.makedirs("log", exist_ok=True)

# 初始化欄位
if not os.path.exists(PERFORMANCE_LOG):
    with open(PERFORMANCE_LOG, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",         # webhook 進場時間
            "strategy",          # 策略名稱
            "symbol",            # 幣種
            "action",            # long / short / exit
            "side",              # BUY / SELL
            "entry_price",       # webhook 發送價格
            "market_price",      # 實際成交價格
            "quantity",          # 下單量
            "tp1", "tp2", "stop_loss",  # 固定止盈止損
            "slippage_pct",      # 滑價百分比
            "lag_sec",           # webhook timestamp 延遲秒數
            "exit_time",         # 出場時間（若 exit webhook）
            "holding_secs",      # 持倉時間（若 exit webhook）
            "pnl_pct",           # 損益百分比
            "tp_hit",            # 命中哪一段止盈（tp1/tp2/none）
            "is_win"             # 是否為獲利交易
        ])

def record_trade(data: dict):
    with open(PERFORMANCE_LOG, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.utcnow().isoformat(),
            data.get("strategy"),
            data.get("symbol"),
            data.get("action"),
            data.get("side", ""),  # BUY / SELL
            data.get("price"),
            data.get("executed_price", data.get("price")),
            data.get("qty"),
            data.get("tp1", ""),
            data.get("tp2", ""),
            data.get("stop_loss", ""),
            round(data.get("slippage_pct", 0), 4),
            data.get("lag_sec", ""),
            data.get("exit_time", ""),
            data.get("holding_secs", ""),
            data.get("pnl_pct", ""),
            data.get("tp_hit", ""),
            data.get("is_win", "")
        ])
