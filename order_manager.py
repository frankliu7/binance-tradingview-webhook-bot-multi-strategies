import time
from decimal import Decimal
from config import get_strategy_params, MAX_TOTAL_POSITION_USDT
from binance_future import BinanceFutureHttpClient
from performance_tracker import record_trade
from util import get_slippage_pct
from position_tracker import get_binance_position_summary
from logger import log_info, log_warn, log_error

client = BinanceFutureHttpClient()

def handle_order(payload):
    symbol = payload.get("symbol")
    strategy = payload.get("strategy_name")
    action = payload.get("action")
    signal_price = float(payload.get("price", 0))
    ts = int(payload.get("timestamp", time.time()))

    log_info(f"🚀 開始處理策略：{strategy} / {symbol} / {action}")

    config = get_strategy_params(strategy)
    if not config.get("enabled", True):
        log_warn(f"策略 {strategy} 已停用，略過下單")
        return {"status": "ignored", "reason": "strategy disabled"}

    # 套用 webhook 的資金配置（如有）
    capital_pct = float(payload.get("position_pct", config["capital_pct"]))
    leverage = int(payload.get("leverage", config["leverage"]))
    max_slippage = float(config.get("max_slippage_pct", 0.5))

    # 設定最大槓桿
    max_leverage = client.get_max_leverage(symbol)
    if max_leverage:
        leverage = min(leverage, max_leverage)
        client.set_leverage(symbol, leverage)

    # 查詢資金與倉位限制
    acct_code, acct_info = client.get_account_info()
    usdt_balance = float(acct_info["totalWalletBalance"])
    capital = usdt_balance * capital_pct * leverage
    qty = round(capital / signal_price, 3)

    # 倉位限制檢查
    total_pos = get_binance_position_summary()
    total_used = total_pos.get("total_long", 0) + total_pos.get("total_short", 0)
    if total_used + capital > MAX_TOTAL_POSITION_USDT:
        log_warn(f"⛔ 倉位已滿 {total_used:.0f} + {capital:.0f} > 限制 {MAX_TOTAL_POSITION_USDT}")
        return {"status": "ignored", "reason": "max total position exceeded"}

    # 滑價比對
    code, price_data = client.get_latest_price(symbol)
    if code != 200:
        return {"status": "error", "reason": "failed to fetch market price"}
    market_price = float(price_data["price"])
    slip_pct = get_slippage_pct(signal_price, market_price)
    if slip_pct > max_slippage:
        log_warn(f"❌ 超過滑價上限 {slip_pct:.2f}% > {max_slippage}%")
        return {"status": "ignored", "reason": "slippage too high"}

    # 動作處理
    if action == "long":
        client.place_market_order(symbol, "BUY", qty)
    elif action == "short":
        client.place_market_order(symbol, "SELL", qty)
    elif action == "exit":
        client.close_position(symbol, position_side="LONG")
        client.close_position(symbol, position_side="SHORT")
    else:
        return {"status": "ignored", "reason": "invalid action"}

    # 紀錄績效
    delay_sec = int(time.time()) - ts
    record_trade({
        "strategy": strategy,
        "symbol": symbol,
        "action": action,
        "qty": qty,
        "price": market_price,
        "timestamp": ts,
        "slippage_pct": slip_pct,
        "delay_sec": delay_sec
    })

    log_info(f"✅ 下單成功：{symbol} @ {market_price:.2f} | qty={qty} | slippage={slip_pct:.2f}%")
    return {"status": "success", "symbol": symbol, "price": market_price, "qty": qty}
