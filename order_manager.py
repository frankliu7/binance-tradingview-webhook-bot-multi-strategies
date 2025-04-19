# order_manager.py
from api.binance_future import BinanceFutureHttpClient, OrderSide, OrderType
from config import API_KEY, API_SECRET
from util import get_account_balance, get_position_amount
from decimal import Decimal
from logger import log_trade

client = BinanceFutureHttpClient(api_key=API_KEY, secret=API_SECRET)

def execute_order(cfg, action, signal_price):
    symbol = cfg["symbol"]
    capital_pct = cfg.get("capital_pct", 1.0)
    leverage = cfg.get("leverage", 1)
    max_usdt = cfg.get("max_position_usdt", 999999)
    fallback_volume = cfg.get("trading_volume", 0.01)

    # 查詢帳戶總資金（USDT）與目前倉位
    balance = get_account_balance(client, asset="USDT")
    current_position = get_position_amount(client, symbol)

    # 計算理論下單金額（使用資金比例與槓桿）
    max_trade_usdt = balance * capital_pct * leverage
    remaining_allowable = max_usdt - (abs(current_position) * signal_price)
    final_trade_usdt = min(max_trade_usdt, remaining_allowable)

    # 若可下單金額太小，則使用 fallback trading_volume
    if final_trade_usdt < 5:
        quantity = fallback_volume
    else:
        quantity = round(Decimal(final_trade_usdt / signal_price), 4)

    # 根據 action 決定下單方向或平倉
    if action.upper() == "LONG":
        order_side = OrderSide.BUY
    elif action.upper() == "SHORT":
        order_side = OrderSide.SELL
    elif action.upper() == "EXIT":
        if current_position > 0:
            order_side = OrderSide.SELL
            quantity = abs(current_position)
        elif current_position < 0:
            order_side = OrderSide.BUY
            quantity = abs(current_position)
        else:
            return {"status": "no position to exit"}
    else:
        raise ValueError("不支援的動作")

    # 建立 order_id
    order_id = client.get_client_order_id()

    # 執行市價單下單
    status, order = client.place_order(
        symbol=symbol,
        order_side=order_side,
        order_type=OrderType.MARKET,
        quantity=quantity,
        price=Decimal(str(signal_price)),
        client_order_id=order_id
    )

    if status == 200:
        executed_price = float(order.get("avgFillPrice") or order.get("price"))
        result = {
            "qty": float(order.get("executedQty")),
            "executed_price": executed_price,
            "order_id": order_id,
            "status": "filled"
        }
        log_trade(cfg["symbol"], action, result)
        return result
    else:
        raise Exception(f"下單失敗: {order}")
