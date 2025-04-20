
from flask import Flask, request, jsonify
import datetime
import os
from dotenv import load_dotenv
import order_manager
import util
from config import get_strategy_params
from decimal import Decimal

load_dotenv()
PASSPHRASE = os.getenv("PASSPHRASE", "")
app = Flask(__name__)

@app.route("/")
def index():
    return "Webhook server is running."

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return error("No JSON received")

    if data.get("passphrase") != PASSPHRASE:
        return error("Invalid passphrase")

    try:
        parsed = util.parse_webhook(data)
        strategy_name = parsed["strategy"]
        params = get_strategy_params(strategy_name)

        if not params.get("enabled", True) or params.get("max_position", 0) == 0:
            log_event("IGNORED", strategy_name, data, reason="Disabled or max_position=0")
            return jsonify({"status": "ignored", "strategy": strategy_name, "reason": "disabled or max_position=0"}), 200

        # ➕ 計算滑價與延遲
        parsed["slippage_pct"] = util.calc_slippage_pct(parsed["price"], parsed["price"])  # 預設先比對相同
        parsed["lag_sec"] = util.calc_lag_sec(parsed["timestamp"])

        # ➕ 呼叫下單模組
        order_result = order_manager.process_order(parsed)

        log_event("EXECUTED", strategy_name, data)
        return jsonify({
            "status": "success",
            "strategy": strategy_name,
            "order_result": order_result
        }), 200

    except Exception as e:
        return error(str(e))

def error(reason):
    log_event("ERROR", "Unknown", {}, reason=reason)
    return jsonify({"status": "error", "reason": reason}), 400

def log_event(status, strategy_name, data, reason=""):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{now}] [{status}] Strategy: {strategy_name} | Action: {data.get('action', '')}"
    if reason:
        msg += f" | Reason: {reason}"
    print(msg)
    with open("webhook.log", "a") as f:
        f.write(msg + "\n")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
