# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ 來自 .env 的模式參數
BINANCE_MODE = os.getenv("BINANCE_MODE", "live")
PORT = int(os.getenv("PORT", 8888))
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", 8501))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ✅ 全體風控設定
MAX_TOTAL_POSITION_PCT = float(os.getenv("MAX_TOTAL_POSITION_PCT", 0.7))  # 所有策略最大倉位佔帳戶總額比例

# ✅ 預設策略參數（用於自動註冊時）
DEFAULT_STRATEGY_CONFIG = {
    "capital_pct": 0.05,           # 預設佔用資金 5%
    "leverage": 5,                 # 預設槓桿 5 倍（實際下單時會查幣安最大）
    "max_qty": 0.03,               # 預設最大倉位
    "max_slippage_pct": 0.5        # 預設滑價容忍 0.5%
}

# ✅ 已手動註冊的策略（可選）
STRATEGIES = {
    "BTC_MACD": {
        "capital_pct": 0.2,
        "leverage": 10
    },
    "ETH_RSI": {
        "capital_pct": 0.1,
        "enabled": True
    }
}

def get_strategy_config(name):
    return STRATEGIES.get(name, DEFAULT_STRATEGY_CONFIG.copy())

# ✅ 若啟用模擬環境，自動切換 binance host
from binance_future import BinanceFutureHttpClient

if BINANCE_MODE == "testnet":
    BinanceFutureHttpClient.host = "https://testnet.binancefuture.com"
