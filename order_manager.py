import logging
from decimal import Decimal
from util import get_binance_price, within_slippage
from config import get_strategy_config
from position_tracker import record_position

logger = logging.getLogger("bot")

def handle_order(data):
    strategy_name = data.get("strategy_name")
    symbol = data.get("symbol")
    action = data.get("action")
    price = float(data.get("price", 0))
    tp1 = float(data.get("take_profit_1", 0))
    tp2 = float(data.get("take_profit_2", 0))
    tp_ratio_1 = float(data.get("tp_ratio_1", 0.5))
    tp_ratio_2 = float(data.get("tp_ratio_2", 0.5))
    stop_loss = float(data.get("stop_loss", 0))
    timestamp = data.get("timestamp")

    logger.info(f"處理策略 {strategy_name}: {action} @ {price}, TP1={tp1}, TP2={tp2}, SL={stop_loss}, TS={timestamp}")

    # 取得當前幣安價格，比對滑價
    market_price = get_binance_price(symbol)
    if not within_slippage(price, market_price):
        logger.warning(f"⛔ 滑價過大：signal={price}, market={market_price}")
        return

    # 下單模擬邏輯（之後可改成 binance 下單）
    if action == "LONG":
        logger.info(f"✅ 開多倉 @ {market_price} - 止盈1: {tp1} ({tp_ratio_1*100}%) 止盈2: {tp2} ({tp_ratio_2*100}%) 止損: {stop_loss}")
        record_position(strategy_name, symbol, "LONG", market_price, tp1, tp2, tp_ratio_1, tp_ratio_2, stop_loss, timestamp)

    elif action == "SHORT":
        logger.info(f"✅ 開空倉 @ {market_price} - 止盈1: {tp1} ({tp_ratio_1*100}%) 止盈2: {tp2} ({tp_ratio_2*100}%) 止損: {stop_loss}")
        record_position(strategy_name, symbol, "SHORT", market_price, tp1, tp2, tp_ratio_1, tp_ratio_2, stop_loss, timestamp)

    elif action == "EXIT":
        logger.info(f"🚪 平倉指令收到 for {strategy_name}")
        # 👉 TODO: 加入實際倉位查詢與市價平倉邏輯

    else:
        logger.warning(f"⚠️ 未知 action: {action}")
