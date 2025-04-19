#!/bin/bash

echo "🔄 更新 Trading Bot 原始碼..."
git pull

echo "🛑 停止交易機器人與 Dashboard..."
./stop.sh
./stop_dashboard.sh

echo "✅ 重新啟動交易機器人與 Dashboard..."
./start.sh
./start_dashboard.sh

echo "🚀 更新與重啟完成！"
