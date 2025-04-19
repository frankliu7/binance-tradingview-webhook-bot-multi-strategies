# config.py

strategy_config = {
    "BTCUSDT_1h_MACD": {
        "enabled": True,  # 策略是否啟用
        "symbol": "BTCUSDT",
        "exchange": "binance_future",
        "capital_pct": 0.1,         # 使用帳戶資金的比例，例如 0.1 表示使用 10%
        "max_position_usdt": 500,   # 最大持倉資金上限 (USD)
        "leverage": 10,             # 預期使用槓桿倍數（如需實際下單控制，需搭配 API 設定）
        "trading_volume": 0.01,     # 單次下單數量，fallback 用（優先使用資金比轉換）
        "max_slippage_pct": 0.5     # 容許的最大滑價百分比
    },

    "BTCUSDT_1h_ATR": {
        "enabled": False,
        "symbol": "BTCUSDT",
        "exchange": "binance_future",
        "capital_pct": 0.05,
        "max_position_usdt": 300,
        "leverage": 5,
        "trading_volume": 0.005,
        "max_slippage_pct": 0.3
    }
}

# 全局參數
WEBHOOK_PASSPHRASE = "mysecurepass"
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
