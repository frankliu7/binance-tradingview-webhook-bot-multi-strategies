#!/bin/bash

cd $(dirname $0)

echo "📥 更新最新 GitHub 程式碼..."
git pull

if [ ! -d "venv" ]; then
  echo "❌ 尚未建立 venv，請先執行 install_no_sudo.sh"
  exit 1
fi

source venv/bin/activate

echo "📦 重新安裝依賴（如有更新）..."
pip install -r requirements.txt

echo "🔄 重新啟動 bot..."
pkill -f "python main.py" || echo "未偵測到正在運行的 bot，直接啟動"
nohup python main.py > log/bot.log 2>&1 &

echo "✅ 更新並重啟完成！log 輸出中（log/bot.log）"
