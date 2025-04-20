# Binance TradingView Webhook Bot (Modular Multi-Strategy)

This project is an automated trading bot that receives webhook signals from multiple TradingView strategies and places real-time orders via the Binance API. It supports modular strategy management, capital allocation, TP/SL control, slippage checking, and performance dashboard.

---

## 🚀 Quick Start (No `sudo` Needed, VPS-Friendly)

```bash
# ⬇️ First-time installation
bash install_no_sudo.sh

# ▶️ Start the main bot (Webhook Server)
bash start.sh

# ▶️ Start the Dashboard
bash start_dashboard.sh

# ❌ Stop main / dashboard
bash stop.sh
bash stop_dashboard.sh

# 🔄 Update repo + restart services
bash update.sh

# ♻️ Manual restart (without git pull)
bash restart.sh
```

---

## 📬 TradingView Webhook Format (Supports TP/SL Levels)

```json
{
  "passphrase": "your_secret",
  "strategy_name": "BTCUSDT_1h_MACD",
  "symbol": "BTCUSDT",
  "exchange": "binance",
  "action": "long",
  "price": 68000,
  "tp1": 69000,
  "tp2": 70000,
  "sl": 67000,
  "position_pct": 0.2,
  "leverage": 20,
  "timestamp": 1713696633
}
```

### 🔑 Supported Parameters

| Field | Description |
|-------|-------------|
| `strategy_name` | Strategy name; matches config or auto-registers |
| `exchange` | Currently supports `binance` (OKX coming soon) |
| `action` | `long` / `short` / `exit` |
| `tp1`, `tp2`, `sl` | Optional TP/SL levels; always market exit |
| `position_pct` | Position size as % of total capital (overrides config if provided) |
| `leverage` | ✅ Per-trade leverage override (fallbacks to config or fetches max) |
| `timestamp` | Optional UTC time for slippage latency check |

💡 Want trailing TP or dynamic exits? Handle exit logic in TradingView and use `action: exit` to notify the bot.

---

## ⚙️ Strategy Configuration via `.env` and `config.py`

You only need to update `.env` to set all key parameters.

### ✅ Example `.env`

```env
# Switch to testnet/live
USE_TESTNET=true

# Binance API keys
BINANCE_TEST_API_KEY=xxx
BINANCE_TEST_API_SECRET=xxx
BINANCE_LIVE_API_KEY=xxx
BINANCE_LIVE_API_SECRET=xxx

# Webhook passphrase
PASSPHRASE=your_secret

# Global position limit
MAX_TOTAL_POSITION_PCT=0.7

# Default strategy config
DEFAULT_CAPITAL_PCT=0.05
DEFAULT_LEVERAGE=5
DEFAULT_MAX_QTY=0.03
DEFAULT_MAX_SLIPPAGE_PCT=0.5
DEFAULT_MAX_POSITION_USDT=1000
```

### ✅ `config.py` strategy override (optional)

```python
STRATEGIES = {
  "BTCUSDT_1h_MACD": {
    "capital_pct": 0.1,
    "leverage": 10
  },
  "ETHUSDT_15m_RSI": {
    "enabled": False
  }
}
```

---

## 📊 Dashboard (Performance & Risk Monitor)

```bash
bash start_dashboard.sh
```

Open in browser: `http://<your-VPS-IP>:8501`

### Modules included:

- 🧾 Fund allocation (pie / bar chart)
- 📋 Recent trades (TP / SL / PnL% / holding seconds)
- 📈 Per-strategy metrics: Sharpe, Sortino, WinRate, RR, streaks
- 📉 Total PnL trend and max drawdown
- 📆 Monthly profit/loss summary
- 🧮 Account capital overview, max limit warnings ✅
- 🎯 Live vs max leverage per strategy
- ⚙️ `.env` & config visualization
- 🧪 Mock slippage calculator + webhook test tool

---

## 📁 Project Structure

```
📦 binance-tradingview-webhook-bot-multi-strategies
├── main.py                 # Webhook entry
├── order_manager.py        # Strategy logic handler
├── binance_future.py       # Binance API wrapper (market/limit/SL)
├── config.py               # Loads .env & strategy overrides
├── performance_tracker.py  # Trade history & performance analysis
├── position_tracker.py     # Tracks active positions
├── monitor.py              # Real-time API monitor
├── dashboard.py            # Streamlit dashboard
├── util.py                 # Helper tools (e.g., slippage calc)
├── requirements.txt
├── .env.template           # API keys & default settings
├── log/                    # Logs and performance.csv
├── start.sh / stop.sh / restart.sh
├── start_dashboard.sh / stop_dashboard.sh
├── update.sh / install_no_sudo.sh
```

---

## 🧪 Testing Checklist

1. Send test signal from TradingView webhook
2. Check terminal/log/bot.log for errors (e.g. position limit exceeded)
3. Visit `/monitor` API to confirm bot registered strategy
4. Open `log/performance.csv` for trade records
5. Visit Dashboard for charts, capital allocation, and metrics

---

## 🔮 Roadmap & Coming Soon

- 📦 Multi-exchange support: OKX / Bybit
- ⌛ Limit orders & trailing TP logic
- 📬 Daily Telegram / LINE PnL reports
- 🧠 Strategy router (auto-disable low-RR strategies)
- 💰 Portfolio risk engine (max total exposure enforcement)

---

📬 Questions? Open an Issue or contact the author to help evolve the modular trading stack 🔧
