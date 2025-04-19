#!/bin/bash

set -e

PYTHON_VERSION=3.9.8
PYTHON_DIR="$HOME/python/python-$PYTHON_VERSION"

echo "🔧 建立 Python 安裝資料夾..."
mkdir -p ~/python && cd ~/python

if [ ! -f Python-$PYTHON_VERSION.tgz ]; then
    echo "⬇️ 下載 Python $PYTHON_VERSION..."
    wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz
fi

echo "📦 解壓 Python 原始碼..."
tar -xvzf Python-$PYTHON_VERSION.tgz && cd Python-$PYTHON_VERSION

echo "⚙️ 編譯並安裝 Python 到 $PYTHON_DIR..."
./configure --prefix=$PYTHON_DIR --enable-optimizations
make -j 2
make install

cd $HOME/binance-tradingview-webhook-bot-multi-strategies

echo "📦 安裝 virtualenv（如果尚未存在）..."
~/.local/bin/pip3 install --user virtualenv || pip3 install --user virtualenv

echo "📦 建立虛擬環境..."
~/.local/bin/virtualenv --python=$PYTHON_DIR/bin/python3 venv

echo "✅ 啟動虛擬環境並安裝依賴..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "🎉 安裝完成！執行如下指令來啟動機器人："
echo ""
echo "  source venv/bin/activate"
echo "  python main.py"
