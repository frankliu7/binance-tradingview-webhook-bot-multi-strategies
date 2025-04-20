#!/bin/bash

# 安裝目錄與版本
PYTHON_DIR="$HOME/python"
PYTHON_VERSION="3.9.18"
PYTHON_SRC="Python-${PYTHON_VERSION}"
PYTHON_BIN="${PYTHON_DIR}/${PYTHON_SRC}/python"
PIP_BIN="$HOME/.local/bin/pip"

# Step 1: 建立 Python 目錄
mkdir -p $PYTHON_DIR
cd $PYTHON_DIR

# Step 2: 下載 Python 原始碼
if [ ! -d "$PYTHON_SRC" ]; then
    echo "⬇️ 下載 Python ${PYTHON_VERSION}..."
    wget https://www.python.org/ftp/python/${PYTHON_VERSION}/${PYTHON_SRC}.tgz
    tar -xzf ${PYTHON_SRC}.tgz
fi
cd $PYTHON_SRC

# Step 3: 編譯安裝（user local）
echo "🔧 編譯 Python..."
./configure --prefix=$PYTHON_DIR/$PYTHON_SRC --enable-optimizations
make -j4

# Step 4: 安裝 pip（若無）
echo "📦 安裝 pip..."
curl -O https://bootstrap.pypa.io/get-pip.py
./python get-pip.py --user

# Step 5: 建立 venv 虛擬環境
cd $HOME/binance-tradingview-webhook-bot-multi-strategies
$PYTHON_BIN -m venv venv

# Step 6: 啟用虛擬環境並安裝依賴
source venv/bin/activate
echo "📦 安裝 requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ 安裝完成！使用 source venv/bin/activate 啟動虛擬環境"
