#!/bin/bash

echo "♻️ 正在重啟 Trading Bot 與 Dashboard..."

./stop.sh
./stop_dashboard.sh

./start.sh
./start_dashboard.sh

echo "✅ 已完成重啟！"
