import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Trading Bot Dashboard", layout="wide")

# 檔案路徑
PERF_PATH = "log/performance.csv"

# 標題區塊
st.title("📊 Trading Strategy Performance Dashboard")

# 載入績效資料
if not os.path.exists(PERF_PATH):
    st.warning("尚未偵測到績效資料，請先執行交易策略...")
    st.stop()

perf_df = pd.read_csv(PERF_PATH)
perf_df['timestamp'] = pd.to_datetime(perf_df['timestamp'], unit='s')
perf_df['date'] = perf_df['timestamp'].dt.date

# 資金視覺化（策略佔用比例）
st.subheader("📈 Capital Allocation by Strategy")
latest_entries = perf_df.sort_values('timestamp').drop_duplicates('strategy_name', keep='last')
latest_entries = latest_entries[latest_entries['is_entry'] == True]

if not latest_entries.empty:
    cap_df = latest_entries.groupby('strategy_name').agg({
        'notional': 'sum',
        'leverage': 'last'
    }).reset_index()
    cap_df['adjusted_exposure'] = cap_df['notional'] * cap_df['leverage']

    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(cap_df, names='strategy_name', values='adjusted_exposure',
                     title='🧮 Adjusted Exposure (Notional × Leverage)')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.bar(cap_df, x='strategy_name', y='leverage',
                     title='⚙️ Actual Leverage per Strategy', text_auto=True)
        st.plotly_chart(fig2, use_container_width=True)

    # 加入總倉佔比限制視覺化
    total_exposure = cap_df['adjusted_exposure'].sum()
    available_pct = max(0, 1 - total_exposure / (cap_df['adjusted_exposure'].sum() / cap_df['capital_pct'].mean()))
    st.metric("🔒 Total Portfolio Usage", f"{total_exposure:.2f} USDT", help="Sum of all adjusted notional exposures")
else:
    st.info("尚未有任何持倉紀錄...")

# 最新交易明細
df_recent = perf_df.sort_values('timestamp', ascending=False).head(30)
st.subheader("🧾 Recent Trades")
st.dataframe(df_recent[['timestamp', 'strategy_name', 'symbol', 'side', 'price', 'qty', 'pnl_pct', 'duration_sec']])

# 各策略績效統計
st.subheader("📊 Strategy Performance Summary")
summary = perf_df[perf_df['is_entry'] == False].groupby('strategy_name').agg({
    'pnl_pct': ['mean', 'sum', 'count'],
    'duration_sec': 'mean'
})
sum_df = summary.copy()
sum_df.columns = ['avg_pnl_pct', 'total_pnl_pct', 'trades', 'avg_holding_time_sec']

# 加入勝率計算
entries = perf_df[perf_df['is_entry'] == True]
exits = perf_df[perf_df['is_entry'] == False]
merged = pd.merge(entries, exits, on='order_id', suffixes=('_entry', '_exit'))
merged['win'] = merged['pnl_pct_exit'] > 0
winrate_df = merged.groupby('strategy_name_exit')['win'].mean().reset_index()
winrate_df.columns = ['strategy_name', 'win_rate']

sum_df = sum_df.merge(winrate_df, on='strategy_name', how='left')
sum_df['win_rate'] = (sum_df['win_rate'] * 100).round(2)
sum_df['start_date'] = perf_df.groupby('strategy_name')['timestamp'].min()
sum_df['end_date'] = perf_df.groupby('strategy_name')['timestamp'].max()
sum_df['days_active'] = (sum_df['end_date'] - sum_df['start_date']).dt.days.clip(lower=1)
sum_df['annualized_return_pct'] = (sum_df['total_pnl_pct'] / sum_df['days_active']) * 365

# 排序顯示
sum_df = sum_df.sort_values('annualized_return_pct', ascending=False)

st.dataframe(sum_df[['avg_pnl_pct', 'total_pnl_pct', 'annualized_return_pct', 'win_rate', 'trades', 'avg_holding_time_sec']].round(2))

# ➕ 總體績效分析
st.subheader("📦 Overall Portfolio Performance")
overall_pnl = sum_df['total_pnl_pct'].sum()
total_days = (perf_df['timestamp'].max() - perf_df['timestamp'].min()).days
portfolio_annualized_return = (overall_pnl / max(total_days, 1)) * 365

col_a, col_b = st.columns(2)
with col_a:
    st.metric("💰 Total PnL (All Strategies)", f"{overall_pnl:.2f}%")
with col_b:
    st.metric("📈 Portfolio Annualized Return", f"{portfolio_annualized_return:.2f}%")
