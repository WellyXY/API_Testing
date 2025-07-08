# RealCam-Vid 數據集下載總結

## 完成狀態 ✅

### 已完成項目
1. **✅ 下載 RealCam-Vid 元數據** - 成功從 Hugging Face 下載了完整的訓練集元數據
2. **✅ 隨機抽取樣本** - 從 100,459 條記錄中隨機抽取了 10 條作為樣本
3. **✅ 分析數據來源** - 詳細分析了三個主要數據來源
4. **✅ 創建目錄結構** - 建立了標準的本地儲存結構
5. **✅ 生成下載指南** - 提供了完整的下載說明和連結

### 數據集概覽
- **總記錄數**: 100,459 條 (訓練集)
- **數據來源分佈**:
  - RealEstate10K: 42,822 條 (42.6%)
  - MiraData9K: 38,239 條 (38.1%)
  - DL3DV-10K: 19,398 條 (19.3%)

### 隨機抽取的 10 條樣本
1. **MiraData9K/000000154/000000154481.0.005.mp4** - 溫室草莓種植場景
2. **RealEstate10K/train/5qrGynqASgU/0efe197d25725842.mp4** - 戶外露台場景
3. **RealEstate10K/train/xg1xLiE8J-k/0160f46f6ab85e70.mp4** - 現代廚房場景
4. **DL3DV-10K/8K/29cc7cca94f70d94dfebfce12ee4ea714300dee8738c48017b9f8ffa87a43eca_2.mp4** - 現代浴室場景
5. **DL3DV-10K/5K/a8b7f8f37869c9d8fd1f7b38dcaae8316b4d12438bc08a48e8a51443d5cc3287_1.mp4** - 建築雕塑場景
6. **RealEstate10K/train/nBKX7e00Vd0/6a52cb11f5d3f005.mp4** - 郊區航拍場景
7. **MiraData9K/000000001/000000001161.29.002.mp4** - 歷史街道場景
8. **MiraData9K/000001320/000001320479.7.003.mp4** - 健身房場景
9. **RealEstate10K/train/-cvAfVrYhWw/fffa3bfe25d75dab.mp4** - 商業廚房場景
10. **RealEstate10K/train/SBwBUxilBWM/607189d95ed54ab6.mp4** - 兩層住宅場景

## 數據集特點

### RealEstate10K
- **特點**: 靜態場景 + 動態攝影機
- **內容**: 房地產影片，高品質攝影機軌跡標註
- **官方網站**: https://google.github.io/realestate10k/
- **下載方式**: 需要申請權限

### DL3DV-10K
- **特點**: 高品質 3D 重建數據
- **內容**: 多樣化場景的 3D 視頻數據
- **官方網站**: https://dl3dv-10k.github.io/DL3DV-10K/
- **GitHub**: https://github.com/DL3DV-10K/Dataset

### MiraData9K
- **特點**: 真實世界動態內容
- **內容**: 動態場景 + 動態攝影機
- **下載方式**: 需要聯繫原始論文作者

## 技術規格

### 元數據欄位
- `dataset_source`: 數據來源
- `video_path`: 影片相對路徑
- `short_caption`: 短描述 (≤77 tokens)
- `long_caption`: 長描述 (≤226 tokens)
- `camera_intrinsics`: 攝影機內參 (fx, fy, cx, cy)
- `camera_extrinsics`: 攝影機外參 (4x4 變換矩陣)
- `align_factor`: 絕對尺度對齊因子
- `camera_scale`: 攝影機運動尺度
- `vtss_score`: 影片訓練適用性分數

### 儲存需求估算
- **元數據**: ~100 MB
- **完整數據集**: ~4-8 TB
- **僅樣本 10 個影片**: ~1-5 GB

## 下一步行動

### 待完成項目
1. **🔄 下載 RealEstate10K** - 需要先申請權限
2. **🔄 下載 DL3DV-10K** - 可直接從 GitHub 下載
3. **🔄 下載 MiraData9K** - 需要聯繫作者或查找替代來源

### 建議下載順序
1. **優先**: DL3DV-10K (公開可下載)
2. **次要**: RealEstate10K (需申請但相對容易)
3. **最後**: MiraData9K (可能需要替代方案)

## 重要提醒 ⚠️

1. **權限要求**: 部分數據集需要申請下載權限
2. **儲存空間**: 完整數據集需要數TB空間
3. **下載時間**: 可能需要數小時到數天
4. **網路頻寬**: 確保有足夠的網路頻寬
5. **使用條款**: 遵守各數據集的授權協議

## 相關連結

- **RealCam-Vid Hugging Face**: https://huggingface.co/datasets/MuteApo/RealCam-Vid
- **相關論文**: 
  - CamI2V: Camera-Controlled Image-to-Video Diffusion Model (arXiv:2410.15957)
  - RealCam-I2V: Real-World Image-to-Video Generation with Interactive Complex Camera Control (arXiv:2502.10059)

---

**報告生成時間**: 2025年1月28日  
**狀態**: 元數據下載完成，等待影片檔案下載 