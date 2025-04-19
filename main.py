# 主入口 main.py
# 接收 TradingView webhook 並分發給各模組
from flask import Flask, request, jsonify
from config import strategy_config
from order_manager import execute_order
from position_tracker import update_position, get_all_positions
from logger import log_trade, log_error
from monitor import get_monitor_status, record_slippage_alert
import traceback
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Trading Bot is running. Access /status for dashboard info."

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        strategy_name = data.get("strategy_name")
        signal_price = float(data.get("price", 0))

        if strategy_name not in strategy_config:
            return jsonify({"error": "策略名稱錯誤"}), 400

        cfg = strategy_config[strategy_name]
        if not cfg.get("enabled", True):
            return jsonify({"msg": f"策略 {strategy_name} 未啟用"}), 200

        action = data.get("action")
        result = execute_order(cfg, action, signal_price=signal_price)

        # 計算滑價百分比並處理
        executed_price = result.get("executed_price")
        if signal_price > 0 and executed_price:
            slippage_pct = abs(executed_price - signal_price) / signal_price * 100
            result["signal_price"] = signal_price
            result["slippage_pct"] = round(slippage_pct, 4)
            
            if slippage_pct > cfg.get("max_slippage_pct", 0.5):  # 超過滑價容忍上限
                result["slippage_alert"] = True
                record_slippage_alert(strategy_name, result)
                return jsonify({"error": f"滑價過大（{slippage_pct:.2f}%），已拒單"}), 400

        # 更新倉位與紀錄
        update_position(strategy_name, action, result.get("qty"))
        log_trade(strategy_name, action, result)

        return jsonify({"msg": "下單成功", "detail": result})

    except Exception as e:
        log_error(f"Webhook 錯誤: {e}\n{traceback.format_exc()}")
        return jsonify({"error": "Webhook 處理錯誤"}), 500

@app.route('/status', methods=['GET'])
def status():
    try:
        return jsonify(get_monitor_status())
    except Exception as e:
        log_error(f"狀態查詢錯誤: {e}\n{traceback.format_exc()}")
        return jsonify({"error": "無法取得狀態資訊"}), 500

if __name__ == '__main__':
    print("[INFO] Trading bot started at", time.strftime('%Y-%m-%d %H:%M:%S'))
    app.run(host='0.0.0.0', port=8888)
