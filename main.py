# main.py
import json
from flask import Flask, request
from config import WEBHOOK_PASSPHRASE, strategy_config, register_strategy
from order_manager import execute_order
from logger import log_error

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Webhook Bot Online."

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = json.loads(request.data)
        if data.get("passphrase") != WEBHOOK_PASSPHRASE:
            return {"code": 403, "message": "Invalid passphrase"}, 403

        strategy_name = data.get("strategy_name")
        symbol = data.get("symbol")
        action = data.get("action")
        price = float(data.get("price"))

        # ✅ 自動註冊策略（若未事先定義）
        register_strategy(strategy_name, symbol)
        cfg = strategy_config[strategy_name]

        # 如果策略未啟用，直接跳過
        if not cfg.get("enabled", True):
            return {"code": 200, "message": f"{strategy_name} is disabled"}, 200

        result = execute_order(cfg, action, price)
        return {"code": 200, "message": "Order executed", "result": result}, 200

    except Exception as e:
        log_error(f"[webhook error] {str(e)}")
        return {"code": 500, "message": "Server error"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
