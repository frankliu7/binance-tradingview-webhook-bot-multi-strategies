import streamlit as st
import pandas as pd
import plotly.express as px
from util import get_total_balance, get_open_position_value
from binance_future import BinanceFutureHttpClient
from config import strategies, get_strategy_config, MAX_TOTAL_POSITION_PCT

import os
from decimal import Decimal

# 初始化 Binance client
binance = BinanceFutureHttpClient(
    api_key=os.getenv("BINANCE_API_KEY"),
    secret=os.getenv("BINANCE_API_SECRET")
)

st.set_page_config(page_title="資金控管 Dashboard", layout="wide")
st.title("📊 資金控管與策略分配")

total_balance = get_total_balance(binance)
total_used = Decimal("0")
data = []

# 遍歷每個策略，計算倉位佔用
for strategy_name in strategies:
    config = get_strategy_config(strategy_name)
    symbol = strategy_name.split("_")[0] + "USDT"
    notional = get_open_position_value(binance, symbol)
    total_used += notional

    data.append({
        "策略名稱": strategy_name,
        "交易對": symbol,
        "佔用資金 USDT": float(notional),
        "設定資金佔比 %": float(config["capital_pct"]) * 100,
        "槓桿倍數": config["leverage"]
    })

df = pd.DataFrame(data)

# 視覺化：圓餅圖（策略佔比）
st.subheader("📈 各策略資金佔用比例（圓餅圖）")
fig = px.pie(df, names="策略名稱", values="佔用資金 USDT", title="策略資金分配")
st.plotly_chart(fig, use_container_width=True)

# 視覺化：總倉位 vs 限制
st.subheader("📉 總體資金使用狀況")
used_pct = (total_used / total_balance * 100).quantize(Decimal("0.01")) if total_balance > 0 else 0
limit_pct = Decimal(str(MAX_TOTAL_POSITION_PCT)) * 100

st.metric("💼 可用資金", f"{float(total_balance - total_used):,.2f} USDT")
st.metric("📊 使用中資金", f"{float(total_used):,.2f} USDT")
st.metric("🚨 使用率", f"{used_pct}% / 限制 {limit_pct}%")

# 長條圖顯示每策略佔用資金
st.subheader("📊 每策略倉位使用狀況（長條圖）")
fig2 = px.bar(df, x="策略名稱", y="佔用資金 USDT", color="策略名稱", text="交易對")
st.plotly_chart(fig2, use_container_width=True)
