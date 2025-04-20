
from flask import Flask, jsonify
from dotenv import dotenv_values
import config
import position_tracker

app = Flask(__name__)

@app.route("/monitor")
def monitor():
    env = dotenv_values(".env")
    try:
        pos_summary = position_tracker.get_binance_position_summary()
    except Exception as e:
        pos_summary = {"error": str(e)}

    return jsonify({
        "status": "ok",
        "env": {
            "USE_TESTNET": env.get("USE_TESTNET", ""),
            "MAX_TOTAL_POSITION_PCT": env.get("MAX_TOTAL_POSITION_PCT", ""),
            "DEFAULT_LEVERAGE": env.get("DEFAULT_LEVERAGE", "")
        },
        "strategies": {
            name: {
                "enabled": val.get("enabled", True),
                "capital_fraction": val.get("capital_fraction", 0),
                "max_position": val.get("max_position", 0)
            } for name, val in config.STRATEGIES.items()
        },
        "position_summary": pos_summary
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
