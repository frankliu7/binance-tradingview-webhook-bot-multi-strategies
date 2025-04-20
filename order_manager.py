import time
from decimal import Decimal
from config import get_strategy_config, MAX_TOTAL_POSITION_PCT
from binance_future import BinanceFutureHttpClient
from performance_tracker import record_trade
from util import get_slippage_pct

client = BinanceFutureHttpClient()

def handle_order(payload):
    symbol = payload.get("symbol")
    strategy = payload.get("strategy_name")
    action = payload.get("action")
    signal_price = float(payload.get("price"))
    ts = int(payload.get("timestamp", time.time()))
    
    # 支援 TradingView 傳入 position_pct 覆寫 config
    config = get_strategy_config(strategy)
    if "position_pct" in payload:
        config["capital_pct"] = float(payload["position_pct"])

    # 設定槓桿（若需要）
    max_leverage = client.get_max_leverage(symbol)
    if max_leverage:
        client.set_leverage(symbol, max_leverage)

    # 計算下單數量
    acct_code, acct_info = client.get_account_info()
    usdt_balance = float(acct_info["totalWalletBalance"])
    capital = usdt_balance * config["capital_pct"] * config["leverage"]
    qty = round(capital / signal_price, 3)

    # 滑價檢查
    code, price_data = client.get_latest_price(symbol)
    if code != 200:
        return
    market_price = float(price_data["price"])
    slip_pct = get_slippage_pct(signal_price, market_price)
    if slip_pct > config["max_slippage_pct"]:
        print(f"❌ 超過滑價上限 {slip_pct:.2f}%，忽略下單")
        return

    # 下單邏輯
    if action == "long":
        client.place_market_order(symbol, "BUY", qty)
    elif action == "short":
        client.place_market_order(symbol, "SELL", qty)
    elif action == "exit":
        client.close_position(symbol, position_side="LONG")
        client.close_position(symbol, position_side="SHORT")

    # 紀錄績效
    record_trade({
        "strategy": strategy,
        "symbol": symbol,
        "action": action,
        "qty": qty,
        "price": market_price,
        "timestamp": ts,
        "slippage_pct": slip_pct
    })
