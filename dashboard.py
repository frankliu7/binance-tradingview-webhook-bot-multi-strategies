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

# 顯示基本資料表
with st.expander("📋 交易明細"):
    st.dataframe(df.tail(100), use_container_width=True)

# 分策略統計
summary = df.groupby("strategy").agg(
    trades=("pnl_pct", "count"),
    win_rate=("is_win", lambda x: round(x.sum() / len(x), 2)),
    avg_pnl=("pnl_pct", "mean"),
    avg_win=("pnl_pct", lambda x: x[x>0].mean()),
    avg_loss=("pnl_pct", lambda x: x[x<0].mean()),
    sharpe=("pnl_pct", lambda x: round(x.mean() / x.std(), 2) if x.std() > 0 else 0),
    sortino=("pnl_pct", lambda x: round(x.mean() / x[x<0].std(), 2) if x[x<0].std() > 0 else 0)
).reset_index()

# 加入總體統計
all_stats = pd.Series({
    "strategy": "ALL",
    "trades": len(df),
    "win_rate": round(df["is_win"].sum() / len(df), 2),
    "avg_pnl": df["pnl_pct"].mean(),
    "avg_win": df[df["pnl_pct"] > 0]["pnl_pct"].mean(),
    "avg_loss": df[df["pnl_pct"] < 0]["pnl_pct"].mean(),
    "sharpe": round(df["pnl_pct"].mean() / df["pnl_pct"].std(), 2) if df["pnl_pct"].std() > 0 else 0,
    "sortino": round(df["pnl_pct"].mean() / df[df["pnl_pct"] < 0]["pnl_pct"].std(), 2) if df[df["pnl_pct"] < 0]["pnl_pct"].std() > 0 else 0
})
summary = pd.concat([summary, all_stats.to_frame().T], ignore_index=True)

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
    all_df = df.sort_values("exit_time").copy()
    all_df["cumsum"] = all_df["pnl_pct"].cumsum()
    st.line_chart(all_df.set_index("exit_time")["cumsum"])
