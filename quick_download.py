#!/usr/bin/env python3
"""
RealCam-Vid 數據集快速下載腳本
使用方法：python quick_download.py
"""

import os
import json
import requests
from pathlib import Path
from huggingface_hub import hf_hub_download, login
import time

def check_hf_login():
    """檢查 Hugging Face 登錄狀態"""
    try:
        from huggingface_hub import whoami
        user = whoami()
        print(f"✅ 已登錄 Hugging Face，用戶：{user['name']}")
        return True
    except:
        print("❌ 尚未登錄 Hugging Face")
        return False

def login_hf():
    """登錄 Hugging Face"""
    print("\n🔑 請輸入您的 Hugging Face Token：")
    print("   1. 前往：https://huggingface.co/settings/tokens")
    print("   2. 創建新的 token（需要 read 權限）")
    print("   3. 複製 token 並貼上：")
    
    token = input("Token: ").strip()
    try:
        login(token=token)
        print("✅ 登錄成功！")
        return True
    except Exception as e:
        print(f"❌ 登錄失敗：{e}")
        return False

def download_sample_videos():
    """下載樣本視頻"""
    print("\n📥 開始下載樣本視頻...")
    
    # 讀取樣本數據
    sample_file = "realcam_vid_dataset/RealCam-Vid/realcam_vid_sample.json"
    if not os.path.exists(sample_file):
        print(f"❌ 找不到樣本檔案：{sample_file}")
        return False
    
    with open(sample_file, 'r') as f:
        samples = json.load(f)
    
    success_count = 0
    total_count = len(samples)
    
    for i, sample in enumerate(samples, 1):
        print(f"\n[{i}/{total_count}] 處理：{sample.get('short_caption', 'Unknown')}")
        
        try:
            # 嘗試下載 DL3DV-10K 的視頻
            if sample['data_source'] == 'DL3DV-10K':
                video_hash = sample['video_path'].split('/')[-1].replace('.mp4', '')
                
                try:
                    # 嘗試從 DL3DV-10K-Sample 下載
                    file_path = hf_hub_download(
                        repo_id="DL3DV/DL3DV-10K-Sample",
                        filename=f"videos/{video_hash}.mp4",
                        local_dir=f"realcam_vid_dataset/DL3DV-10K/",
                        repo_type="dataset"
                    )
                    print(f"✅ 下載成功：{file_path}")
                    success_count += 1
                except Exception as e:
                    print(f"⚠️  DL3DV-10K 需要權限：{e}")
            
            # 其他數據源的處理邏輯
            elif sample['data_source'] == 'RealEstate10K':
                print("⚠️  RealEstate10K 需要申請權限")
            elif sample['data_source'] == 'MiraData9K':
                print("⚠️  MiraData9K 數據源不明")
                
        except Exception as e:
            print(f"❌ 下載失敗：{e}")
        
        # 避免請求過於頻繁
        time.sleep(1)
    
    print(f"\n📊 下載完成！成功：{success_count}/{total_count}")
    return success_count > 0

def show_download_guide():
    """顯示詳細下載指南"""
    print("""
🎯 完整下載指南：

1. 【立即可用】DL3DV-10K 樣本：
   - 申請權限：https://huggingface.co/datasets/DL3DV/DL3DV-10K-Sample
   - 審核時間：1-3 天
   - 包含我們樣本中的 2 個視頻

2. 【完整數據】RealEstate10K：
   - 申請權限：https://google.github.io/realestate10k/
   - 審核時間：1-2 週
   - 包含我們樣本中的 5 個視頻

3. 【使用腳本】權限通過後：
   python quick_download.py

4. 【手動下載】如果腳本失敗：
   - 前往 Hugging Face 數據集頁面
   - 點擊 "Files and versions"
   - 直接下載需要的視頻檔案
""")

def main():
    print("🎬 RealCam-Vid 數據集下載工具")
    print("=" * 50)
    
    # 檢查登錄狀態
    if not check_hf_login():
        if input("\n要現在登錄 Hugging Face 嗎？(y/n): ").lower() == 'y':
            if not login_hf():
                print("❌ 登錄失敗，無法繼續下載")
                show_download_guide()
                return
        else:
            show_download_guide()
            return
    
    # 嘗試下載
    print("\n🚀 開始嘗試下載...")
    success = download_sample_videos()
    
    if not success:
        print("\n⚠️  看起來您還沒有相關權限")
        show_download_guide()
    else:
        print("\n🎉 部分下載成功！檢查 realcam_vid_dataset/ 資料夾")

if __name__ == "__main__":
    main() 