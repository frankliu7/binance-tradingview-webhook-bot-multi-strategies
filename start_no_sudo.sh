#!/bin/bash

# 啟動 bot 使用非 sudo 環境下的 Python 環境
cd $(dirname $0)  # 切換到腳本所在的資料夾

if [ ! -d "venv" ]; then
  echo "❌ 找不到 venv，請先執行 install_no_sudo.sh 安裝環境"
  exit 1
fi

source venv/bin/activate

mkdir -p log

echo "[ $(date) ] 啟動 bot" >> log/startup.log
nohup python main.py > log/bot.log 2>&1 &

echo "✅ 已啟動 bot，log 寫入 log/bot.log 中"
echo "使用 tail -f log/bot.log 可查看即時輸出"
