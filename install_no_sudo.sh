#!/bin/bash
echo "📦 建立虛擬環境..."
python3 -m venv venv

echo "📦 啟動虛擬環境..."
source venv/bin/activate

echo "📦 安裝依賴模組..."
pip install -r requirements.txt --break-system-packages
