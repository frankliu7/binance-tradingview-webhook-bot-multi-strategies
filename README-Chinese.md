# Binance TradingView Webhook Bot（多策略模組化版）

本專案是一套自動化量化交易機器人，支援接收 TradingView 多策略 webhook 訊號，並透過 Binance API 自動下單。具備多策略管理、資金控管、止盈止損、滑價控制、績效分析 Dashboard 等功能。

---

## 🚀 快速啟動（免 sudo VPS 友善）

```bash
# ⬇️ 第一次安裝
bash install_no_sudo.sh

# ▶️ 啟動主程式（Webhook Server）
bash start.sh

# ▶️ 啟動 Dashboard
bash start_dashboard.sh

# ❌ 停止主程式 / Dashboard
bash stop.sh
bash stop_dashboard.sh

# 🔄 更新程式碼 + 重啟所有服務
bash update.sh

# ♻️ 手動重新啟動（不拉 git）
bash restart.sh
```

---

## 📬 TradingView Webhook 格式（支援 TP/SL 多段）

```json
{
  "passphrase": "你的密碼",
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

### 🔑 支援參數：

| 欄位 | 說明 |
|------|------|
| `strategy_name` | 策略名稱，對應 config 設定或自動註冊 |
| `exchange` | 目前支援 binance（預計支援 okx） |
| `action` | long / short / exit |
| `tp1` / `tp2` / `sl` | 多段止盈 / 止損（選填）皆為市價出場 |
| `position_pct` | 該策略佔總倉位資金比例（若無將使用 config 預設） |
| `leverage` | ✅ 可傳入每次下單槓桿（若無將使用 config 或自動查最大） |
| `timestamp` | 訊號 UTC 時間戳，用於滑價延遲比對（選填） |

💡 若策略需實作「追蹤止盈」，建議直接在 TradingView 策略腳本中實作後由 webhook 發送 action: exit 通知 bot 平倉。

---

## ⚙️ 策略設定 config.py（來自 .env 設定）

使用 `.env` 設定環境變數與預設策略參數。

### ✅ `.env` 關鍵欄位

```env
# 切換實盤/測試網（true=使用測試網）
USE_TESTNET=true

# 測試網 API 金鑰
BINANCE_TEST_API_KEY=xxx
BINANCE_TEST_API_SECRET=xxx

# 實盤 API 金鑰
BINANCE_LIVE_API_KEY=xxx
BINANCE_LIVE_API_SECRET=xxx

# Webhook 密碼驗證
PASSPHRASE=你的密碼

# 全域總倉控管
MAX_TOTAL_POSITION_PCT=0.7

# 預設策略設定
DEFAULT_CAPITAL_PCT=0.05
DEFAULT_LEVERAGE=5
DEFAULT_MAX_QTY=0.03
DEFAULT_MAX_SLIPPAGE_PCT=0.5
DEFAULT_MAX_POSITION_USDT=1000
```

### ✅ config.py 範例設定（由 .env 控制）

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

## 📊 Dashboard 績效儀表板

```bash
bash start_dashboard.sh
```

📍 預設開啟於：http://<你的 VPS IP>:8501

### 包含模組：

- 🧾 資金分配視覺化（圓餅圖 / 長條圖）
- 📋 最近交易明細（TP / SL / PnL% / 持倉秒數）
- 📈 各策略績效：Sharpe / Sortino / 勝率 / RR 比 / 連勝數
- 📉 總體 PnL 趨勢與最大回落分析
- 📆 月度盈虧統計圖表
- 🧮 總體資金狀況：倉位佔用比例 / 可用資金 / 超過上限警示 ✅
- 🎯 每策略最大槓桿 / 實際倉位 / 使用者配置一覽
- ⚙️ `.env` 設定與 config 組態視覺化
- 🧪 滑價測試 / 模擬 webhook 測試器

---

## 📁 專案架構說明

```
📦 binance-tradingview-webhook-bot-multi-strategies
├── main.py                 # Webhook 接收入口
├── order_manager.py        # 處理進出場策略邏輯
├── binance_future.py       # Binance 下單模組（支援限價 / 槓桿自動設置）
├── config.py               # 策略設定檔（.env 驅動）
├── performance_tracker.py  # 交易紀錄與績效分析
├── position_tracker.py     # 倉位追蹤（多策略）
├── monitor.py              # API 顯示策略狀態
├── dashboard.py            # Streamlit Dashboard 報表
├── util.py                 # 公用方法（滑價計算等）
├── requirements.txt
├── .env.template           # API 金鑰與參數範例
├── log/                    # 包含 performance.csv 與錯誤日誌
├── start.sh / stop.sh / restart.sh
├── start_dashboard.sh / stop_dashboard.sh
├── update.sh / install_no_sudo.sh
```

---

## 🧪 測試建議流程

1. 在 TradingView 發送 webhook 測試訊號
2. 觀察終端機與 log/bot.log 有無錯誤（例如超過最大總倉比例）
3. 用 `/monitor` API 確認策略是否註冊與倉位狀況
4. 查看 `log/performance.csv` 是否正確記錄績效
5. 開啟 Dashboard 確認策略盈虧統計與總體資金佔用情況

---

## 🔮 預計功能與 Roadmap

- 📦 支援 OKX / Bybit 等多交易所擴充
- ⌛ 限價掛單 / 止盈移動追蹤（追蹤止盈）
- 📬 每日 Telegram / LINE Notify 績效回報
- 🧠 策略調度器（RR 比低於閾值自動停用）
- 💰 Portfolio 均權配置與風控比重（MAX_TOTAL_POSITION_PCT 支援中）

---

📬 有任何問題請開啟 Issue 或聯繫作者。一起打造模組化量化交易基礎架構 🔧
