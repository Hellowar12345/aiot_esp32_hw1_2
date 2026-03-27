# AIoT 感測數據收集與視覺化系統 - 實作報告

**開發時間:** 2026年3月28日
**專案路徑:** `C:\Users\linmaggie\.gemini\antigravity\scratch\aiot_demo`

---

## 壹、專案總覽 (Project Overview)

本專案實作了一套完整的區域網路端 AIoT 數據平台。設計目標是模擬 ESP32 邊緣裝置擷取溫濕度與 WiFi 訊號品質，並透過 HTTP 協定將數據上傳至伺服器進行儲存與即時動態展示。

### 1. 系統資料流架構
透過以下架構圖可以清楚了解資料從產生、傳遞、儲存到呈現的完整生命週期：

```mermaid
graph TD
    subgraph 邊緣端 (Edge)
        ESP32[ESP32 模擬器程式\n產生 DHT11 數據]
    end

    subgraph 伺服器端 (Server)
        API[Flask REST API\n提供 /sensor 接收資料]
        DB[(SQLite3 資料庫\n記錄歷史感測數據)]
    end

    subgraph 使用者介面 (Client)
        UI[Streamlit 動態儀表板\n分析與視覺化]
    end

    ESP32 -- "發送 HTTP POST\n(每 5 秒)" --> API
    API -- "寫入 (INSERT)" --> DB
    UI -- "讀取 (SELECT)\n自動定時刷新" --> DB
```

---

## 貳、核心模組實作細節

專案主要由四支核心檔案構成，並建立於獨立的 Python 虛擬環境 (`.venv`) 中運行，確保相依套件庫的乾淨與穩定 (包含 `flask`, `streamlit`, `requests`, `pandas` 等)。

### 1. 後端與資料儲存 (`server.py`)
負責監聽前端與裝置的請求，並自動建置 `aiotdb.db` 資料庫檔案與 `sensors` 資料表。
- **資料表結構**: 包含流水號 (`id`)、時間戳記 (`timestamp`)、溫度 (`temperature`)、濕度 (`humidity`)、裝置 ID (`device_id`)、網路名稱 (`wifi_ssid`) 以及訊號強度 (`wifi_rssi`)。
- **API 路由設計**:
  - `GET /health`：用於快速測試伺服器是否正常運作 (Health Check)。
  - `POST /sensor`：提供給 ESP32 發送 Payload 的主要端點，成功寫入資料庫後會回傳 `HTTP 201`。

### 2. 資料產生器 (`esp32_sim.py`)
這是一支模擬 ESP32 微控制器的腳本，由於我們是在本地端進行系統測試，因此以迴圈取代真實硬體。
- 模擬發送包含隨機浮動的溫濕度數值。
- 同時打包了網路連線的 Metadata (如 SSID 和 RSSI)，模擬真實連網裝置的狀態。
- 預設每隔 5 秒向本地 Flask 伺服器推播一次資料。

### 3. 即時戰情室視覺化 (`app.py`)
前端採用 Streamlit 框架建構，不需撰寫複雜的 HTML/JS，而是直接以 Python 將 SQLite 內的數據渲染成圖表：
- **關鍵指標 (KPI)**：首列顯著顯示最新一筆的「溫度」、「濕度」、「目前連線裝置」與「WiFi 訊號強度」。
- **動態線圖**：提供溫度的歷史走勢圖以及濕度走勢圖，方便觀察環境波動。
- **即時表格**：展示最近 100 筆的原始感測資料。
- 透過 `while True` 搭配 `st.empty` 容器機制，自動於背景抓取最新資料刷新畫面，不需手動重新整理網頁。

---

## 參、系統測試與驗證紀錄

在實際執行環境中，所有元件均已無縫接軌並成功運作：

1. **後端連線**：Flask 成功架設於本地 Port `5000`。透過瀏覽器或命令列造訪 `http://127.0.0.1:5000/health`，成功收到 `{"status": "healthy"}` 的 JSON 正常回應。
2. **數據注入**：啟動 `esp32_sim.py` 後，監聽日誌顯示持續回報 `Status: 201` 的成功寫入訊息。
3. **資料庫驗證**：透過腳本抽測 DB 寫入狀況，成功捕捉到感測器數值，資料總筆數也隨著時間正確增長。
4. **前端存取**：Streamlit 儀表板常駐於 `http://127.0.0.1:8501`，開啟網頁後即時儀表與折線圖皆正常繪製與跳動。

---

## 肆、操作手冊 (如何手動重啟)

若電腦重開機或服務中斷，請開啟 **三個** 獨立的命令提示字元 (CMD / PowerShell)，並依序執行以下指令來喚醒各個子系統：

**視窗 一：啟動 API 伺服器**
```powershell
cd C:\Users\linmaggie\.gemini\antigravity\scratch\aiot_demo
.\.venv\Scripts\python.exe server.py
```

**視窗 二：啟動動態前端介面**
```powershell
cd C:\Users\linmaggie\.gemini\antigravity\scratch\aiot_demo
.\.venv\Scripts\streamlit.exe run app.py
```

**視窗 三：開始發送模擬資料**
```powershell
cd C:\Users\linmaggie\.gemini\antigravity\scratch\aiot_demo
.\.venv\Scripts\python.exe esp32_sim.py
```

> **開發者備註：**所有的歷史數據皆會永久保存在專案目錄下的 `aiotdb.db` 檔案中。若在展演前想要清空圖表、進行全新測試，只需在啟動 Flask 前將該 `.db` 檔案拖曳至垃圾桶刪除即可，系統會自動重生乾淨的資料庫。
