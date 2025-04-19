import os
import json
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from order_manager import handle_order
from monitor import register_monitor_route

# 載入 .env
load_dotenv()
WEBHOOK_PASSPHRASE = os.getenv("WEBHOOK_PASSPHRASE")

# 初始化 Flask app
app = Flask(__name__)
logging.basicConfig(filename="log/bot.log", level=logging.INFO)

# 掛載 /monitor API
register_monitor_route(app)

@app.route("/", methods=["GET"])
def home():
    return "✅ Trading Bot Webhook Active."

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = json.loads(request.data)
        logging.info(f"📥 Webhook received: {data}")

        if data.get("passphrase") != WEBHOOK_PASSPHRASE:
            logging.warning("⛔ 密碼錯誤")
            return {"status": "error", "message": "Invalid passphrase"}, 401

        handle_order(data)
        return {"status": "success"}

    except Exception as e:
        logging.exception("❌ Webhook 發生錯誤")
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
