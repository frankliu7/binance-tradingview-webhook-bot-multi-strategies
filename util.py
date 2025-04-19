from decimal import Decimal
from binance_future import BinanceFutureHttpClient
from config import strategies
from config import get_strategy_config
import logging

# ✅ 查詢帳戶總資金（USDT）
def get_total_balance(binance_client: BinanceFutureHttpClient) -> Decimal:
    status, data = binance_client.get_balance()
    if status == 200 and isinstance(data, list):
        for item in data:
            if item["asset"] == "USDT":
                return Decimal(item["balance"])
    logging.warning("[util] get_total_balance fallback to 0")
    return Decimal("0")

# ✅ 計算目前某個交易對倉位價值（symbol 對應倉位金額）
def get_open_position_value(binance_client: BinanceFutureHttpClient, symbol: str) -> Decimal:
    status, data = binance_client.get_position_info(symbol)
    if status != 200:
        logging.warning(f"[util] get_position_info fail: {data}")
        return Decimal("0")

    for pos in data:
        if pos["symbol"] == symbol:
            notional = Decimal(pos.get("notional", "0"))
            return abs(notional)

    return Decimal("0")
