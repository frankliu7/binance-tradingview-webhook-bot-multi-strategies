import os
import json
from dotenv import load_dotenv

load_dotenv()

CONFIG_PATH = "strategy_config.json"

# 預設策略模版
DEFAULT_STRATEGY_TEMPLATE = {
    "enabled": True,
    "exchange": "binance_future",
    "capital_pct": float(os.getenv("DEFAULT_CAPITAL_PCT", 0.05)),
    "max_position_usdt": float(os.getenv("DEFAULT_MAX_POSITION_USDT", 1000)),
    "leverage": int(os.getenv("DEFAULT_LEVERAGE", 5)),
    "trading_volume": float(os.getenv("DEFAULT_MAX_QTY", 0.03)),
    "max_slippage_pct": float(os.getenv("DEFAULT_MAX_SLIPPAGE_PCT", 0.5))
}

# 讀取設定檔
def load_strategy_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

# 儲存設定檔
def save_strategy_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

# 取得單一策略參數（若不存在則自動註冊）
def get_strategy_params(strategy_name):
    config = load_strategy_config()
    if strategy_name not in config:
        config[strategy_name] = DEFAULT_STRATEGY_TEMPLATE.copy()
        save_strategy_config(config)
    return config[strategy_name]

# 讀取系統等級參數
WEBHOOK_PASSPHRASE = os.getenv("PASSPHRASE", "")
USE_TESTNET = os.getenv("USE_TESTNET", "true").lower() == "true"
MAX_TOTAL_POSITION_USDT = float(os.getenv("MAX_TOTAL_POSITION_USDT", 10000))
MAX_TOTAL_POSITION_PCT = float(os.getenv("MAX_TOTAL_POSITION_PCT", 0.7))

# API KEYs 依照 mode 回傳
def get_api_keys():
    if USE_TESTNET:
        return os.getenv("BINANCE_TEST_API_KEY"), os.getenv("_
