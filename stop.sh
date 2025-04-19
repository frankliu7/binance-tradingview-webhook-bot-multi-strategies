#!/bin/bash

echo "🛑 正在停止交易機器人..."

PID=$(pgrep -f "python main.py")

if [ -z "$PID" ]; then
  echo "⚠️ 找不到正在運行的 bot。無需停止。"
else
  kill $PID
  echo "✅ 已停止 bot (PID: $PID)"
fi
