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

# ✅ 滑價過大異常統計
st.subheader("🚨 Slippage Alerts")
slip_threshold = 0.5  # 可自定義
if 'slippage_pct' in perf_df.columns:
    slip_abnormal = perf_df[perf_df['slippage_pct'].abs() > slip_threshold]
    if not slip_abnormal.empty:
        st.warning(f"偵測到 {len(slip_abnormal)} 筆滑價超過 ±{slip_threshold}% 的異常交易：")
        st.dataframe(slip_abnormal[['timestamp', 'strategy_name', 'symbol', 'side', 'price', 'slippage_pct']])
    else:
        st.success("無滑價異常紀錄。")
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

# ➕ 報酬 vs 風險分析（Sharpe, Sortino, RR）

st.subheader("📈 Risk-Adjusted Metrics")
st.subheader("📈 Risk-Adjusted Metrics")
try:
    df = perf_df[perf_df['is_entry'] == False]
    grouped = df.groupby('strategy_name')

    risk_df = pd.DataFrame()
    risk_df['mean'] = grouped['pnl_pct'].mean()
    risk_df['std'] = grouped['pnl_pct'].std()
    risk_df['sharpe'] = (risk_df['mean'] / risk_df['std']) * (252**0.5)

    downside_std = grouped['pnl_pct'].apply(lambda x: x[x < 0].std())
    risk_df['sortino'] = (risk_df['mean'] / downside_std) * (252**0.5)

    merged_rr = pd.merge(entries, exits, on='order_id', suffixes=('_entry', '_exit'))
    merged_rr['rr'] = merged_rr['pnl_pct_exit'].abs() / merged_rr['slippage_pct_exit'].abs().replace(0, 1e-6)
    rr_df = merged_rr.groupby('strategy_name_exit')['rr'].mean().reset_index()
    rr_df.columns = ['strategy_name', 'avg_rr']

    risk_df = risk_df.merge(rr_df, on='strategy_name', how='left')
    risk_df = risk_df.reset_index()

    st.dataframe(risk_df[['strategy_name', 'sharpe', 'sortino', 'avg_rr']].round(2))

    # 總體 Sharpe、Sortino、RR
    total_sharpe = (df['pnl_pct'].mean() / df['pnl_pct'].std()) * (252**0.5)
    total_sortino = (df['pnl_pct'].mean() / df[df['pnl_pct'] < 0]['pnl_pct'].std()) * (252**0.5)
    total_avg_rr = merged_rr['rr'].mean()

    st.markdown("---")
    st.subheader("📦 Overall Risk Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Sharpe Ratio", f"{total_sharpe:.2f}")
    col2.metric("Sortino Ratio", f"{total_sortino:.2f}")
    col3.metric("Avg. RR", f"{total_avg_rr:.2f}")

except Exception as e:
    st.warning(f"無法計算 Sharpe / Sortino / RR 指標: {e}")

# ➕ monitor.py API 狀態
try:
    import requests
    st.subheader("🩺 /monitor API Status")
    resp = requests.get("http://localhost:8888/monitor", timeout=5)
    if resp.status_code == 200:
        monitor_data = resp.json()
        st.success("API 回應成功")
        st.json(monitor_data)
    else:
        st.warning(f"/monitor 回應錯誤：{resp.status_code}")
except Exception as e:
    st.warning(f"/monitor API 無法呼叫：{e}")

# ➕ position_tracker 實際倉位
try:
    import position_tracker
    st.subheader("📊 Position Tracker Info")
    pos = position_tracker.get_all_positions()
    st.dataframe(pd.DataFrame(pos))
except Exception as e:
    st.warning(f"無法讀取 position_tracker 倉位資料：{e}")

