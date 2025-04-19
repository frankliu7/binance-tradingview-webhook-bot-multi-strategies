from binance_future import (
    get_price,
    get_position,
    place_market_order,
    place_limit_order,
    place_tp_sl_orders,
    close_position,
    get_account_balance
)
import logging
from config import get_strategy_config
from util import is_within_slippage, calc_quantity
from performance_tracker import record_trade
from datetime import datetime

logger = logging.getLogger("bot")

# 暫存開倉資訊：策略+幣種 對應進場價與時間
entry_cache = {}

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

    market_price = get_price(symbol)
    config = get_strategy_config(strategy)
    slippage_pct = config.get("max_slippage_pct", 0.5)

    if not is_within_slippage(price, market_price, slippage_pct):
        logger.warning(f"⛔ [{strategy}] 滑價過大：TV={price} / Market={market_price} 超過允許({slippage_pct}%)，拒單")
        return

    if action in ["LONG", "SHORT"]:
        usdt_balance = get_account_balance()
        total_qty = calc_quantity(market_price, config, usdt_balance)
        qty1 = round(total_qty * tp_ratio_1, 4)
        qty2 = round(total_qty * tp_ratio_2, 4)

        place_market_order(symbol, side, total_qty)

        if tp1:
            place_limit_order(symbol, "SELL" if side == "BUY" else "BUY", qty1, tp1, reduce_only=True)
        if tp2:
            place_limit_order(symbol, "SELL" if side == "BUY" else "BUY", qty2, tp2, reduce_only=True)

        if stop_loss:
            place_tp_sl_orders(symbol, side, stop_loss_price=stop_loss)

        # 儲存進場資訊供平倉分析用
        entry_cache[strategy + symbol] = {
            "entry_price": price,
            "entry_time": datetime.utcnow(),
            "tp1": tp1,
            "tp2": tp2,
            "sl": stop_loss
        }

        record_trade(
            strategy, symbol, action, side,
            entry_price=price,
            market_price=market_price,
            qty=total_qty,
            tp1=tp1, tp2=tp2,
            sl=stop_loss,
            slippage_pct=abs(price - market_price) / price * 100
        )

    elif action == "EXIT":
        logger.info(f"🚪 [{strategy}] 平倉 {symbol}")
        pos = get_position(symbol)
        if pos:
            close_position(symbol)

            entry_info = entry_cache.get(strategy + symbol, {})
            entry_price = entry_info.get("entry_price", pos['entry'])
            entry_time = entry_info.get("entry_time", datetime.utcnow())
            tp1 = entry_info.get("tp1", 0)
            tp2 = entry_info.get("tp2", 0)
            sl = entry_info.get("sl", 0)
            holding_secs = (datetime.utcnow() - entry_time).total_seconds()

            exit_price = get_price(symbol)
            pnl_pct = ((exit_price - entry_price) / entry_price) * 100 if pos['side'] == "LONG" else ((entry_price - exit_price) / entry_price) * 100
            tp_hit = "TP1" if tp1 and ((pos['side'] == "LONG" and exit_price >= tp1) or (pos['side'] == "SHORT" and exit_price <= tp1)) \
                     else "TP2" if tp2 and ((pos['side'] == "LONG" and exit_price >= tp2) or (pos['side'] == "SHORT" and exit_price <= tp2)) \
                     else "SL" if sl and ((pos['side'] == "LONG" and exit_price <= sl) or (pos['side'] == "SHORT" and exit_price >= sl)) \
                     else "-"

            record_trade(
                strategy, symbol, action, "SELL" if pos['side'] == "LONG" else "BUY",
                entry_price=entry_price,
                market_price=exit_price,
                qty=abs(pos['amt']),
                tp1=tp1, tp2=tp2, sl=sl,
                slippage_pct=0.0,
                extra={
                    "exit_time": datetime.utcnow().isoformat(),
                    "holding_secs": int(holding_secs),
                    "pnl_pct": round(pnl_pct, 2),
                    "tp_hit": tp_hit,
                    "is_win": pnl_pct > 0
                }
            )

    else:
        logger.warning(f"⚠️ 未知指令：{action}")
