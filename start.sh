#!/bin/bash

# 進入當前目錄
cd "$(dirname "$0")"

# 啟動 venv（虛擬環境）
if [ ! -d "venv" ]; then
    echo "❌ venv not found. 請先執行 install_no_sudo.sh 來安裝環境"
    exit 1
fi

source venv/bin/activate

# 啟動主程式（Webhook 接收）
echo "🚀 啟動主程式 webhook..."
nohup python3 main.py > log/bot.log 2>&1 &

echo "✅ 主程式啟動完成！log 寫入 log/bot.log"
