# order_manager.py
# 將幣安邏輯從此檔案移除，改為引用 binance_future.py 模組

from binance_future import (
    get_price,
    get_position,
    place_market_order,
    place_limit_order,
    place_tp_sl_orders,
    close_position
)

# 在這裡實作策略接收 webhook 訊號後的邏輯，如 handle_order() 等
# 例如：
# def handle_order(data):
#     symbol = data["symbol"]
#     action = data["action"]
#     ...
#     place_market_order(symbol, ...) 等
