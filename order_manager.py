from decimal import Decimal
from config import get_strategy_config, MAX_TOTAL_POSITION_PCT
from binance_future import BinanceFutureHttpClient
from performance_tracker import record_trade
from util import get_total_balance, get_open_position_value
import os

binance_client = BinanceFutureHttpClient(
    api_key=os.getenv("BINANCE_API_KEY"),
    secret=os.getenv("BINANCE_API_SECRET")
)

def handle_order(data):
    strategy_name = data.get("strategy_name")
    action = data.get("action", "").upper()
    symbol = data.get("symbol", "BTCUSDT")
    signal_price = Decimal(str(data.get("price", "0")))
    timestamp = data.get("timestamp", None)

    # 取得策略設定（如無則 fallback）
    config = get_strategy_config(strategy_name)
    capital_pct = Decimal(str(config["capital_pct"]))
    leverage = Decimal(str(data.get("leverage", config["leverage"])))
    max_qty = Decimal(str(config.get("max_qty", 0.1)))
    max_slippage_pct = Decimal(str(config.get("max_slippage_pct", 0.5)))

    # 取得帳戶總資金與目前持倉
    total_balance = get_total_balance(binance_client)
    notional_now = get_open_position_value(binance_client, symbol)
    max_allowed = total_balance * Decimal(str(MAX_TOTAL_POSITION_PCT))

    # 預估下單持倉金額
    order_notional = total_balance * capital_pct * leverage

    if notional_now + order_notional > max_allowed:
        print(f"[❌ 超過總倉上限] 拒絕策略 {strategy_name} 下單, 欲下倉位: {order_notional}, 已佔用: {notional_now}, 上限: {max_allowed}")
        return

    # 計算下單數量（幣種）
    status, ticker = binance_client.get_ticker(symbol)
    mark_price = Decimal(ticker["askPrice"]) if status == 200 else signal_price
    quantity = (order_notional / mark_price).quantize(Decimal("0.0001"))

    if quantity > max_qty:
        quantity = max_qty

    # 檢查滑價
    slippage = abs(mark_price - signal_price) / signal_price * 100
    if slippage > max_slippage_pct:
        print(f"[❌ 滑價過高] 策略 {strategy_name} 滑價 {slippage:.2f}% 超過上限 {max_slippage_pct}%")
        return

    # ✅ 設定幣安槓桿倍率（使用 webhook 或自動查詢）
    leverage_int = int(leverage)
    if "leverage" not in data:
        leverage_int = binance_client.get_max_leverage(symbol)
    binance_client.set_leverage(symbol, leverage_int)

    # ✅ 市價單方向
    side = "BUY" if action == "LONG" else "SELL"
    print(f"[📥 下單] 策略: {strategy_name}, 動作: {action}, 數量: {quantity}, 價格: {mark_price}, 槓桿: {leverage_int}x")

    # ⛳ 下市價單
    status, order = binance_client.place_order(
        symbol=symbol,
        order_side=side,
        order_type="MARKET",
        quantity=quantity,
        price=mark_price  # 對市價單會自動忽略
    )

    if status == 200:
        record_trade(
            strategy_name=strategy_name,
            symbol=symbol,
            side=side,
            price=float(mark_price),
            qty=float(quantity),
            timestamp=timestamp,
            is_entry=True
        )
    else:
        print(f"[❌ 下單失敗] 策略: {strategy_name}, 錯誤: {order}")
