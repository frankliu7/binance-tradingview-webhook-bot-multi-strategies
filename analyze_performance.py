import pandas as pd
import numpy as np

# 載入績效檔案
FILE = "log/performance.csv"
df = pd.read_csv(FILE)

# 去除尚未平倉紀錄（無 exit_time）
df = df[df["exit_time"].notna()]

# 新增報酬率欄位
try:
    df["pnl_pct"] = df["pnl_pct"].astype(float)
except:
    df["pnl_pct"] = 0

# 分策略統計
def analyze_strategy_group(group):
    trades = len(group)
    win_trades = group[group["is_win"] == True]
    loss_trades = group[group["is_win"] == False]

    win_rate = len(win_trades) / trades if trades else 0
    avg_win = win_trades["pnl_pct"].mean() if not win_trades.empty else 0
    avg_loss = loss_trades["pnl_pct"].mean() if not loss_trades.empty else 0
    avg_pnl = group["pnl_pct"].mean()
    pnl_std = group["pnl_pct"].std()
    sharpe = avg_pnl / pnl_std if pnl_std else 0

    downside = group[group["pnl_pct"] < 0]["pnl_pct"]
    sortino = avg_pnl / downside.std() if not downside.empty and downside.std() > 0 else 0

    return pd.Series({
        "trades": trades,
        "win_rate": round(win_rate, 3),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2),
        "avg_pnl": round(avg_pnl, 2),
        "sharpe": round(sharpe, 3),
        "sortino": round(sortino, 3)
    })

summary = df.groupby("strategy").apply(analyze_strategy_group)
total = analyze_strategy_group(df)
total.name = "ALL"
summary = pd.concat([summary, total.to_frame().T])

print("\n📊 策略績效統計：")
print(summary)

# 如需輸出 CSV： summary.to_csv("log/strategy_summary.csv")
