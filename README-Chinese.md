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

## 📦 安裝說明

### 1️⃣ 複製專案
```bash
git clone https://github.com/你的帳號/binance-tradingview-webhook-bot-multi-strategies.git
cd binance-tradingview-webhook-bot-multi-strategies
```

### 2️⃣ 設定環境變數
建立 `.env` 檔案：
```bash
cp .env.template .env
```
編輯 `.env` 並填入你的 Binance API 金鑰與密碼。

### 3️⃣ 啟動 bot（自動安裝 + 背景執行）
```bash
bash start.sh
```
查看 log：
```bash
tail -f log/bot.log
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

> 策略名稱與 symbol 將會自動註冊進 config

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
| `start.sh` | 一鍵安裝 + 啟動 bot |
| `.env.template` | 環境變數樣板 |
| `log/` | log 與績效資料儲存 |

---

## 📮 進階功能（可擴充）

- Line Notify / Telegram 實時通報
- 自建 Dashboard 前端狀態監控
- TradingView 回測報表串接
- 多帳戶自動倉位平衡管理

---

如需協助部署、擴充功能或交易模型優化，歡迎提出 Issue 🙌
