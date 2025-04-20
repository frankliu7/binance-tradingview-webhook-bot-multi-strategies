✅ Binance TradingView Webhook Bot - 技術規格 v1.3
📦 基礎架構
系統語言：Python
運作模式：接收 TradingView webhook，執行 Binance 市價單交易
支援市場：Binance Futures（Testnet / Live）
執行流程：webhook 驗證 → 策略驗證 → 倉位風控 → 下單執行 → log 紀錄
🧾 Webhook JSON 結構定義

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
  "qty1": 0.3,
  "qty2": 0.7,
  "position_pct": 0.2,
  "leverage": 20,
  "exit": false,
  "timestamp": 1713696633
}


Webhook 欄位說明：
- strategy_name：策略名稱（必填，自動註冊）
- passphrase：密碼驗證（必填）
- action：long / short / exit（平倉）
- price：webhook 當下價格（用於滑價計算）
- qty1 / qty2：TP1 / TP2 出場比例（加總 = 1）
- tp1 / tp2 / sl：固定止盈 / 止損價位
- position_pct：使用總資金比例（若無，取預設）
- leverage：每筆下單槓桿（若無，使用預設或查最大）
- exit：若為 true 則為動態平倉訊號
- timestamp：webhook 發送時間戳（比對延遲）

⚙️ 系統設定（由 .env 控制）

USE_TESTNET=true
BINANCE_TEST_API_KEY=xxx
BINANCE_TEST_API_SECRET=xxx
BINANCE_LIVE_API_KEY=xxx
BINANCE_LIVE_API_SECRET=xxx
PASSPHRASE=yourpass
MAX_TOTAL_POSITION_USDT=10000
MAX_TOTAL_POSITION_PCT=0.7
DEFAULT_CAPITAL_PCT=0.05
DEFAULT_LEVERAGE=5
DEFAULT_MAX_QTY=0.03
DEFAULT_MAX_SLIPPAGE_PCT=0.5

❌ 拒單邏輯定義（全部記錄 log）

- 策略停用（enabled = false）
- max_position = 0
- 系統總倉滿（超過 MAX_TOTAL_POSITION_USDT）
- webhook 欄位缺失（如 strategy / action / qty）
- 密碼錯誤
- Binance API 錯誤
- 滑價超過容許範圍（可設定閾值）
- webhook 延遲過久（timestamp 差距過大）

🧠 進階功能

- ✅ 滑價分析：webhook 價格與實際成交價格差異分析（% 和 tick）
- ✅ 延遲分析：timestamp 對比系統時間並記錄 lag
- ✅ 自動註冊策略：新策略自動寫入 strategy_config.json
- ✅ 多策略獨立倉控與績效追蹤
- ✅ 日誌分級記錄（info / warning / error / trade）
- ✅ 支援 .env 熱更新
- ✅ Streamlit Dashboard 儀表板整合

📊 Dashboard 功能模組

- 資金分配視覺化（圓餅圖 / 長條圖）
- 最近交易明細（TP / SL / PnL% / 持倉秒數）
- 各策略績效指標：Sharpe / Sortino / 勝率 / RR 比 / 連勝數
- 總體 PnL 趨勢與最大回落分析
- 月度盈虧統計圖表
- 倉位佔用比例、可用資金、超過上限警示
- 每策略最大槓桿 / 實際倉位 / 使用者配置一覽
- .env 與 config 組態視覺化
- 滑價測試 / 模擬 webhook 測試器

📁 專案架構

binance-tradingview-webhook-bot-multi-strategies/
├── main.py                 # Webhook 接收入口
├── order_manager.py        # 處理進出場策略邏輯
├── binance_future.py       # Binance 下單模組
├── config.py               # 策略設定（含自動註冊）
├── performance_tracker.py  # PnL 與績效紀錄
├── position_tracker.py     # 倉位追蹤（本地與 Binance 合併）
├── dashboard.py            # Streamlit Dashboard 顯示介面
├── monitor.py              # 系統監控 API
├── logger.py               # Log 模組（info/error/trade）
├── util.py                 # 共用方法（滑價、延遲等）
├── log/                    # 日誌與績效紀錄資料夾
├── .env.template           # 環境參數範例
├── start.sh / stop.sh / update.sh
├── start_dashboard.sh / stop_dashboard.sh

⚙️ 行為與風控規則

- 市價單下單：所有委託皆使用市價單
- 槓桿自動調整：預設使用最大槓桿，亦可 webhook 指定
- 倉位限制：若總持倉超過 MAX_TOTAL_POSITION_USDT 則拒單
- 拒單條件：密碼錯誤、策略停用、max_position=0、倉位滿、滑價過大、延遲過久等
- 支援 exit=true：動態止盈平倉訊號，不再進場
- 滑價比對：webhook 價格 vs 成交價格 自動分析（% 與 tick）
- 延遲比對：timestamp 對照系統時間，計算 lag 秒數並記錄

📊 Dashboard 強化模組說明（即時狀態總覽）

為提升監控效率，Dashboard 除了顯示績效外，需整合以下即時狀態模組：

1. 📡 Binance 實時倉位：顯示每幣種方向、倉位金額、未實現損益（unrealized PnL）
2. 🧮 系統總倉分析：目前總倉位金額、佔總限制比、剩餘可用資金比例
3. ⚙️ 策略設定顯示：整合 .env 與 strategy_config.json，呈現所有策略啟用狀態與資金佔比
4. 📋 系統設定視覺化：包含 USE_TESTNET、槓桿、max_position 設定等
5. 📁 模組狀態檢查：顯示 config / logger / API / webhook 模組是否啟動、異常檢測紀錄
6. 🧪 滑價與延遲監測：顯示最近 10 策略 webhook 滑價與 lag 秒數分佈

