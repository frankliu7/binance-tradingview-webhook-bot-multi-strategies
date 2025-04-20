#!/bin/bash

echo "🛑 停止 webhook 主程式..."

# 抓出 main.py 對應的 PID 並 kill
ps aux | grep '[p]ython3 main.py' | awk '{print $2}' | xargs -r kill

echo "✅ 已停止 main.py"
