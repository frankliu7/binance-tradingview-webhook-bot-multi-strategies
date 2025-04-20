import os
from dotenv import load_dotenv
import json
from typing import Dict

load_dotenv()

CONFIG_FILE = "strategy_config.json"

# 預設策略模板
DEFAULT_STRATEGY_TEMPLATE = {
    "enabled": True,
    "max_position": 100,
    "capital_fraction": 0.2,
    "qty1": 0.5,
    "qty2": 0.5,
    "rr1": 1.0,
    "rr2": 2.0
}

# 載入或初始化策略設定檔
def load_strategy_config() -> Dict[str, dict]:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_strategy_config(config: Dict[str, dict]):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# 自動註冊新策略名稱
def register_new_strategy(strategy_name: str) -> Dict[str, dict]:
    config = load_strategy_config()

    if strategy_name not in config:
        print(f"[config] 註冊新策略: {strategy_name}")
        config[strategy_name] = DEFAULT_STRATEGY_TEMPLATE.copy()
        save_strategy_config(config)

    return config

# 取得單一策略參數
def get_strategy_params(strategy_name: str) -> dict:
    config = register_new_strategy(strategy_name)

    params = config[strategy_name]

    if params["max_position"] == 0 or not params["enabled"]:
        print(f"[config] 策略 {strategy_name} 被禁用或 max_position 為 0，忽略")
        return {"enabled": False}  # 特別標記為禁用

    return params

# 手動觸發重載（或供 Flask dashboard 用）
def reload_config():
