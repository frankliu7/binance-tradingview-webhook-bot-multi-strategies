def is_within_slippage(signal_price, market_price, slippage_pct):
    diff = abs(signal_price - market_price)
    max_diff = signal_price * (slippage_pct / 100)
    return diff <= max_diff

def calc_quantity(price, config, usdt_balance):
    cap = config.get("capital_pct", 0.1)
    lev = config.get("leverage", 1)
    max_qty = config.get("max_qty", 0)

    qty = (usdt_balance * cap * lev) / price
    if max_qty > 0:
        qty = min(qty, max_qty)
    return round(qty, 4)
