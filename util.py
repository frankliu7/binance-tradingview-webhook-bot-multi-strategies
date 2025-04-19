# util.py
from decimal import Decimal

def get_account_balance(client, asset="USDT"):
    """
    回傳帳戶該資產的可用餘額（期貨帳戶）
    """
    try:
        data = client.get_balance()
        for item in data:
            if item["asset"] == asset:
                return float(item["balance"])
    except Exception as e:
        print(f"取得帳戶餘額錯誤: {e}")
    return 0.0

def get_position_amount(client, symbol):
    """
    回傳該交易對的目前持倉量：
    正數表示多單，負數表示空單，0 表示無倉位。
    """
    try:
        positions = client.get_position()
        for pos in positions:
            if pos["symbol"] == symbol:
                amt = Decimal(pos["positionAmt"])
                return float(amt)
    except Exception as e:
        print(f"取得倉位失敗: {e}")
    return 0.0
