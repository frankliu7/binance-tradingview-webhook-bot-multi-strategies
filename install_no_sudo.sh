#!/bin/bash
echo "📦 建立 venv..."
/home/master/python/Python-3.9.8/bin/python3 -m venv venv

echo "📦 啟動 venv..."
source venv/bin/activate

echo "📦 安裝依賴模組..."
pip install -r requirements.txt --break-system-packages
