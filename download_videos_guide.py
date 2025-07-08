#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from collections import defaultdict

def load_sample_data(filename="realcam_vid_sample.json"):
    """載入樣本數據"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"找不到檔案 {filename}")
        return None

def analyze_video_sources(sample_data):
    """分析影片來源並提供下載指南"""
    if not sample_data:
        return
    
    source_info = defaultdict(list)
    
    for record in sample_data:
        source = record['dataset_source']
        source_info[source].append(record)
    
    print("=== 影片來源分析與下載指南 ===\n")
    
    for source, records in source_info.items():
        print(f"📁 {source} ({len(records)} 條記錄)")
        print("=" * 50)
        
        if source == "RealEstate10K":
            print("🔗 官方網站: https://google.github.io/realestate10k/")
            print("📝 論文: Real Estate 10K: A Large-scale Dataset of Real Estate Images")
            print("💾 下載方式:")
            print("   1. 訪問官方網站")
            print("   2. 填寫申請表格")
            print("   3. 等待審核通過後下載")
            print("📋 包含內容: 房地產影片，攝影機軌跡標註")
            print("💡 特點: 靜態場景 + 動態攝影機")
            
        elif source == "DL3DV-10K":
            print("🔗 官方網站: https://dl3dv-10k.github.io/DL3DV-10K/")
            print("📝 論文: DL3DV-10K: A Large-Scale Scene Dataset for Deep Learning-based 3D Vision")
            print("💾 下載方式:")
            print("   1. 訪問 GitHub: https://github.com/DL3DV-10K/Dataset")
            print("   2. 使用提供的下載腳本")
            print("   3. 需要大量儲存空間 (數TB)")
            print("📋 包含內容: 多樣化場景的 3D 視頻數據")
            print("💡 特點: 高品質 3D 重建數據")
            
        elif source == "MiraData9K":
            print("🔗 相關專案: MiraData")
            print("📝 說明: 動態場景數據集")
            print("💾 下載方式:")
            print("   1. 可能需要聯繫原始論文作者")
            print("   2. 或查找相關開源專案")
            print("   3. 部分數據可能來自公開影片平台")
            print("📋 包含內容: 動態場景 + 動態攝影機")
            print("💡 特點: 真實世界動態內容")
        
        print("\n📹 此來源的樣本影片:")
        for i, record in enumerate(records, 1):
            print(f"   {i}. {record['video_path']}")
            print(f"      描述: {record['short_caption'][:80]}...")
            print(f"      尺度: {record['camera_scale']:.2f}")
        
        print("\n" + "="*80 + "\n")

def create_download_structure():
    """創建建議的目錄結構"""
    print("=== 建議的本地目錄結構 ===\n")
    
    structure = """
realcam_vid_dataset/
├── RealCam-Vid/                    # 元數據
│   ├── train.npz
│   ├── test.npz
│   └── realcam_vid_sample.json
│
├── RealEstate10K/                  # 房地產數據集
│   ├── train/
│   │   ├── 5qrGynqASgU/
│   │   │   └── 0efe197d25725842.mp4
│   │   ├── xg1xLiE8J-k/
│   │   │   └── 0160f46f6ab85e70.mp4
│   │   └── ...
│   └── test/
│
├── DL3DV-10K/                      # 3D 視覺數據集
│   ├── 2K/
│   ├── 5K/
│   │   └── a8b7f8f37869c9d8fd1f7b38dcaae8316b4d12438bc08a48e8a51443d5cc3287_1.mp4
│   ├── 8K/
│   │   └── 29cc7cca94f70d94dfebfce12ee4ea714300dee8738c48017b9f8ffa87a43eca_2.mp4
│   └── ...
│
└── MiraData9K/                     # 動態場景數據集
    ├── 000000001/
    │   └── 000000001161.29.002.mp4
    ├── 000000154/
    │   └── 000000154481.0.005.mp4
    └── ...
    """
    
    print(structure)

def generate_download_commands():
    """生成下載命令範例"""
    print("=== 下載命令範例 ===\n")
    
    print("1. 創建目錄結構:")
    print("mkdir -p realcam_vid_dataset/{RealEstate10K,DL3DV-10K,MiraData9K}")
    print()
    
    print("2. 下載 RealEstate10K (需要先申請權限):")
    print("# 請先到官方網站申請下載權限")
    print("# wget <官方提供的下載連結>")
    print()
    
    print("3. 下載 DL3DV-10K:")
    print("git clone https://github.com/DL3DV-10K/Dataset")
    print("cd Dataset")
    print("# 按照 README 說明下載")
    print()
    
    print("4. 下載 MiraData9K:")
    print("# 需要查找原始數據來源或聯繫作者")
    print()

def estimate_storage_requirements():
    """估算儲存需求"""
    print("=== 儲存空間需求估算 ===\n")
    
    requirements = [
        ("RealCam-Vid 元數據", "~100 MB", "包含所有標註資訊"),
        ("RealEstate10K 完整數據集", "~500 GB", "約 67K 個房地產影片"),
        ("DL3DV-10K 完整數據集", "~2-5 TB", "高品質 3D 視頻數據"),
        ("MiraData9K 完整數據集", "~1-2 TB", "動態場景影片"),
        ("僅樣本 10 個影片", "~1-5 GB", "取決於影片長度和品質")
    ]
    
    for name, size, desc in requirements:
        print(f"📊 {name:<25} {size:<15} {desc}")
    
    print(f"\n💾 完整數據集總計: ~4-8 TB")
    print(f"🎯 僅下載樣本: ~1-5 GB")

def main():
    print("RealCam-Vid 影片下載指南")
    print("=" * 60)
    
    # 載入樣本數據
    sample_data = load_sample_data()
    
    if sample_data:
        # 分析影片來源
        analyze_video_sources(sample_data)
        
        # 創建目錄結構建議
        create_download_structure()
        
        # 生成下載命令
        generate_download_commands()
        
        # 估算儲存需求
        estimate_storage_requirements()
        
        print("\n⚠️  重要提醒:")
        print("1. 這些數據集可能需要申請權限才能下載")
        print("2. 完整數據集需要大量儲存空間 (數TB)")
        print("3. 下載時間可能需要數小時到數天")
        print("4. 請確保有足夠的網路頻寬")
        print("5. 遵守各數據集的使用條款和授權協議")
        
        print(f"\n✅ 成功分析了 {len(sample_data)} 條樣本記錄")
    else:
        print("❌ 無法載入樣本數據，請先執行 download_realcam_vid.py")

if __name__ == "__main__":
    main() 