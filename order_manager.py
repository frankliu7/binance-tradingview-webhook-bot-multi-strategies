import logging
from decimal import Decimal
from config import get_strategy_config, MAX_TOTAL_POSITION_PCT
from util import get_total_balance, get_open_position_value
from binance_future import BinanceFutureHttpClient, OrderSide, OrderType
from performance_tracker import record_trade

def should_block_order(binance_client, symbol, position_value_estimate: Decimal) -> bool:
    try:
        total_balance = get_total_balance(binance_client)
        current_open = get_open_position_value(binance_client, symbol)
        total_after_order = current_open + position_value_estimate
        max_allowed = total_balance * Decimal(str(MAX_TOTAL_POSITION_PCT))

        if total_after_order > max_allowed:
            logging.warning(f"[風控] 倉位超過總額限制：目前 {total_after_order} > 上限 {max_allowed}")
            return True
    except Exception as e:
        logging.error(f"[風控] 檢查總體倉位失敗: {e}")
    return False

def handle_order(data: dict, binance_client: BinanceFutureHttpClient):
    strategy_name = data.get("strategy_name")
    symbol = data.get("symbol")
    action = data.get("action").lower()
    entry_price = Decimal(str(data.get("price")))
    timestamp = data.get("timestamp", None)

    # TP/SL 支援
    tp1 = Decimal(str(data.get("tp1", 0)))
    tp2 = Decimal(str(data.get("tp2", 0)))
    sl = Decimal(str(data.get("sl", 0)))

    if not all([strategy_name, symbol, action, entry_price]):
        logging.error("[handle_order] 缺少必要參數")
        return

    config = get_strategy_config(strategy_name)
    capital_pct = Decimal(str(data.get("position_pct", config["capital_pct"])))
    leverage = Decimal(str(config["leverage"]))
    max_slippage_pct = Decimal(str(config["max_slippage_pct"]))

    # 計算下單金額（估算用於風控）
    total_balance = get_total_balance(binance_client)
    estimated_value = total_balance * capital_pct * leverage

    if should_block_order(binance_client, symbol, estimated_value):
        logging.warning(f"[忽略] 超出總體倉位上限，略過策略 {strategy_name} 下單")
        return

    qty = estimated_value / entry_price
    # 可加 max_qty 限制

    logging.info(f"[下單] {strategy_name} | {action.upper()} | {symbol} | 金額: {estimated_value:.2f} | 價格: {entry_price:.2f}")

    # 下市價單
    side = OrderSide.BUY if action == "long" else OrderSide.SELL
    status, order = binance_client.place_order(
        symbol=symbol,
        order_side=side,
        order_type=OrderType.MARKET,
        quantity=qty,
        price=entry_price
    )

    if status == 200:
        logging.info(f"[成功] 下單成功: {order.get('orderId')}")
        record_trade(
            strategy_name=strategy_name,
            symbol=symbol,
            side=action,
            entry_price=entry_price,
            qty=qty,
            tp1=tp1,
            tp2=tp2,
            sl=sl,
            timestamp=timestamp
        )
    else:
        logging.warning(f"[失敗] 下單失敗: {order}")
