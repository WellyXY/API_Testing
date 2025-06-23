#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import google.generativeai as genai

# 设置API密钥
API_KEY = "AIzaSyAHW0Kj707YP7-l6ZKn4OEIRHE0R4VMRjk"  # 注意：在实际应用中建议使用环境变量存储密钥
genai.configure(api_key=API_KEY)

def get_clipboard_data():
    """从剪贴板获取数据"""
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    data = p.stdout.read()
    return data.decode('utf-8')

def set_clipboard_data(data):
    """将数据设置到剪贴板"""
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(data.encode('utf-8'))
    p.stdin.close()
    p.wait()

def translate_with_gemini(text):
    """使用Gemini API将中文文本翻译为英文"""
    # 配置模型
    model = genai.GenerativeModel('gemini-pro')
    
    # 构建提示词
    prompt = f"Translate the following Chinese text to English. Just return the translation without any explanations or additional text:\n\n{text}"
    
    try:
        # 获取响应
        response = model.generate_content(prompt)
        
        # 返回翻译结果
        if response and hasattr(response, 'text'):
            return response.text.strip()
        else:
            return "Translation failed: No response from API"
    except Exception as e:
        return f"Translation failed: {str(e)}"

def main():
    # 确定输入来源：如果有参数则从标准输入读取，否则从剪贴板读取
    if len(sys.argv) > 1 and sys.argv[1] == "--from-stdin":
        input_text = sys.stdin.read().strip()
        from_clipboard = False
    else:
        input_text = get_clipboard_data().strip()
        from_clipboard = True

    if not input_text:
        print("No text input found")
        return

    # 翻译文本
    translated_text = translate_with_gemini(input_text)
    
    # 输出结果
    if from_clipboard:
        # 将结果写回剪贴板
        set_clipboard_data(translated_text)
        print("Translation completed and copied to clipboard")
    else:
        # 输出到标准输出
        print(translated_text)

if __name__ == "__main__":
    main()