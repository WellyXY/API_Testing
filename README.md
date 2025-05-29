# Pika API 圖片轉視頻生成器

🎬 一個基於 Pika API 的圖片轉視頻生成器，支持多任務並行處理，實時進度監控。

## ✨ 特色功能

- 📸 **圖片上傳**：支持拖拽和點擊上傳
- ✨ **提示詞生成**：添加自定義描述優化視頻效果
- 🔄 **多任務處理**：支持同時提交多個生成任務
- ⏱️ **實時監控**：顯示每個任務的進度和耗時
- 📊 **統計分析**：計算平均生成時間
- 💾 **視頻下載**：生成完成後直接下載視頻
- 🎨 **現代UI**：響應式設計，美觀易用

## 🚀 快速開始

### 本地開發

1. 克隆倉庫：
```bash
git clone <your-repo-url>
cd pika-api-frontend
```

2. 安裝依賴：
```bash
pip install -r requirements.txt
```

3. 運行本地服務器：
```bash
python pika_proxy_server.py
```

4. 打開瀏覽器訪問：`http://localhost:5003`

### Vercel 部署

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=<your-repo-url>)

1. 點擊上面的 Deploy 按鈕
2. 連接您的 GitHub 賬戶
3. 選擇倉庫並部署
4. 部署完成後即可使用

## 📋 API 配置

- **API Key**：已預設為 `pk_GW7ITxUVnC271AoJaasgdATrmzjl4OnQKTmD2j6tLZM`
- **Base URL**：Vercel 部署時使用相對路徑，本地開發使用 `http://localhost:5003`

## 🛠️ 技術棧

- **前端**：HTML5, CSS3, JavaScript (原生)
- **後端**：Python (Vercel Functions)
- **API**：Pika API (qazwsxedcrf3g5h.pika.art)
- **部署**：Vercel

## 📁 項目結構

```
pika-api-frontend/
├── index.html              # 主前端頁面
├── api/
│   ├── generate.py         # 生成視頻 API
│   └── videos.py           # 查詢狀態 API
├── vercel.json             # Vercel 配置
├── requirements.txt        # Python 依賴
├── package.json            # Node.js 配置
└── README.md              # 項目說明
```

## 🔧 API 端點

- `POST /generate/v0/image-to-video` - 提交視頻生成任務
- `GET /videos/{video_id}` - 查詢視頻生成狀態

## 📊 使用統計

- ⏱️ **平均生成時間**：約 4-5 分鐘
- 🎯 **支持格式**：JPG, PNG, GIF
- 📱 **響應式設計**：支持手機和桌面設備

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 許可證

MIT License

---

Made with ❤️ by AI Assistant 