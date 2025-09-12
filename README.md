# Parrot API Testing Tool

一個用於測試 Parrot Labs API 的工具，支持圖片轉視頻功能，現在支持多個 API 提供商。

## 🌟 功能特點

- 📸 **圖片轉視頻**: 上傳圖片生成視頻
- 🎬 **多提供商支持**: 支持 Original 和 Staging API 環境
- 🔄 **即時狀態查詢**: 自動查詢視頻生成進度
- ⚡ **批量處理**: 支持批量上傳和處理
- 🔧 **代理服務器**: 內建 Flask 代理服務器，解決 CORS 問題
- 💾 **下載功能**: 支援單個和批量視頻下載

## 🔧 API 提供商配置

### Original API
- **基礎 URL**: `https://qazwsxedcrf3g5h.pika.art`
- **API Key**: `pk_fnOLPQFrhk96QscYG9hIUSw-Jn5ygl_ehSUWa9PvwZM`
- **支援版本**: v0
- **端點選項**:
  - `/generate/v0/image-to-video` (默認)
  - `/generate/v0/image-to-video-new`
  - `/generate/v0/image-to-video-inner`
  - `/generate/v0/audio-to-video` (圖片+音頻合成視頻)

### Staging API  
- **基礎 URL**: `https://089e99349ace.pikalabs.app`
- **API Key**: `pk_fnOLPQFrhk96QscYG9hIUSw-Jn5ygl_ehSUWa9PvwZM`
- **支援版本**: v2.2
- **端點**: `/generate/2.2/i2v`

## 🚀 快速開始

### 1. 安裝依賴
```bash
pip3 install -r requirements.txt
```

### 2. 啟動代理服務器
```bash
python3 parrot_proxy_server.py
```
服務器將在 http://localhost:5003 啟動

### 3. 開啟瀏覽器
訪問 http://localhost:5003 開始使用

## 📋 使用說明

1. **選擇 API 提供商**: 從下拉菜單選擇 Original 或 Staging 環境
2. **選擇 API 版本**: 根據選擇的提供商自動顯示可用版本
3. **輸入 API Key**: 可選，留空將使用配置中的默認 Key
4. **測試連接**: 點擊 "Test Connection" 驗證 API 可用性
5. **上傳圖片**: 拖拽或點擊上傳圖片文件
6. **輸入提示詞**: 可選，描述期望的視頻效果
7. **開始生成**: 點擊 "Start Generating Video" 開始處理
8. **查看進度**: 系統會自動查詢並更新視頻狀態
9. **下載視頻**: 生成完成後可下載視頻文件

## 🔍 API 端點

### 代理服務器端點
- `GET /` - 前端頁面
- `POST /generate/v0/image-to-video` - Original API v0 (默認端點)
- `POST /generate/v0/image-to-video-new` - Original API v0 (新端點)
- `POST /generate/v0/image-to-video-inner` - Original API v0 (內部端點)
 - `POST /generate/v0/audio-to-video` - Original API v0 (圖片+音頻)
- `POST /generate/2.2/i2v` - Staging API v2.2 (直接代理)  
- `POST /api/generate` - 靈活端點 (支援多提供商)
- `GET /videos/{video_id}` - 查詢視頻狀態
- `GET /api/info` - 獲取支援的 API 提供商信息

### 請求參數
- `image` - 圖片文件 (必需)
- `promptText` - 提示詞 (可選)
- `provider` - API 提供商 ('original' 或 'staging')
- `version` - API 版本 ('v0' 或 'v2.2')
- `endpoint_type` - 端點類型 (僅 Original API v0: 'image-to-video', 'image-to-video-new', 'image-to-video-inner')
 - `audio` - 音頻文件 (僅 `audio-to-video` 端點必需)

## 🛠️ 技術棧

- **後端**: Python Flask + Flask-CORS + requests
- **前端**: HTML + CSS + JavaScript
- **API**: Parrot Labs API (多提供商)

## 📝 更新日誌

### 最新版本
- ✅ 添加多 API 提供商支持
- ✅ 支援 Original 和 Staging 兩個環境
- ✅ 動態 API 提供商和版本選擇
- ✅ 統一的代理端點架構
- ✅ 改進的錯誤處理和調試信息
- ✅ 支援 Original API v0 的多個端點選項 (image-to-video, image-to-video-new, image-to-video-inner)

### 之前版本
- ✅ 基礎圖片轉視頻功能
- ✅ 批量處理支持
- ✅ 視頻下載功能
- ✅ 代理服務器解決 CORS

## 🔐 安全說明

- API Keys 存儲在配置文件中，請妥善保管
- 生產環境建議使用環境變量管理敏感信息
- 代理服務器僅用於開發測試，生產環境請使用專業的代理方案 