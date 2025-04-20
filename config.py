import os

# 新增從 .env 載入金鑰
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# 新增支援 testnet 模式
BINANCE_BASE_URL = "https://testnet.binancefuture.com" if os.getenv("BINANCE_MODE") == "testnet" else "https://fapi.binance.com"

# ✅ 加入總倉位限制設定
MAX_TOTAL_POSITION_PCT = 0.7

# ✅ 原本的 DEFAULT_STRATEGY_CONFIG + 加入 "enabled"
DEFAULT_STRATEGY_CONFIG = {
    "capital_pct": 0.05,
    "leverage": 5,
    "max_qty": 0.03,
    "max_slippage_pct": 0.5,
    "enabled": True
}

# ✅ STRATEGIES 改大寫符合其他檔案一致命名習慣
STRATEGIES = {
    "BTCUSDT_1h_MACD": {
        "capital_pct": 0.1,
        "leverage": 10
    },
    "ETHUSDT_15m_RSI": {
        "capital_pct": 0.08,
        "enabled": False
    }
}

# ✅ 改用 dict.update() 支援 fallback
def get_strategy_config(name: str):
    cfg = STRATEGIES.get(name, {})
    final = DEFAULT_STRATEGY_CONFIG.copy()
    final.update(cfg)
    return final
