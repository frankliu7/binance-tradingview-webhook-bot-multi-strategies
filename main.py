import os
import json
import logging
import time
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from order_manager import handle_order
from logger import log_info, log_warn, log_error

load_dotenv()

app = Flask(__name__)
WEBHOOK_PASSPHRASE = os.getenv("PASSPHRASE", "")

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is running."

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        now_ts = int(time.time())

        # 1️⃣ 驗證密碼
        if data.get("passphrase") != WEBHOOK_PASSPHRASE:
            log_warn("⛔ 拒絕：Webhook 密碼錯誤")
            return jsonify({"code": 403, "msg": "Invalid passphrase"}), 403

        # 2️⃣ 驗證必要欄位
        required_fields = ["strategy_name", "symbol", "action", "qty"]
        for field in required_fields:
            if field not in data:
                log_warn(f"⛔ 拒絕：缺少欄位 {field}")
                return jsonify({"code": 400, "msg": f"Missing field: {field}"}), 400

        # 3️⃣ 比對延遲（timestamp 可選）
        if "timestamp" in data:
            lag_sec = now_ts - int(data["timestamp"])
            data["lag_sec"] = lag_sec
            if lag_sec > 30:
                log_warn(f"⚠️ Webhook 延遲過久：{lag_sec} 秒")

        log_info(f"📩 Webhook 收到：{json.dumps(data)}")

        # 4️⃣ 傳遞給 order_manager 處理邏輯
        result = handle_order(data)

        return jsonify({
            "code": 200,
            "msg": "Webhook received",
            "result": result
        }), 200

    except Exception as e:
        log_error(f"❌ Webhook 處理錯誤：{e}")
        return jsonify({"code": 500, "msg": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
