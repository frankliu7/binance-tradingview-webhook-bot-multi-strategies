# Binance TradingView Webhook Bot

本專案是一個模組化的幣安自動交易機器人，能接收 TradingView 訊號、依據策略自動下單、風控控管、多策略資金分配、滑價處理與績效紀錄。

---

## ✅ 功能特色

- 多策略 webhook 接收與管理
- 策略自動註冊，無需手動設定 config
- 單策略資金分配、槓桿風控、最大倉位控制
- 即時倉位監控、自動滑價偵測與異常拒單
- 成交紀錄 + PnL 績效儲存（CSV）
- 支援 `.env` 金鑰管理、log 記錄、dashboard 查詢介面

---

## 📦 安裝說明（無 sudo VPS 適用）

### 1️⃣ 複製專案
```bash
git clone https://github.com/你的帳號/binance-tradingview-webhook-bot-multi-strategies.git
cd binance-tradingview-webhook-bot-multi-strategies
```

### 2️⃣ 設定環境變數
```bash
cp .env.template .env
nano .env  # 編輯填入金鑰與密碼
```

### 3️⃣ 執行安裝（自編譯 Python）
```bash
bash install_no_sudo.sh
```

### 4️⃣ 啟動 bot（背景執行）
```bash
bash start_no_sudo.sh
```

---

## 🚀 TradingView Webhook 格式

請將以下格式設定在你的策略 webhook JSON 中：

```json
{
  "strategy_name": "BTC_1h_MACD",
  "symbol": "BTCUSDT",
  "exchange": "binance_future",
  "action": "LONG",  // 或 SHORT / EXIT
  "price": 67500,
  "passphrase": "你的 webhook 密碼"
}
```

---

## 📁 專案結構簡介

| 檔案/資料夾 | 說明 |
|--------------|------|
| `main.py` | webhook 接收與策略分發邏輯 |
| `config.py` | 策略設定，自動註冊參數與金鑰載入 |
| `order_manager.py` | 下單風控、滑價、倉位、績效統一控管 |
| `logger.py` | 錯誤與交易紀錄儲存 |
| `monitor.py` | 倉位與滑價狀態查詢 |
| `performance_tracker.py` | 每筆損益與勝率紀錄 CSV |
| `start_no_sudo.sh` | 背景啟動（無 sudo 適用）|
| `install_no_sudo.sh` | 一鍵安裝 Python + venv + pip（無 sudo）|
| `stop.sh` / `status.sh` / `update.sh` | 管理與狀態工具腳本 |
| `.env.template` | 環境變數樣板檔案 |
| `log/` | 執行記錄與錯誤輸出資料夾 |

---

## 🧩 常用指令集（部署與管理）

| 指令 | 說明 |
|-------|------|
| `bash install_no_sudo.sh` | 編譯安裝 Python + 建立虛擬環境 |
| `bash start_no_sudo.sh` | 啟動 bot 並寫入背景 log |
| `bash stop.sh` | 停止正在運行的 bot |
| `bash status.sh` | 查看 bot 是否有在運行中 |
| `bash update.sh` | 從 GitHub 拉最新程式並重新啟動 bot |
| `tail -f log/bot.log` | 即時查看 bot 執行輸出 log |

---

## 📮 可擴充功能（建議）

- ✅ Line Notify / Telegram 警報通知
- ✅ 前端 Dashboard（Flask + Chart.js）績效視覺化
- ✅ 多帳戶 / 資金動態分配管理

---

如需協助部署、策略設計或擴充自動化，歡迎提出 Issue 或聯絡開發者 🙌
