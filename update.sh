#!/bin/bash

echo "⬇️ 拉取最新 Git 程式碼..."
git pull

echo "📦 安裝 / 更新相依套件..."
source venv/bin/activate
pip install -r requirements.txt

echo "🔄 重啟主程式與 Dashboard..."
bash restart.sh

echo "✅ 更新完成！主程式與 Dashboard 均已重啟。"
