# RealCam-Vid 樣本視頻下載指南

## 當前狀態 📊

我們已經成功下載了 **RealCam-Vid 元數據**，並隨機抽取了 **10 條樣本記錄**。但是，實際的視頻檔案需要從原始數據集下載，且大部分都需要申請權限。

### 樣本視頻分佈
- **RealEstate10K**: 5 個視頻 (需要申請權限)
- **DL3DV-10K**: 2 個視頻 (需要申請權限) 
- **MiraData9K**: 3 個視頻 (來源不明，需要聯繫作者)

## 詳細下載指南 🚀

### 1. DL3DV-10K 數據集

#### 📋 申請步驟
1. **訪問 Hugging Face 頁面**：
   - 樣本數據：https://huggingface.co/datasets/DL3DV/DL3DV-10K-Sample
   - 完整數據：https://huggingface.co/datasets/DL3DV/DL3DV-ALL-480P

2. **申請權限**：
   - 點擊 "Request access to this repo"
   - 填寫申請表格，說明使用目的
   - 等待審核通過（通常 1-3 天）

3. **設定 Hugging Face 驗證**：
   ```bash
   # 安裝 huggingface_hub
   pip install huggingface_hub
   
   # 登入 Hugging Face
   huggingface-cli login
   ```

4. **下載樣本數據**：
   ```bash
   # 下載我們樣本中的兩個視頻
   python dl3dv_download.py --odir realcam_vid_dataset/DL3DV-10K \
     --subset 1K --resolution 480P --file_type video \
     --hash a8b7f8f37869c9d8fd1f7b38dcaae8316b4d12438bc08a48e8a51443d5cc3287 \
     --clean_cache
   
   python dl3dv_download.py --odir realcam_vid_dataset/DL3DV-10K \
     --subset 1K --resolution 480P --file_type video \
     --hash 29cc7cca94f70d94dfebfce12ee4ea714300dee8738c48017b9f8ffa87a43eca \
     --clean_cache
   ```

#### 📹 我們的樣本視頻
1. **a8b7f8f37869c9d8fd1f7b38dcaae8316b4d12438bc08a48e8a51443d5cc3287**
   - 描述：現代建築，有大型金屬車輪雕塑
   - 路徑：`DL3DV-10K/5K/a8b7f8f37869c9d8fd1f7b38dcaae8316b4d12438bc08a48e8a51443d5cc3287_1.mp4`

2. **29cc7cca94f70d94dfebfce12ee4ea714300dee8738c48017b9f8ffa87a43eca**
   - 描述：現代浴室，白色瓷磚，有馬桶、洗手台、鏡子
   - 路徑：`DL3DV-10K/8K/29cc7cca94f70d94dfebfce12ee4ea714300dee8738c48017b9f8ffa87a43eca_2.mp4`

### 2. RealEstate10K 數據集

#### 📋 申請步驟
1. **訪問官方網站**：https://google.github.io/realestate10k/

2. **填寫申請表格**：
   - 提供學術機構資訊
   - 說明研究目的
   - 同意使用條款

3. **等待審核**：
   - 通常需要 1-2 週
   - 會收到下載連結的電子郵件

#### 📹 我們的樣本視頻
1. **RealEstate10K/train/5qrGynqASgU/0efe197d25725842.mp4**
   - 描述：舒適的戶外露台，玻璃桌、白色椅子、盆栽植物

2. **RealEstate10K/train/xg1xLiE8J-k/0160f46f6ab85e70.mp4**
   - 描述：現代廚房，白色櫥櫃、不銹鋼水槽、木地板

3. **RealEstate10K/train/nBKX7e00Vd0/6a52cb11f5d3f005.mp4**
   - 描述：郊區社區航拍，房屋、樹木、大片水域

4. **RealEstate10K/train/-cvAfVrYhWw/fffa3bfe25d75dab.mp4**
   - 描述：專業級廚房，不銹鋼設備、瓦斯爐

5. **RealEstate10K/train/SBwBUxilBWM/607189d95ed54ab6.mp4**
   - 描述：舒適的兩層房屋，大型木製露台

### 3. MiraData9K 數據集

#### 🔍 查找來源
MiraData9K 的來源較不明確，可能需要：

1. **聯繫原始論文作者**
2. **查找相關 GitHub 倉庫**
3. **尋找替代的公開數據集**

#### 📹 我們的樣本視頻
1. **MiraData9K/000000154/000000154481.0.005.mp4**
   - 描述：溫室中的草莓種植，展示鮮豔的紅色和茂盛的綠葉

2. **MiraData9K/000000001/000000001161.29.002.mp4**
   - 描述：歷史街道場景，人們穿著復古服裝

3. **MiraData9K/000001320/000001320479.7.003.mp4**
   - 描述：健身房中的人舉重，專注於上半身力量訓練

## 替代方案 🔄

如果無法獲得原始視頻，可以考慮：

### 1. 使用公開的相似數據集
- **Pexels Videos**: https://www.pexels.com/videos/
- **Pixabay Videos**: https://pixabay.com/videos/
- **Unsplash Videos**: https://unsplash.com/

### 2. 創建自己的測試視頻
根據我們樣本的描述，可以錄製相似場景：
- 現代廚房場景
- 戶外露台場景
- 浴室場景
- 建築雕塑場景

### 3. 使用 RealCam-Vid 的其他功能
即使沒有原始視頻，我們仍然可以：
- 分析攝影機軌跡數據
- 研究場景描述
- 開發基於元數據的應用

## 自動化腳本 🤖

我已經創建了以下腳本來協助下載：

1. **`download_realcam_vid.py`** - 下載元數據和樣本分析
2. **`download_sample_videos.py`** - 嘗試下載實際視頻檔案
3. **`dl3dv_download.py`** - DL3DV-10K 官方下載腳本
4. **`download_videos_guide.py`** - 詳細的下載指南

## 檔案結構 📁

```
realcam_vid_dataset/
├── RealCam-Vid/
│   ├── realcam_vid_sample.json      # 10 個樣本的元數據
│   ├── download_summary.md          # 下載總結報告
│   └── video_download_guide.md      # 本指南
│
├── RealEstate10K/
│   └── train/
│       ├── 5qrGynqASgU/
│       │   └── 0efe197d25725842.placeholder.txt
│       └── ...
│
├── DL3DV-10K/
│   ├── 5K/
│   └── 8K/
│
└── MiraData9K/
    ├── 000000001/
    ├── 000000154/
    └── 000001320/
```

## 重要提醒 ⚠️

1. **申請權限需要時間**：DL3DV-10K 和 RealEstate10K 都需要 1-3 週的審核時間
2. **儲存空間需求**：完整數據集需要 TB 級別的空間
3. **使用條款**：必須遵守各數據集的授權協議
4. **學術用途**：大部分數據集僅限學術研究使用

## 聯繫資訊 📧

- **DL3DV-10K**: ling58@purdue.edu
- **RealEstate10K**: 通過官方網站申請
- **MiraData9K**: 需要查找原始論文作者

---

**最後更新**：2025年1月28日  
**狀態**：元數據已下載，視頻檔案需要申請權限 