# ➕ util.py 測試區塊
try:
    import util
    st.subheader("🛠️ Slippage Test Tool")
    mock_entry = 10000
    mock_actual = 10050
    tick_size = 10
    slippage_pct = util.calc_slippage_pct(mock_entry, mock_actual)
    slippage_tick = (mock_actual - mock_entry) / tick_size
    st.code(f"從 TradingView 傳來價格：{mock_entry}
實際成交價格：{mock_actual}
→ 滑價為：{slippage_pct:.2f}% ({slippage_tick:.2f} ticks)")
except Exception as e:
    st.warning(f"無法載入滑價工具：{e}")

# ➕ analyze_performance 額外分析（若存在）
st.subheader("📊 Advanced Performance Analysis")
if os.path.exists("log/analyze_summary.csv"):
    analyze_df = pd.read_csv("log/analyze_summary.csv")
    st.dataframe(analyze_df)
else:
    st.info("尚未產生 analyze_performance 統計報表。")

# 顯示 config 預設設定與總倉風控與個別策略設定
try:
    import config
    st.subheader("⚙️ Config Defaults")
    default_cfg = config.DEFAULT_STRATEGY_CONFIG.copy()
    default_cfg["MAX_TOTAL_POSITION_PCT"] = config.MAX_TOTAL_POSITION_PCT
    st.write(pd.DataFrame(default_cfg.items(), columns=["Parameter", "Value"]))

    st.subheader("📋 Custom Strategy Overrides")
    strategy_df = pd.DataFrame.from_dict(config.STRATEGIES, orient='index')
    strategy_df = strategy_df.fillna('-')
    st.dataframe(strategy_df)
except Exception as e:
    st.warning("無法載入 config.py 設定值，請確認是否存在且無語法錯誤。")

# 額外模組狀態顯示
st.subheader("🧩 Module Insights")

modules = [
    ("config.py", "📘 策略與參數管理", os.path.exists("config.py")),
    ("performance_tracker.py", "📈 績效紀錄模組", os.path.exists("performance_tracker.py")),
    ("position_tracker.py", "📊 倉位追蹤模組", os.path.exists("position_tracker.py")),
    ("monitor.py", "🩺 即時狀態監控 API", os.path.exists("monitor.py")),
    ("util.py", "🛠️ 公用工具/滑價計算等", os.path.exists("util.py")),
    ("analyze_performance.py", "📊 績效進階分析（可選）", os.path.exists("analyze_performance.py"))
]

for path, label, status in modules:
    icon = "✅" if status else "❌"
    st.write(f"{icon} **{label}** ({path})")

# 滑價統計區塊

# 若有 slippage_tick 欄位，加入 tick 表示的統計與圖表
st.subheader("📉 Slippage Analysis")
if 'slippage_pct' in perf_df.columns:
    st.write("平均滑價 (正值為買貴/賣低)：")
    slippage_summary = perf_df.groupby('strategy_name')['slippage_pct'].agg(['mean', 'max', 'count']).reset_index()
    slippage_summary.columns = ['strategy_name', 'avg_slippage_pct', 'max_slippage_pct', 'trades']
    st.dataframe(slippage_summary.round(3))

    st.write("策略平均滑價圖表：")
    fig_slip = px.bar(slippage_summary, x='strategy_name', y='avg_slippage_pct',
                      title='Average Slippage per Strategy (%)', text_auto=True)
    st.plotly_chart(fig_slip, use_container_width=True)
else:
    st.info("未偵測到 slippage_pct 欄位，請確認程式有寫入滑價資訊。")

if 'slippage_tick' in perf_df.columns:
    st.write("策略平均滑價 (以 tick 表示)：")
    slippage_tick_summary = perf_df.groupby('strategy_name')['slippage_tick'].agg(['mean', 'max', 'count']).reset_index()
    slippage_tick_summary.columns = ['strategy_name', 'avg_slippage_tick', 'max_slippage_tick', 'trades']
    st.dataframe(slippage_tick_summary.round(2))

    fig_tick = px.bar(slippage_tick_summary, x='strategy_name', y='avg_slippage_tick',
                      title='Average Slippage per Strategy (ticks)', text_auto=True)
    st.plotly_chart(fig_tick, use_container_width=True)
else:
    st.info("未偵測到 slippage_tick 欄位，請確認程式有寫入 tick 單位滑價。")
st.subheader("📦 Overall Portfolio Performance")
overall_pnl = sum_df['total_pnl_pct'].sum()
total_days = (perf_df['timestamp'].max() - perf_df['timestamp'].min()).days
portfolio_annualized_return = (overall_pnl / max(total_days, 1)) * 365

col_a, col_b = st.columns(2)
with col_a:
    st.metric("💰 Total PnL (All Strategies)", f"{overall_pnl:.2f}%")
with col_b:
    st.metric("📈 Portfolio Annualized Return", f"{portfolio_annualized_return:.2f}%")



# ➕ 新增：strategy_config.json 策略設定總覽
try:
    import config
    import json

    st.subheader("📋 strategy_config.json 設定總覽")

    config_data = config.load_strategy_config()
    if config_data:
        config_df = pd.DataFrame([
            {
                "策略名稱": name,
                "啟用": "✅" if val.get("enabled", True) else "❌",
                "資金比例": val.get("capital_fraction", 0),
                "最大倉位": val.get("max_position", 0),
                "TP1 比例": val.get("qty1", 0),
                "TP2 比例": val.get("qty2", 0),
                "RR1": val.get("rr1", 0),
                "RR2": val.get("rr2", 0)
            }
            for name, val in config_data.items()
        ])
        st.dataframe(config_df)
    else:
        st.info("尚未建立 strategy_config.json 或資料為空")
except Exception as e:
    st.warning(f"無法載入策略設定：{e}")

# ➕ 新增：Binance 倉位追蹤（即時）
try:
    from binance_position_tracker import BinancePositionTracker
    tracker = BinancePositionTracker()
    st.subheader("📡 Binance 即時倉位追蹤")

    summary = tracker.get_position_summary()
    if "error" in summary:
        st.error("無法連線取得 Binance 倉位資訊")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("多單總值", f"${summary['total_long']:.2f}")
        col2.metric("空單總值", f"${summary['total_short']:.2f}")
        col3.metric("浮動損益", f"${summary['unrealized_pnl']:.2f}")
        col4.metric("淨倉位", f"${summary['net_position']:.2f}")
        st.caption(f"更新時間：{pd.to_datetime(summary['timestamp'], unit='ms')}")
except Exception as e:
    st.warning(f"無法取得即時倉位資訊：{e}")

