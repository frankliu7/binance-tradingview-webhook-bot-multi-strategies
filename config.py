# ✅ config.py（已優化，參數來自 .env）

import os
from dotenv import load_dotenv

# 載入 .env 檔
load_dotenv()

# ✅ 讀取環境變數：選擇 API 金鑰來源
USE_TESTNET = os.getenv("USE_TESTNET", "true").lower() == "true"

API_KEY = os.getenv("BINANCE_TEST_API_KEY") if USE_TESTNET else os.getenv("BINANCE_LIVE_API_KEY")
API_SECRET = os.getenv("BINANCE_TEST_API_SECRET") if USE_TESTNET else os.getenv("BINANCE_LIVE_API_SECRET")
PASSPHRASE = os.getenv("PASSPHRASE", "changeme")

# ✅ 全域風控限制（來自 .env 或預設）
MAX_TOTAL_POSITION_PCT = float(os.getenv("MAX_TOTAL_POSITION_PCT", 0.7))

# ✅ 預設策略參數
DEFAULT_STRATEGY_CONFIG = {
    "capital_pct": float(os.getenv("DEFAULT_CAPITAL_PCT", 0.05)),
    "leverage": int(os.getenv("DEFAULT_LEVERAGE", 5)),
    "max_qty": float(os.getenv("DEFAULT_MAX_QTY", 0.03)),
    "max_slippage_pct": float(os.getenv("DEFAULT_MAX_SLIPPAGE_PCT", 0.5)),
    "enabled": True,
    "max_position_usdt": float(os.getenv("DEFAULT_MAX_POSITION_USDT", 1000))
}

# ✅ 自訂策略設定（可由外部自動產生或編輯）
STRATEGIES = {
    "BTCUSDT_1h_MACD": {
        "capital_pct": 0.1,
        "leverage": 10
    },
    "ETHUSDT_15m_RSI": {
        "capital_pct": 0.05,
        "enabled": False
    }
}

def get_strategy_config(name):
    return STRATEGIES.get(name, DEFAULT_STRATEGY_CONFIG.copy())
