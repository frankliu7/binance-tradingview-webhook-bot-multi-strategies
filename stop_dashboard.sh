#!/bin/bash

echo "🛑 嘗試停止 Streamlit Dashboard..."

# 尋找並終止執行中的 streamlit 程序
pids=$(ps aux | grep 'streamlit run dashboard.py' | grep -v grep | awk '{print $2}')

if [ -z "$pids" ]; then
    echo "⚠️ 沒有找到正在執行的 Dashboard。"
else
    kill $pids
    echo "✅ Dashboard 已成功停止 (PID: $pids)"
fi
