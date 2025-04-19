# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # 讀取 .env 檔案中的變數

strategy_config = {}

# 動態註冊策略預設參數
DEFAULT_STRATEGY_SETTINGS = {
    "enabled": True,
    "exchange": "binance_future",
    "capital_pct": 0.05,
    "max_position_usdt": 200,
    "leverage": 5,
    "trading_volume": 0.01,
    "max_slippage_pct": 0.3
}

def register_strategy(name, symbol):
    if name not in strategy_config:
        strategy_config[name] = DEFAULT_STRATEGY_SETTINGS.copy()
        strategy_config[name]["symbol"] = symbol

# ✅ 示範自動註冊策略（可刪掉）
# register_strategy("BTCUSDT_5m_ATR", "BTCUSDT")

# 從環境變數中讀取私密設定
WEBHOOK_PASSPHRASE = os.getenv("WEBHOOK_PASSPHRASE")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
