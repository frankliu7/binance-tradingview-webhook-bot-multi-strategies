#!/bin/bash

echo "✅ 啟動 Trading Bot Dashboard 中..."

# 啟動 Streamlit 應用
streamlit run dashboard.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false
