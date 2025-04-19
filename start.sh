#!/bin/bash

# 建立 log 資料夾（若尚未存在）
mkdir -p log

# 紀錄啟動時間到 startup log
echo "[ $(date) ] Starting trading bot..." >> log/startup.log

# 背景執行主程式，將 stdout 與 stderr 寫入 log 檔
nohup python3 main.py > log/bot.log 2>&1 &
