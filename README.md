# Binance TradingView Webhook Bot

## 🚀 VPS Deployment Quick Guide (No sudo required)

1️⃣ Login to your VPS (via Cloudways SSH)
```bash
ssh master_username@<YOUR_VPS_IP>
```

2️⃣ Clone the project
```bash
git clone https://github.com/<your-account>/binance-tradingview-webhook-bot-multi-strategies.git
cd binance-tradingview-webhook-bot-multi-strategies
```

3️⃣ Set up environment variables
```bash
cp .env.template .env
nano .env  # Fill in your Binance API key/secret and webhook passphrase
```

4️⃣ Install environment (compiles Python & creates venv)
```bash
bash install_no_sudo.sh
```

5️⃣ Start the bot in background
```bash
bash start_no_sudo.sh
```

6️⃣ Check if the bot is running
```bash
bash status.sh
# Or view live log:
tail -f log/bot.log
```

---

## ✅ Features

- Multiple strategy support via webhook
- Auto strategy registration (no need to pre-edit config)
- Per-strategy capital allocation, leverage & max position control
- Real-time position monitoring, slippage control & rejection logging
- PnL and trade logs saved per strategy
- `.env` support for API key security and log directory separation

---

## 📦 Installation (For VPS without sudo)

```bash
git clone https://github.com/<your-account>/binance-tradingview-webhook-bot-multi-strategies.git
cd binance-tradingview-webhook-bot-multi-strategies
cp .env.template .env
bash install_no_sudo.sh
bash start_no_sudo.sh
```

---

## 🔔 TradingView Webhook JSON Format

```json
{
  "strategy_name": "BTC_1h_MACD",
  "symbol": "BTCUSDT",
  "exchange": "binance_future",
  "action": "LONG",  // or SHORT / EXIT
  "price": 67500,
  "passphrase": "your_webhook_password"
}
```

---

## 📁 Project Structure

| File/Folder | Description |
|-------------|-------------|
| `main.py` | Webhook endpoint & strategy dispatcher |
| `config.py` | Dynamic config loader and strategy registration |
| `order_manager.py` | Handles risk, slippage, execution, logging |
| `logger.py` | Error and trade logger |
| `monitor.py` | Monitor slippage & open positions |
| `performance_tracker.py` | Tracks entry/exit & PnL to CSV |
| `start_no_sudo.sh` | Start script for non-sudo VPS |
| `install_no_sudo.sh` | Python 3.9 + venv + pip installer |
| `stop.sh / status.sh / update.sh` | Bot lifecycle management scripts |
| `.env.template` | Example env file for sensitive keys |
| `log/` | Logs and CSV export folder |

---

## 🧩 Useful Command Set

| Command | Description |
|---------|-------------|
| `bash install_no_sudo.sh` | Compile Python + set up venv |
| `bash start_no_sudo.sh` | Start bot in background |
| `bash stop.sh` | Stop the running bot |
| `bash status.sh` | Check if bot is running |
| `bash update.sh` | Pull latest from GitHub and restart bot |
| `tail -f log/bot.log` | View live bot logs |

---

## 📮 Future Enhancements

- ✅ Line Notify / Telegram alerting integration
- ✅ Flask-based dashboard for monitoring PnL & positions
- ✅ Multi-account, dynamic capital balancing module

---

For questions, feature requests, or contributions — feel free to open an issue or contact the maintainer 🙌
