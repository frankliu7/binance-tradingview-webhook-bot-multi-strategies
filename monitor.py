from config import get_strategy_config
from position_tracker import get_all_positions
from binance_future import get_price, get_position
from datetime import datetime

def get_strategy_status():
    status = {}
    positions = get_all_positions()

    for strategy, cfg in get_strategy_config().items():
        symbol = cfg.get("symbol", "")
        pos = positions.get(strategy, 0)
        market_price = get_price(symbol)

        status[strategy] = {
            "enabled": cfg.get("enabled", True),
            "symbol": symbol,
            "position_qty": pos,
            "capital_pct": cfg.get("capital_pct"),
            "leverage": cfg.get("leverage"),
            "slippage_limit": cfg.get("max_slippage_pct"),
            "market_price": market_price,
            "timestamp": datetime.utcnow().isoformat()
        }
    return status
