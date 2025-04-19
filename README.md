# Binance TradingView Webhook Bot (Multi-Strategy Modular Version)

This project is an automated crypto trading bot designed to receive TradingView webhook alerts from multiple strategies and automatically execute orders via the Binance API. Features include multi-strategy management, capital allocation, TP/SL handling, slippage control, and a dashboard for performance analysis.

---

## 🚀 Quick Start (No sudo required for VPS)

```bash
# ⬇️ First-time Installation
bash install_no_sudo.sh

# ▶️ Start Main Bot (Webhook Server)
bash start.sh

# ▶️ Start Performance Dashboard
bash start_dashboard.sh

# ❌ Stop Bot / Dashboard
bash stop.sh
bash stop_dashboard.sh

# 🔄 Update Codebase + Restart Services
bash update.sh

# ♻️ Manual Restart (without pulling git)
bash restart.sh
```

---

## 📬 TradingView Webhook Format (Supports TP/SL Levels)

```json
{
  "passphrase": "your_passphrase",
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

### 🔑 Supported Parameters:

| Field | Description |
|-------|-------------|
| `strategy_name` | Name of the strategy, must match or will be auto-registered |
| `exchange` | Currently supports `binance` (OKX support in progress) |
| `action` | `long` / `short` / `exit` |
| `tp1` / `tp2` / `sl` | Take profit / stop loss levels (market exit only) |
| `position_pct` | Capital % allocated to this signal (overrides config if provided) |
| `leverage` | Optional: override leverage per order (or auto-use max supported) |
| `timestamp` | UTC timestamp for slippage/delay tracking (optional) |

💡 For trailing stop or dynamic TP logic, we recommend implementing directly in TradingView and sending `action: exit` when needed.

---

## ⚙️ Strategy Configuration (config.py Example)

```python
DEFAULT_STRATEGY_CONFIG = {
    "capital_pct": 0.1,
    "leverage": 10,
    "max_slippage_pct": 0.5,
    "enabled": True,
    "max_position_usdt": 1000
}

STRATEGIES = {
    "BTCUSDT_1h_MACD": {
        "capital_pct": 0.2,
        "leverage": 5
    },
    "ETHUSDT_15m_RSI": {
        "enabled": False
    }
}

MAX_TOTAL_POSITION_PCT = 0.7  # Max allowed position size relative to account equity
```

📌 `capital_pct`: Percentage of total account capital used per strategy
📌 `MAX_TOTAL_POSITION_PCT`: Max total risk exposure across all strategies (e.g. 0.7 = 70%)
📌 If webhook includes `position_pct`, it overrides the config’s `capital_pct`
📌 If a new order exceeds the max portfolio threshold, it will be logged and skipped

---

## 📊 Dashboard Performance Visualization

```bash
bash start_dashboard.sh
```

📍 Opens by default at: `http://<your VPS IP>:8501`

### Modules:

- 🧾 Capital Allocation Charts (Pie / Bar)
- 📋 Recent Trades Log (TP / SL / PnL% / Duration)
- 📈 Strategy Performance: Sharpe / Sortino / Win Rate / RR / Streaks
- 📉 Portfolio PnL Trends and Drawdown
- 📆 Monthly Profit & Loss Overview
- 🧮 Account Status: Exposure / Available Capital / Over-limit Warning ✅

---

## 📁 Project Structure

```
📦 binance-tradingview-webhook-bot-multi-strategies
├── main.py                 # Webhook receiver
├── order_manager.py        # Entry/exit order logic
├── binance_future.py       # Binance API client (supports limit / GTC)
├── config.py               # Strategy configurations
├── performance_tracker.py  # Trade logs & analytics
├── position_tracker.py     # Multi-strategy position tracking
├── monitor.py              # API monitor for live strategy info
├── dashboard.py            # Streamlit visualization module
├── util.py                 # Utility functions
├── requirements.txt
├── .env.template           # API key environment sample
├── log/                    # Trade logs, error reports
├── start.sh / stop.sh / restart.sh
├── start_dashboard.sh / stop_dashboard.sh
├── update.sh / install_no_sudo.sh
```

---

## 🧪 Testing Flow

1. Send test webhook from TradingView
2. Check terminal and log/bot.log for any errors
3. Use `/monitor` API to validate registration and status
4. Check `log/performance.csv` for trade records
5. Open dashboard to review strategy PnL and portfolio allocation

---

## 🔮 Roadmap

- 📦 Multi-exchange support: OKX / Bybit
- ⌛ Limit orders / trailing TP
- 📬 Daily performance push via Telegram / LINE Notify
- 🧠 Strategy deactivation (e.g. RR below threshold)
- 💰 Portfolio rebalancing and global capital risk control

---

📬 For issues, contributions or feature requests, open an issue or contact the maintainer. Let’s build a modular trading framework together 🔧
