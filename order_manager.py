
from decimal import Decimal
import config
import binance_future
import performance_tracker
import position_tracker
import util
import logger

def process_order(data):
    strategy = data["strategy"]
    symbol = data["symbol"]
    qty = Decimal(str(data["qty"]))
    price = Decimal(str(data["price"]))
    action = data["action"]
    tp1 = Decimal(str(data.get("tp1", 0)))
    tp2 = Decimal(str(data.get("tp2", 0)))
    sl = Decimal(str(data.get("sl", 0)))
    qty1 = Decimal(str(data.get("qty1", 0.5)))
    qty2 = Decimal(str(data.get("qty2", 0.5)))
    exit_flag = data.get("exit", False)

    strategy_config = config.get_strategy_params(strategy)
    if not strategy_config.get("enabled", True):
        logger.log_warning(f"策略 {strategy} 已停用")
        return {"status": "skipped", "reason": "disabled"}

    current_value = position_tracker.get_total_position_value()
    if current_value + float(qty) > config.MAX_TOTAL_POSITION_USDT:
        logger.log_warning(f"策略 {strategy} 超過最大倉位，拒單")
        return {"status": "rejected", "reason": "max total position exceeded"}

    # 執行市價單
    try:
        result = binance_future.place_order(symbol, action, qty, leverage=None)
        executed_price = result["avg_fill_price"]

        logger.log_trade(strategy, action, symbol, executed_price, qty)

        performance_tracker.record_trade({
            "strategy": strategy,
            "symbol": symbol,
            "action": action,
            "side": "BUY" if action == "long" else "SELL",
            "price": price,
            "executed_price": executed_price,
            "qty": qty,
            "tp1": tp1,
            "tp2": tp2,
            "stop_loss": sl,
            "slippage_pct": util.calc_slippage_pct(price, executed_price),
            "lag_sec": util.calc_lag_sec(data.get("timestamp", 0)),
            "exit_time": "",
            "holding_secs": "",
            "pnl_pct": "",
            "tp_hit": "",
            "is_win": ""
        })

        return {"status": "filled", "executed_price": executed_price}

    except Exception as e:
        logger.log_error(f"策略 {strategy} 下單錯誤: {e}")
        return {"status": "error", "reason": str(e)}
