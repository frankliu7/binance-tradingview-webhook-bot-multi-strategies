#!/bin/bash
set -e

echo "📦 準備 Python 安裝路徑..."
mkdir -p ~/python
cd ~/python

# 安裝 Python（如尚未安裝）
if [ ! -d "Python-3.9.8" ]; then
  echo "🔽 下載 Python 3.9.8 原始碼..."
  wget https://www.python.org/ftp/python/3.9.8/Python-3.9.8.tgz
  tar xzf Python-3.9.8.tgz
  cd Python-3.9.8
  echo "🔧 編譯安裝 Python..."
  ./configure --prefix=$HOME/python/Python-3.9.8 --enable-optimizations
  make -j4
  make install
  cd ..
else
  echo "✅ Python 3.9.8 已存在，略過安裝。"
fi

PYTHON_BIN=$HOME/python/Python-3.9.8/bin/python3

echo "🐍 Python 路徑：$PYTHON_BIN"
echo "🧪 建立虛擬環境..."
$PYTHON_BIN -m ensurepip --upgrade
$PYTHON_BIN -m pip install --upgrade pip setuptools wheel
$PYTHON_BIN -m pip install virtualenv

if [ ! -d "venv" ]; then
  $PYTHON_BIN -m virtualenv venv
else
  echo "✅ venv 已存在"
fi

echo "✅ 啟動虛擬環境並安裝依賴..."
source venv/bin/activate
pip install -r requirements.txt

echo "🎉 安裝完成！請執行："
echo "source venv/bin/activate"
