# 🚀 部署指南

## 📋 準備工作

✅ 代碼已準備完成，包含以下文件：
- `index.html` - 主前端頁面（已硬編碼 API Key）
- `api/generate.py` - 生成視頻 API 函數
- `api/videos.py` - 查詢狀態 API 函數
- `vercel.json` - Vercel 配置文件
- `requirements.txt` - Python 依賴
- `package.json` - 項目配置

## 🔧 GitHub 設置

### 1. 創建 GitHub 倉庫

1. 訪問 [GitHub](https://github.com) 並登錄
2. 點擊右上角的 "+" 號，選擇 "New repository"
3. 設置倉庫信息：
   - **Repository name**: `pika-api-frontend`
   - **Description**: `🎬 Pika API 圖片轉視頻生成器 - 支持多任務並行處理`
   - **Visibility**: Public
   - ❌ 不要勾選 "Add a README file"（我們已經有了）

### 2. 推送代碼到 GitHub

在終端中執行以下命令：

```bash
# 添加遠程倉庫（替換 YOUR_USERNAME 為您的 GitHub 用戶名）
git remote add origin https://github.com/YOUR_USERNAME/pika-api-frontend.git

# 推送代碼到 GitHub
git branch -M main
git push -u origin main
```

## 🌐 Vercel 部署

### 方式一：通過 Vercel 網站（推薦）

1. 訪問 [Vercel](https://vercel.com) 並用 GitHub 賬戶登錄

2. 點擊 "New Project"

3. 選擇您剛創建的 `pika-api-frontend` 倉庫

4. 配置項目：
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: `echo "Build complete"`
   - **Output Directory**: 留空
   - **Install Command**: `pip install -r requirements.txt`

5. 點擊 "Deploy" 開始部署

6. 等待部署完成（通常 1-2 分鐘）

### 方式二：一鍵部署按鈕

1. 在 GitHub 倉庫的 README.md 中更新部署按鈕 URL：
   ```markdown
   [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/pika-api-frontend)
   ```

2. 點擊按鈕即可一鍵部署

## 🔑 API Key 配置

### 當前狀態
- ✅ API Key 已硬編碼在前端：`pk_GW7ITxUVnC271AoJaasgdATrmzjl4OnQKTmD2j6tLZM`
- ✅ Base URL 已設置為相對路徑（適用於 Vercel）

### 安全性說明
⚠️ **注意**：API Key 暴露在前端代碼中，任何人都可以查看並使用。

🔒 **建議**（可選）：如需更高安全性，可在 Vercel 中設置環境變量：
1. 在 Vercel 項目設置中添加環境變量：`PIKA_API_KEY=pk_GW7ITxUVnC271AoJaasgdATrmzjl4OnQKTmD2j6tLZM`
2. 修改 API 函數讀取環境變量而非前端傳入

## 🎯 部署完成

部署成功後，您將獲得：
- 🌐 **Vercel URL**: `https://your-project-name.vercel.app`
- 📱 **功能完整**: 圖片上傳、多任務處理、實時監控
- ⚡ **CDN 加速**: 全球快速訪問
- 🔄 **自動部署**: GitHub 推送自動觸發重新部署

## 🐛 故障排除

### 常見問題

1. **部署失敗**：
   - 檢查 `requirements.txt` 中的包版本
   - 確認 Python 版本兼容性

2. **API 調用失敗**：
   - 檢查 Vercel 函數日誌
   - 確認 API Key 有效性

3. **CORS 錯誤**：
   - 檢查 `vercel.json` 中的 headers 配置
   - 確認 API 函數返回了正確的 CORS 頭

### 調試方法

1. **查看 Vercel 日誌**：
   - 進入 Vercel 項目控制台
   - 查看 "Functions" 標籤頁的實時日誌

2. **本地測試**：
   ```bash
   python pika_proxy_server.py
   ```

## 📞 支持

如果遇到問題，可以：
- 📧 檢查 Vercel 部署日誌
- 🔍 查看瀏覽器開發者工具
- 📝 在 GitHub 倉庫中提交 Issue

---

🎉 **恭喜！您的 Pika API 視頻生成器已準備好部署！** 