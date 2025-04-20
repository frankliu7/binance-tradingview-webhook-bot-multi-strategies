#!/bin/bash

echo "▶️ 啟動 Dashboard..."
source venv/bin/activate
mkdir -p log
streamlit run dashboard.py --server.port=8501 --server.address=0.0.0.0 > log/dashboard.log 2>&1 &
echo "✅ Dashboard 已啟動於 http://<your-ip>:8501"
