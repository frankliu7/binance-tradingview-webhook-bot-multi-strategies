import os
import json
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from order_manager import handle_order
from logger import setup_logger

load_dotenv()

app = Flask(__name__)
logger = setup_logger()

WEBHOOK_PASSPHRASE = os.getenv("WEBHOOK_PASSPHRASE")

@app.route("/", methods=["GET"])
def home():
    return "🚀 Bot is running."

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()

        if data.get("passphrase") != WEBHOOK_PASSPHRASE:
            logger.warning("⛔ 拒絕：Passphrase 錯誤")
            return jsonify({"code": 403, "msg": "Invalid passphrase"}), 403

        logger.info(f"📩 收到 webhook: {json.dumps(data)}")

        # 傳入 order_manager 處理下單邏輯
        handle_order(data)

        return jsonify({"code": 200, "msg": "Webhook received"})

    except Exception as e:
        logger.exception("Webhook 處理錯誤")
        return jsonify({"code": 500, "msg": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
