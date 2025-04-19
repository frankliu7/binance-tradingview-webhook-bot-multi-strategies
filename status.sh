#!/bin/bash

echo "📊 交易機器人執行狀態："

PID=$(pgrep -f "python main.py")

if [ -z "$PID" ]; then
  echo "❌ bot 未在運行中"
else
  echo "✅ bot 運行中 (PID: $PID)"
  ps -p $PID -o pid,etime,cmd
fi
