#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import pandas as pd
from datasets import load_dataset
from huggingface_hub import hf_hub_download
import urllib.request
import json

def download_realcam_vid_metadata():
    """下載 RealCam-Vid 數據集的元數據"""
    print("正在下載 RealCam-Vid 數據集元數據...")
    
    try:
        # 載入數據集
        dataset = load_dataset("MuteApo/RealCam-Vid", split="train")
        print(f"成功載入數據集，共有 {len(dataset)} 條記錄")
        
        # 轉換為 pandas DataFrame 以便處理
        df = dataset.to_pandas()
        print("數據集欄位：", df.columns.tolist())
        
        return df
        
    except Exception as e:
        print(f"下載數據集時發生錯誤：{e}")
        return None

def sample_random_records(df, n=10):
    """隨機抽取 n 條記錄"""
    if df is None or len(df) == 0:
        print("數據集為空")
        return None
        
    # 隨機抽取 n 條記錄
    sampled_df = df.sample(n=min(n, len(df)), random_state=42)
    print(f"隨機抽取了 {len(sampled_df)} 條記錄")
    
    return sampled_df

def analyze_video_sources(df):
    """分析影片來源"""
    if df is None:
        return
        
    print("\n=== 影片來源分析 ===")
    
    # 分析 dataset_source 欄位
    if 'dataset_source' in df.columns:
        source_counts = df['dataset_source'].value_counts()
        print("數據來源分佈：")
        for source, count in source_counts.items():
            print(f"  {source}: {count} 條")
    
    # 分析 video_path 的前綴
    print("\nvideo_path 前綴分析：")
    path_prefixes = df['video_path'].str.split('/').str[0].value_counts()
    for prefix, count in path_prefixes.items():
        print(f"  {prefix}: {count} 條")

def display_sample_info(df):
    """顯示樣本資訊"""
    if df is None:
        return
        
    print("\n=== 隨機抽取的 10 條記錄詳細資訊 ===")
    
    for idx, row in df.iterrows():
        print(f"\n--- 記錄 {idx} ---")
        print(f"數據來源: {row.get('dataset_source', 'N/A')}")
        print(f"影片路徑: {row['video_path']}")
        print(f"短描述: {row['short_caption'][:100]}...")
        print(f"攝影機尺度: {row.get('camera_scale', 'N/A')}")
        print(f"對齊因子: {row.get('align_factor', 'N/A')}")
        print(f"VTSS 分數: {row.get('vtss_score', 'N/A')}")

def save_sample_to_json(df, filename="realcam_vid_sample.json"):
    """將樣本保存為 JSON 檔案"""
    if df is None:
        return
        
    # 轉換為可序列化的格式
    sample_data = []
    for idx, row in df.iterrows():
        record = {
            'index': int(idx),
            'dataset_source': row.get('dataset_source', ''),
            'video_path': row['video_path'],
            'short_caption': row['short_caption'],
            'long_caption': row.get('long_caption', ''),
            'camera_scale': float(row.get('camera_scale', 0)),
            'align_factor': float(row.get('align_factor', 0)),
            'vtss_score': float(row.get('vtss_score', 0))
        }
        sample_data.append(record)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n樣本數據已保存到 {filename}")

def main():
    print("開始下載 RealCam-Vid 數據集...")
    
    # 下載元數據
    df = download_realcam_vid_metadata()
    
    if df is not None:
        # 分析數據來源
        analyze_video_sources(df)
        
        # 隨機抽取 10 條記錄
        sample_df = sample_random_records(df, n=10)
        
        if sample_df is not None:
            # 顯示樣本資訊
            display_sample_info(sample_df)
            
            # 保存樣本到 JSON
            save_sample_to_json(sample_df)
            
            print(f"\n=== 總結 ===")
            print(f"成功載入 {len(df)} 條記錄")
            print(f"隨機抽取 {len(sample_df)} 條記錄")
            print("注意：此腳本只下載了元數據，實際的影片檔案需要從原始數據集下載")
            print("主要數據來源包括：RealEstate10K, DL3DV-10K, MiraData 等")

if __name__ == "__main__":
    main() 