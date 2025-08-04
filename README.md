# Pika API 工具集

這個文件夾包含了所有與 Pika API 視頻生成相關的工具和文件。

## 📁 文件說明

### 🚀 核心 API 工具
- **`new-api.py`** - 最新的 Pika API 接口，支援多種生成功能：
  - Pikadditions（視頻特效添加）
  - Pikascenes（場景生成）
  - Pikaswaps（內容替換）
  - Pikaframes（關鍵幀生成）
  - Pikatwists（視頻變換）

### 🌐 代理服務器
- **`pika_proxy_server.py`** - Pika API 代理服務器
  - 支援 Original 和 Staging 兩種 API 環境
  - 提供 CORS 支援和錯誤處理
  - 配合 `pika_api_frontend.html` 使用

### 🎯 批量生成工具
- **`pika_api_frontend.html`** - 批量圖片轉視頻的前端界面
  - 支援多種 API 版本（v0, v2.2, Turbo）
  - 支援最多50張圖片批量上傳
  - 智能批量處理系統（可調整批次大小和延遲）
  - 實時進度監控和狀態追蹤
  - 並行處理和錯誤處理
  - 一鍵下載所有完成的視頻

### 📦 批量處理系統
- **`pika_batch_server.py`** - 批量視頻生成後端服務器
- **`pika_batch_frontend.html`** - 批量處理的前端界面
- **`batch_frontend.html`** - 簡化版批量處理界面
- **`start_batch_server.py`** - 批量服務器啟動腳本

### 📋 配置和文檔
- **`requirements.txt`** - Python 依賴包列表
- **`vercel.json`** - Vercel 部署配置文件
- **`README_BATCH.md`** - 批量處理系統的詳細說明
- **`test_batch_50.html`** - 50張圖片批量處理功能測試說明

## 🛠️ 使用方法

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 啟動代理服務器（推薦）
```bash
python pika_proxy_server.py
```
然後在瀏覽器中打開 http://localhost:8000

### 3. 啟動批量處理服務器
```bash
python start_batch_server.py
```
然後在瀏覽器中打開 http://localhost:5000

### 4. 直接使用 API
```python
from new-api import generate_pikascenes_turbo
# 使用各種 API 功能
```

## 🔧 API 配置

### Original API
- 基礎 URL: `https://qazwsxedcrf3g5h.pika.art`
- 支援版本: v0
- 需要 API Key

### Staging API  
- 基礎 URL: `https://089e99349ace.pikalabs.app`
- 支援版本: v0
- 使用相同的 API Key（與Original環境相同）

## 💡 功能特點

- ✅ 支援 Pika API v0 版本
- ✅ 支援最多50張圖片批量處理
- ✅ 智能批量處理系統（可調整批次大小和延遲）
- ✅ 實時進度監控和狀態追蹤
- ✅ 批次內並行處理，批次間智能延遲
- ✅ 自動視頻下載和一鍵批量下載
- ✅ 完善的錯誤處理和重試機制
- ✅ 跨域請求支援和代理服務器
- ✅ 響應式網頁界面和進度可視化

## 📝 注意事項

1. 確保有有效的 Pika API Key
2. 批量處理時請注意 API 速率限制，建議使用較小的批次大小（3-5個任務）
3. 處理大量圖片時請耐心等待，系統會自動管理任務隊列
4. 如果遇到API限制錯誤，可以增加批次間延遲時間
5. 大文件上傳可能需要調整服務器超時設置
6. 建議在 HTTPS 環境下使用以獲得最佳體驗

## 🔧 批量處理建議設置

- **小批量（1-10張圖片）**: 批次大小3-5，延遲2-5秒
- **中批量（11-25張圖片）**: 批次大小3，延遲5-10秒  
- **大批量（26-50張圖片）**: 批次大小3，延遲10-30秒 