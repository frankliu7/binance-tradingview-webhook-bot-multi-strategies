# config.py

strategies = {
    "BTC_MACD": {
        "capital_pct": 0.1,
        "leverage": 10,
        "max_qty": 0.05,
        "max_slippage_pct": 0.5
    },
    # 可手動新增更多策略...
}

# 預設策略參數（當 strategy_name 未在上方註冊時會使用）
DEFAULT_STRATEGY_CONFIG = {
    "capital_pct": 0.05,           # 預設佔用資金 5%
    "leverage": 5,                 # 預設槓桿 5 倍
    "max_qty": 0.03,               # 預設最大倉位
    "max_slippage_pct": 0.5        # 預設滑價容忍 0.5%
}

def get_strategy_config(name):
    return strategies.get(name, DEFAULT_STRATEGY_CONFIG.copy())
