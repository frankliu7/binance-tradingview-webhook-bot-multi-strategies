# config.py

strategy_config = {
    "BTCUSDT_1h_MACD": {
        "enabled": True,  # 是否啟用策略
        "symbol": "BTCUSDT",
        "exchange": "binance_future",
        "capital_pct": 0.1,             # 使用帳戶資金的比例，例如 0.1 = 10%
        "max_position_usdt": 500,       # 單策略最大持倉 USD 上限
        "leverage": 10,                 # 預設槓桿倍率（風控用）
        "trading_volume": 0.01,         # fallback 單次下單量
        "max_slippage_pct": 0.5         # 接受滑價上限（%）
    },

    "ETHUSDT_15m_RSI": {
        "enabled": True,
        "symbol": "ETHUSDT",
        "exchange": "binance_future",
        "capital_pct": 0.05,
        "max_position_usdt": 300,
        "leverage": 5,
        "trading_volume": 0.005,
        "max_slippage_pct": 0.3
    }
}

# 安全驗證用的 passphrase
WEBHOOK_PASSPHRASE = "mysecurepass"

# Binance API 金鑰
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
