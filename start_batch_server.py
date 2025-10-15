#!/usr/bin/env python3
"""
Parrot 批量視頻生成器啟動腳本
"""

import os
import sys
import subprocess

def install_dependencies():
    """安裝必要的依賴包"""
    print("🔄 安裝依賴包...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ 依賴包安裝完成")
    except subprocess.CalledProcessError:
        print("❌ 依賴包安裝失敗，請檢查網路連接")
        return False
    return True

def create_directories():
    """創建必要的目錄"""
    print("📁 創建必要目錄...")
    directories = ['uploads', 'generated_videos', 'downloads']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ 目錄創建完成")

def start_server():
    """啟動服務器"""
    print("🚀 啟動 Parrot 批量視頻生成服務器...")
    print("📱 前端頁面: http://localhost:5004")
    print("🔧 API 端點: http://localhost:5004/batch/generate")
    print("⚠️  請確保你有有效的 Parrot API Key")
    print("-" * 50)
    
    try:
        # 導入並運行服務器
        from parrot_batch_server import app
        app.run(
            host='0.0.0.0',
            port=5004,
            debug=True
        )
    except ImportError:
        print("❌ 找不到 parrot_batch_server.py 文件")
    except Exception as e:
        print(f"❌ 啟動服務器失敗: {e}")

def main():
    print("=" * 60)
    print("🎬 Parrot 批量視頻生成器啟動程序")
    print("=" * 60)
    
    # 檢查 requirements.txt 是否存在
    if not os.path.exists('requirements.txt'):
        print("❌ 找不到 requirements.txt 文件")
        return
    
    # 檢查主要文件是否存在
    required_files = ['parrot_batch_server.py', 'batch_frontend.html']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 找不到必要文件: {file}")
            return
    
    # 安裝依賴
    if not install_dependencies():
        return
    
    # 創建目錄
    create_directories()
    
    # 啟動服務器
    start_server()

if __name__ == '__main__':
    main() 