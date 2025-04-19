#!/bin/bash

echo "🔄 更新 Trading Bot 原始碼..."
git pull

echo "🛠 重新啟動 Dashboard..."
./stop_dashboard.sh
./start_dashboard.sh

echo "✅ 更新完成，Dashboard 已重啟！"
