from binance.client import Client
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

client = Client(api_key, api_secret)

def get_price(symbol):
    ticker = client.futures_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def get_position(symbol):
    positions = client.futures_position_information(symbol=symbol)
    for p in positions:
        amt = float(p['positionAmt'])
        if amt != 0:
            return {
                "amt": amt,
                "side": "LONG" if amt > 0 else "SHORT",
                "entry": float(p['entryPrice'])
            }
    return None

def place_market_order(symbol, side, quantity, reduce_only=False):
    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type="MARKET",
        quantity=quantity,
        reduceOnly=reduce_only
    )
    return order

def place_limit_order(symbol, side, quantity, price, time_in_force="GTC", reduce_only=False):
    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type="LIMIT",
        timeInForce=time_in_force,
        quantity=quantity,
        price=str(price),
        reduceOnly=reduce_only
    )
    return order

def place_tp_sl_orders(symbol, side, take_profit_price=None, stop_loss_price=None):
    results = {}

    if take_profit_price:
        results['tp_order'] = client.futures_create_order(
            symbol=symbol,
            side="SELL" if side == "BUY" else "BUY",
            type="TAKE_PROFIT_MARKET",
            stopPrice=str(take_profit_price),
            closePosition=True,
            timeInForce="GTC"
        )

    if stop_loss_price:
        results['sl_order'] = client.futures_create_order(
            symbol=symbol,
            side="SELL" if side == "BUY" else "BUY",
            type="STOP_MARKET",
            stopPrice=str(stop_loss_price),
            closePosition=True,
            timeInForce="GTC"
        )

    return results

def close_position(symbol):
    pos = get_position(symbol)
    if not pos:
        return None
    close_side = "SELL" if pos['side'] == "LONG" else "BUY"
    quantity = abs(pos['amt'])
    return place_market_order(symbol, close_side, quantity, reduce_only=True)
