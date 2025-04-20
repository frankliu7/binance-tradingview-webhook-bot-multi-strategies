from flask import Flask, request, jsonify
from config import get_strategy_params
import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'Webhook server is running.'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "reason": "No JSON received"}), 400

    strategy_name = data.get("strategy_name")
    if not strategy_name:
        return jsonify({"status": "error", "reason": "Missing strategy_name"}), 400

    params = get_strategy_params(strategy_name)

    # 被禁用或 max_position = 0 的策略
    if not params.get("enabled", True):
        log_event("IGNORED", strategy_name, data, reason="Strategy disabled or max_position=0")
        return jsonify({
            "status": "ignored",
            "strategy": strategy_name,
            "reason": "disabled or max_position=0"
        }), 200

    # 正常策略處理流程（示範）
    # 可以送到 order_manager 處理下單
    log_event("ACCEPTED", strategy_name, data)

    return jsonify({
        "status": "received",
        "strategy": strategy_name,
        "params": params
    }), 200

# 簡易日誌函數
def log_event(status, strategy_name, data, reason=""):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{now}] [{status}] Strategy: {strategy_name} | Symbol: {data.get('symbol')} | Action: {data.get('action')}"

    if reason:
        msg += f" | Reason: {reason}"

    print(msg)

    with open("webhook.log", "a") as f:
        f.write(msg + "\n")

if __name__ == '__main__':
