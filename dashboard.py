import pandas as pd
import streamlit as st
import os

st.set_page_config(page_title="📊 Trading Bot Dashboard", layout="wide")

LOG_FILE = "log/performance.csv"

st.title("📊 策略績效儀表板")

if not os.path.exists(LOG_FILE):
    st.warning("尚未產生績效資料。請先執行交易。")
    st.stop()

# 載入資料
df = pd.read_csv(LOG_FILE)
df = df[df["exit_time"].notna()]
df["exit_time"] = pd.to_datetime(df["exit_time"])
df = df.sort_values("exit_time")

# 顯示基本資料表
with st.expander("📋 交易明細"):
    st.dataframe(df.tail(100), use_container_width=True)

# 計算額外指標
df["holding_secs"] = pd.to_numeric(df["holding_secs"], errors="coerce")
df["rr_ratio"] = df["avg_win"] = df["avg_loss"] = None

def calc_streak(pnls):
    max_win, max_loss = 0, 0
    cur_win, cur_loss = 0, 0
    for pnl in pnls:
        if pnl > 0:
            cur_win += 1
            cur_loss = 0
        elif pnl < 0:
            cur_loss += 1
            cur_win = 0
        else:
            continue
        max_win = max(max_win, cur_win)
        max_loss = max(max_loss, cur_loss)
    return max_win, max_loss

# 分策略統計
def summarize(group):
    win = group[group["pnl_pct"] > 0]["pnl_pct"].mean()
    loss = group[group["pnl_pct"] < 0]["pnl_pct"].mean()
    rr = abs(win / loss) if loss else None
    max_win_streak, max_loss_streak = calc_streak(group["pnl_pct"])
    return pd.Series({
        "trades": len(group),
        "win_rate": round(group["is_win"].sum() / len(group), 2),
        "avg_pnl": group["pnl_pct"].mean(),
        "avg_win": win,
        "avg_loss": loss,
        "avg_hold_sec": group["holding_secs"].mean(),
        "rr_ratio": rr,
        "max_win_streak": max_win_streak,
        "max_loss_streak": max_loss_streak,
        "sharpe": round(group["pnl_pct"].mean() / group["pnl_pct"].std(), 2) if group["pnl_pct"].std() > 0 else 0,
        "sortino": round(group["pnl_pct"].mean() / group[group["pnl_pct"] < 0]["pnl_pct"].std(), 2) if group[group["pnl_pct"] < 0]["pnl_pct"].std() > 0 else 0
    })

summary = df.groupby("strategy").apply(summarize).reset_index()

# 總體統計
overall = summarize(df)
overall["strategy"] = "ALL"
summary = pd.concat([summary, overall.to_frame().T], ignore_index=True)

st.subheader("📈 策略績效統計")
st.dataframe(summary, use_container_width=True)

# 趨勢圖
with st.expander("📈 每筆損益趨勢圖"):
    for strategy in df["strategy"].unique():
        st.write(f"### {strategy}")
        strat_df = df[df["strategy"] == strategy].copy()
        strat_df = strat_df.sort_values("exit_time")
        strat_df["cumsum"] = strat_df["pnl_pct"].cumsum()
        st.line_chart(strat_df.set_index("exit_time")["cumsum"])

# 總體績效趨勢圖
with st.expander("📉 總體 PnL 趨勢圖"):
    all_df = df.copy()
    all_df["cumsum"] = all_df["pnl_pct"].cumsum()
    st.line_chart(all_df.set_index("exit_time")["cumsum"])

# 總體最大回落分析
with st.expander("📉 總體最大回落分析 Drawdown"):
    equity = (df["pnl_pct"].cumsum()).copy()
    highwater = equity.cummax()
    drawdown = equity - highwater
    max_dd = drawdown.min()
    st.metric("最大回落 (Drawdown)", f"{round(max_dd, 2)}%")
    st.line_chart(drawdown.rename("drawdown"))

# 月度盈虧統計
with st.expander("📆 月度盈虧報表"):
    df["month"] = df["exit_time"].dt.to_period("M")
    monthly = df.groupby("month")["pnl_pct"].sum().to_frame().reset_index()
    monthly["month"] = monthly["month"].astype(str)
    st.bar_chart(monthly.set_index("month"))
