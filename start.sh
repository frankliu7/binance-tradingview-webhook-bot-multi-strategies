#!/bin/bash

echo "🔧 建立 log 資料夾..."
mkdir -p log

echo "📦 建立虛擬環境（如果尚未存在）..."
python3 -m venv venv

echo "🔁 啟動虛擬環境..."
source venv/bin/activate

echo "📦 安裝依賴模組..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ 啟動交易機器人中..."
echo "[ $(date) ] Starting trading bot..." >> log/startup.log
nohup python3 main.py > log/bot.log 2>&1 &

echo "🎉 啟動完成！請用 tail -f log/bot.log 查看日誌。"
