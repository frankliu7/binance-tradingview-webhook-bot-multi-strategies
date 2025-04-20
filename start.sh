#!/bin/bash

echo "▶️ 啟動主程式..."
source venv/bin/activate
nohup python3 main.py > log/bot.log 2>&1 &

echo "▶️ 啟動 Dashboard..."
nohup streamlit run dashboard.py --server.port=8501 --server.address=0.0.0.0 > log/dashboard.log 2>&1 &

echo "✅ 主程式與 Dashboard 均已啟動"
