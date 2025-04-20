#!/bin/bash

echo "🔧 建立虛擬環境..."
python3 -m venv venv

if [ ! -f "venv/bin/activate" ]; then
    echo "❌ 虛擬環境建立失敗，請確認 python3 是否存在"
    exit 1
fi

echo "✅ 啟動虛擬環境..."
source venv/bin/activate

echo "📦 安裝依賴模組..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ 安裝完成！"
echo "▶️ 請執行：bash start.sh 啟動主程式"
