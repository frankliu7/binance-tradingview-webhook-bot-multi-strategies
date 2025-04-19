from flask import Flask, request, jsonify
from binance_future import BinanceFutureHttpClient
from config import get_strategy_config, strategies
from order_manager import handle_order
import logging
import os

app = Flask(__name__)

# 建立 Binance client
binance = BinanceFutureHttpClient(
    api_key=os.getenv("BINANCE_API_KEY"),
    secret=os.getenv("BINANCE_API_SECRET")
)

@app.route("/", methods=["GET"])
def index():
    return "✅ Webhook Server Ready"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        strategy_name = data.get("strategy_name")

        # 自動註冊策略名稱（如尚未存在）
        if strategy_name and strategy_name not in strategies:
            strategies[strategy_name] = {}  # 使用 DEFAULT_STRATEGY_CONFIG

        handle_order(data, binance)
        return jsonify({"status": "ok"})

    except Exception as e:
        logging.exception("[webhook] 接收失敗")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
