import datetime
import binance_future
from config import get_strategy_params
from position_tracker import get_binance_position_summary

def log(msg):
    print(msg)
    with open("order.log", "a") as f:
        f.write(f"{msg}\n")

def execute_order(data: dict):
    strategy_name = data.get("strategy_name")
    symbol = data.get("symbol")
    action = data.get("action")  # "buy" / "sell"
    qty = float(data.get("qty", 0))

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefix = f"[{now}] [strategy: {strategy_name}]"

    # 基本欄位檢查
    if not all([strategy_name, symbol, action, qty]):
        msg = f"{prefix} ❌ 缺少必要欄位，忽略執行"
        log(msg)
        return {"status": "error", "reason": "missing parameters"}

    # 讀取策略設定
    params = get_strategy_params(strategy_name)
    if not params.get("enabled", True):
        msg = f"{prefix} ❌ 策略未啟用（disabled），忽略"
        log(msg)
        return {"status": "ignored", "reason": "strategy disabled"}

    if params.get("max_position", 0) == 0:
        msg = f"{prefix} ⛔ max_position = 0，策略禁用"
        log(msg)
        return {"status": "ignored", "reason": "max_position=0"}

    # 倉位風控檢查
    try:
        pos = get_binance_position_summary()
        if "error" in pos:
            msg = f"{prefix} ❗ Binance 倉位資料錯誤：{pos['error']}"
            log(msg)
            return {"status": "error", "reason": "position fetch failed"}

        current_total = pos['total_long'] + pos['total_short']
        if current_total >= params["max_position"]:
            msg = f"{prefix} 🚫 倉位已達上限 ({current_total:.2f} / {params['max_position']})"
            log(msg)
            return {"status": "ignored", "reason": "max_position exceeded"}
    except Exception as e:
        return {"status": "error", "reason": f"倉位檢查失敗：{e}"}

    # 決定方向
    side = "BUY" if action.lower() == "buy" else "SELL"

    # 呼叫 binance 下單
    result = binance_future.create_order(symbol, side, qty, strategy_name)

    if result["status"] == "success":
        log(f"{prefix} ✅ 下單成功：{symbol} {side} {qty}")
    elif result["status"] == "rejected":
        log(f"{prefix} ⛔ 下單被拒：{result.get('reason')}")
    else:
        log(f"{prefix} ❌ 下單失敗：{result.get('reason')}")

    return result
