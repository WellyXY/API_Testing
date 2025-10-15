#!/usr/bin/env python3
"""
Seedream API 测试脚本
支持 Seedream 3.0 和 4.0 图像生成测试
"""

import requests
import json
import time
import os

# API 配置
API_KEY = "70f23192-0f0c-47d2-9bbf-961f70a17a92"
BASE_URL = "https://ark.ap-southeast.bytepluses.com/api/v3"

# 模型配置
MODELS = {
    "seedream_3.0": "ep-20250806055257-l5f4r",
    "seedream_4.0": "ep-20250921042133-t769x"
}

def test_seedream_generation(model_name, prompt, output_dir="output"):
    """
    测试 Seedream 图像生成
    """
    print(f"\n🎨 测试 {model_name}")
    print(f"📝 提示词: {prompt}")
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # API 请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # 请求数据 (根据BytePlus ModelArk文档格式)
    data = {
        "model": MODELS[model_name],
        "prompt": prompt,
        "n": 1,  # 生成图片数量
        "size": "1024x1024",  # 图片尺寸
        "response_format": "url"  # 返回格式
    }
    
    try:
        # 发送请求
        print("⏳ 发送请求...")
        response = requests.post(
            f"{BASE_URL}/images/generations",
            headers=headers,
            json=data,
            timeout=60
        )
        
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 请求成功!")
            print(f"📄 响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 如果有图片URL，尝试下载
            if "data" in result and len(result["data"]) > 0:
                for i, item in enumerate(result["data"]):
                    if "url" in item:
                        download_image(item["url"], f"{output_dir}/{model_name}_{int(time.time())}_{i}.png")
            
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"📄 错误信息: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ 请求超时")
    except requests.exceptions.RequestException as e:
        print(f"🚫 请求异常: {e}")
    except Exception as e:
        print(f"💥 未知错误: {e}")

def download_image(url, filename):
    """
    下载生成的图片
    """
    try:
        print(f"⬇️ 下载图片: {filename}")
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ 图片已保存: {filename}")
        else:
            print(f"❌ 下载失败: {response.status_code}")
    except Exception as e:
        print(f"💥 下载错误: {e}")

def main():
    """
    主测试函数
    """
    print("🚀 开始测试 Seedream API")
    print("=" * 50)
    
    # 测试提示词
    test_prompts = [
        "A beautiful sunset over mountains, digital art style",
        "一只可爱的小猫在花园里玩耍，卡通风格",
        "Futuristic city skyline with flying cars, cyberpunk style"
    ]
    
    # 测试 Seedream 3.0
    for prompt in test_prompts[:1]:  # 先测试一个提示词
        test_seedream_generation("seedream_3.0", prompt)
        time.sleep(2)  # 避免请求过快
    
    # 测试 Seedream 4.0
    for prompt in test_prompts[:1]:  # 先测试一个提示词
        test_seedream_generation("seedream_4.0", prompt)
        time.sleep(2)
    
    print("\n🎯 测试完成!")

if __name__ == "__main__":
    main()

