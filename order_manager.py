from binance_future import (
    get_price,
    get_position,
    place_market_order,
    place_limit_order,
    place_tp_sl_orders,
    close_position
)
import logging
from config import get_strategy_config
from util import is_within_slippage

logger = logging.getLogger("bot")

def handle_order(data):
    strategy = data.get("strategy_name")
    symbol = data.get("symbol")
    action = data.get("action")
    side = "BUY" if action == "LONG" else "SELL"
    price = float(data.get("price", 0))
    tp1 = float(data.get("take_profit_1", 0))
    tp2 = float(data.get("take_profit_2", 0))
    stop_loss = float(data.get("stop_loss", 0))
    tp_ratio_1 = float(data.get("tp_ratio_1", 0.5))
    tp_ratio_2 = float(data.get("tp_ratio_2", 0.5))

    logger.info(f"📥 [{strategy}] {action} {symbol} @ {price} TP1={tp1} TP2={tp2} SL={stop_loss}")

    # 滑價比對
    market_price = get_price(symbol)
    config = get_strategy_config(strategy)
    slippage_pct = config.get("max_slippage_pct", 0.5)

    if not is_within_slippage(price, market_price, slippage_pct):
        logger.warning(f"⛔ [{strategy}] 滑價過大：TV={price} / Market={market_price} 超過允許({slippage_pct}%)，拒單")
        return

    if action in ["LONG", "SHORT"]:
        total_qty = 0.01
        qty1 = round(total_qty * tp_ratio_1, 4)
        qty2 = round(total_qty * tp_ratio_2, 4)

        place_market_order(symbol, side, total_qty)

        if tp1:
            place_limit_order(symbol, "SELL" if side == "BUY" else "BUY", qty1, tp1, reduce_only=True)
        if tp2:
            place_limit_order(symbol, "SELL" if side == "BUY" else "BUY", qty2, tp2, reduce_only=True)

        if stop_loss:
            place_tp_sl_orders(symbol, side, stop_loss_price=stop_loss)

    elif action == "EXIT":
        logger.info(f"🚪 [{strategy}] 平倉 {symbol}")
        close_position(symbol)

    else:
        logger.warning(f"⚠️ 未知指令：{action}")
