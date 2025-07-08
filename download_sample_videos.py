#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import requests
import urllib.request
from pathlib import Path
import time

def load_sample_data(filename="realcam_vid_sample.json"):
    """載入樣本數據"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"找不到檔案 {filename}")
        return None

def create_directory_structure(video_path, base_dir="realcam_vid_dataset"):
    """根據video_path創建目錄結構"""
    full_path = Path(base_dir) / video_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    return full_path

def try_download_dl3dv_video(video_path, base_dir="realcam_vid_dataset"):
    """嘗試下載 DL3DV-10K 視頻"""
    if not video_path.startswith("DL3DV-10K"):
        return False
    
    print(f"嘗試下載 DL3DV-10K 視頻: {video_path}")
    
    # DL3DV-10K 可能的下載 URL 模式
    possible_urls = [
        f"https://dl3dv-10k.github.io/DL3DV-10K/data/{video_path}",
        f"https://github.com/DL3DV-10K/Dataset/raw/main/{video_path}",
        f"https://huggingface.co/datasets/DL3DV/DL3DV-10K/resolve/main/{video_path}",
    ]
    
    local_path = create_directory_structure(video_path, base_dir)
    
    for url in possible_urls:
        try:
            print(f"  嘗試從 {url[:50]}... 下載")
            response = requests.head(url, timeout=10)
            if response.status_code == 200:
                print(f"  找到視頻，開始下載...")
                urllib.request.urlretrieve(url, local_path)
                print(f"  ✅ 成功下載到 {local_path}")
                return True
        except Exception as e:
            print(f"  ❌ 下載失敗: {e}")
            continue
    
    print(f"  ⚠️  無法從任何 URL 下載 {video_path}")
    return False

def try_download_realestate_video(video_path, base_dir="realcam_vid_dataset"):
    """嘗試下載 RealEstate10K 視頻（通常需要權限）"""
    if not video_path.startswith("RealEstate10K"):
        return False
    
    print(f"⚠️  RealEstate10K 視頻需要申請權限: {video_path}")
    print("   請訪問 https://google.github.io/realestate10k/ 申請下載權限")
    
    # 創建佔位檔案
    local_path = create_directory_structure(video_path, base_dir)
    placeholder_path = local_path.with_suffix('.placeholder.txt')
    
    with open(placeholder_path, 'w', encoding='utf-8') as f:
        f.write(f"RealEstate10K 視頻佔位檔案\n")
        f.write(f"原始路徑: {video_path}\n")
        f.write(f"下載說明: 請訪問 https://google.github.io/realestate10k/ 申請權限\n")
        f.write(f"申請通過後，請將視頻檔案放置在: {local_path}\n")
    
    print(f"  📝 已創建佔位檔案: {placeholder_path}")
    return False

def try_download_miradata_video(video_path, base_dir="realcam_vid_dataset"):
    """嘗試下載 MiraData9K 視頻"""
    if not video_path.startswith("MiraData9K"):
        return False
    
    print(f"⚠️  MiraData9K 視頻來源不明: {video_path}")
    print("   可能需要聯繫原始論文作者或查找替代來源")
    
    # 創建佔位檔案
    local_path = create_directory_structure(video_path, base_dir)
    placeholder_path = local_path.with_suffix('.placeholder.txt')
    
    with open(placeholder_path, 'w', encoding='utf-8') as f:
        f.write(f"MiraData9K 視頻佔位檔案\n")
        f.write(f"原始路徑: {video_path}\n")
        f.write(f"下載說明: 需要聯繫原始論文作者或查找公開來源\n")
        f.write(f"找到視頻後，請將檔案放置在: {local_path}\n")
    
    print(f"  📝 已創建佔位檔案: {placeholder_path}")
    return False

def download_sample_videos():
    """下載樣本視頻"""
    print("開始下載 RealCam-Vid 樣本視頻...")
    print("=" * 60)
    
    # 載入樣本數據
    sample_data = load_sample_data()
    if not sample_data:
        print("❌ 無法載入樣本數據")
        return
    
    success_count = 0
    total_count = len(sample_data)
    
    for i, record in enumerate(sample_data, 1):
        video_path = record['video_path']
        dataset_source = record['dataset_source']
        
        print(f"\n[{i}/{total_count}] 處理視頻: {video_path}")
        print(f"    來源: {dataset_source}")
        print(f"    描述: {record['short_caption'][:60]}...")
        
        success = False
        
        if dataset_source == "DL3DV-10K":
            success = try_download_dl3dv_video(video_path)
        elif dataset_source == "RealEstate10K":
            success = try_download_realestate_video(video_path)
        elif dataset_source == "MiraData9K":
            success = try_download_miradata_video(video_path)
        else:
            print(f"  ❌ 未知的數據來源: {dataset_source}")
        
        if success:
            success_count += 1
        
        # 添加延遲避免過於頻繁的請求
        time.sleep(1)
    
    print(f"\n" + "=" * 60)
    print(f"下載完成！")
    print(f"成功下載: {success_count}/{total_count} 個視頻")
    print(f"失敗/需要權限: {total_count - success_count}/{total_count} 個視頻")
    
    if success_count == 0:
        print("\n⚠️  沒有成功下載任何視頻檔案")
        print("   這是正常的，因為大部分數據集需要申請權限或特殊來源")
        print("   已為無法下載的視頻創建了佔位檔案，包含下載說明")

def check_downloaded_files():
    """檢查已下載的檔案"""
    base_dir = Path("realcam_vid_dataset")
    
    print(f"\n檢查下載結果...")
    print("=" * 40)
    
    video_files = list(base_dir.rglob("*.mp4"))
    placeholder_files = list(base_dir.rglob("*.placeholder.txt"))
    
    print(f"📹 視頻檔案: {len(video_files)} 個")
    for video_file in video_files:
        size_mb = video_file.stat().st_size / (1024 * 1024)
        print(f"  ✅ {video_file.relative_to(base_dir)} ({size_mb:.1f} MB)")
    
    print(f"\n📝 佔位檔案: {len(placeholder_files)} 個")
    for placeholder_file in placeholder_files:
        print(f"  📋 {placeholder_file.relative_to(base_dir)}")

def main():
    print("RealCam-Vid 樣本視頻下載器")
    print("=" * 60)
    
    # 確保目錄存在
    os.makedirs("realcam_vid_dataset", exist_ok=True)
    
    # 下載視頻
    download_sample_videos()
    
    # 檢查結果
    check_downloaded_files()
    
    print(f"\n💡 提示:")
    print("1. DL3DV-10K 視頻可能需要從官方 GitHub 倉庫下載")
    print("2. RealEstate10K 需要申請權限: https://google.github.io/realestate10k/")
    print("3. MiraData9K 可能需要聯繫原始作者")
    print("4. 已創建佔位檔案，包含詳細的下載說明")

if __name__ == "__main__":
    main() 