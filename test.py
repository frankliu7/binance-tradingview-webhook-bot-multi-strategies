import requests
import datetime

def fetch_bitcoin_prices():
    # Binance API endpoint for historical Klines (candlestick) data
    url = "https://api.binance.com/api/v3/klines"
    symbol = "BTCUSDT"  # Bitcoin to USDT
    interval = "1d"  # Daily interval
    end_time = int(datetime.datetime.now().timestamp() * 1000)  # Current time in milliseconds
    start_time = int((datetime.datetime.now() - datetime.timedelta(days=20)).timestamp() * 1000)  # 20 days ago

    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_time,
        "endTime": end_time,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        prices = [{"date": datetime.datetime.fromtimestamp(candle[0] / 1000).strftime('%Y-%m-%d'), "price": float(candle[4])} for candle in data]
        return prices
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

if __name__ == "__main__":
    try:
        prices = fetch_bitcoin_prices()
        for price in prices:
            print(f"Date: {price['date']}, Closing Price: {price['price']}")
    except Exception as e:
        print(f"Error: {e}")