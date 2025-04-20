#!/bin/bash

echo "⬇️ 拉取最新 Git 程式碼..."
git pull

echo "📁 切換到虛擬環境..."
source venv/bin/activate || { echo "❌ 找不到 venv，請先執行 install_no_sudo.sh 建立環境"; exit 1; }

echo "📦 安裝 / 更新相依套件..."
pip install -r requirements.txt --quiet

echo "🔄 重啟主程式與 Dashboard..."
bash restart.sh

echo "✅ 更新完成！主程式與 Dashboard 均已重啟。"
