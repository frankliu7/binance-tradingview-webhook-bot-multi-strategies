#!/bin/bash

echo "🛑 停止主程式..."
ps aux | grep '[p]ython3 main.py' | awk '{print $2}' | xargs -r kill

echo "🛑 停止 Dashboard..."
ps aux | grep '[s]treamlit run dashboard.py' | awk '{print $2}' | xargs -r kill

echo "✅ 已全部停止"
