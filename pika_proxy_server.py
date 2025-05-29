#!/usr/bin/env python3
"""
Pika API 代理服務器
解決瀏覽器 CORS 跨域問題
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
import json

app = Flask(__name__)
CORS(app)  # 允許所有跨域請求

# Pika API 配置
PIKA_BASE_URL = "https://qazwsxedcrf3g5h.pika.art"

@app.route('/')
def index():
    """提供前端頁面"""
    return send_from_directory('.', 'pika_api_frontend.html')

@app.route('/generate/v0/image-to-video', methods=['POST'])
def generate_video():
    """代理圖片轉視頻請求"""
    try:
        # 獲取 API Key
        api_key = request.headers.get('X-API-KEY')
        if not api_key:
            return jsonify({'error': 'Missing API Key'}), 400

        print(f"收到圖片轉視頻請求，API Key: {api_key[:10]}...")

        # 準備請求數據
        files = {}
        data = {}
        
        # 處理圖片文件
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename:
                files['image'] = (
                    image_file.filename,
                    image_file.stream,
                    image_file.content_type
                )
                print(f"收到圖片文件: {image_file.filename}")

        # 處理提示詞
        if 'promptText' in request.form:
            prompt_text = request.form['promptText']
            if prompt_text.strip():
                data['promptText'] = prompt_text
                print(f"提示詞: {prompt_text}")

        # 發送請求到 Pika API
        headers = {
            'X-API-KEY': api_key,
            'Accept': 'application/json'
        }

        print(f"轉發請求到: {PIKA_BASE_URL}/generate/v0/image-to-video")
        
        response = requests.post(
            f"{PIKA_BASE_URL}/generate/v0/image-to-video",
            headers=headers,
            files=files,
            data=data,
            timeout=30
        )

        print(f"Pika API 響應: {response.status_code}")
        
        # 返回響應
        if response.headers.get('content-type', '').startswith('application/json'):
            return jsonify(response.json()), response.status_code
        else:
            return response.text, response.status_code

    except requests.exceptions.RequestException as e:
        print(f"請求錯誤: {e}")
        return jsonify({'error': f'Network error: {str(e)}'}), 500
    except Exception as e:
        print(f"服務器錯誤: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/videos/<video_id>', methods=['GET'])
def get_video_status(video_id):
    """代理視頻狀態查詢請求"""
    try:
        # 獲取 API Key
        api_key = request.headers.get('X-API-KEY')
        if not api_key:
            return jsonify({'error': 'Missing API Key'}), 400

        print(f"查詢視頻狀態: {video_id}")

        # 轉發請求到 Pika API
        headers = {
            'X-API-KEY': api_key,
            'Accept': 'application/json'
        }

        response = requests.get(
            f"{PIKA_BASE_URL}/videos/{video_id}",
            headers=headers,
            timeout=30
        )

        print(f"視頻狀態響應: {response.status_code}")
        
        # 詳細日誌響應內容
        try:
            response_data = response.json()
            print(f"響應數據: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        except:
            print(f"響應文本: {response.text}")

        # 返回響應
        if response.headers.get('content-type', '').startswith('application/json'):
            return jsonify(response.json()), response.status_code
        else:
            return response.text, response.status_code

    except requests.exceptions.RequestException as e:
        print(f"請求錯誤: {e}")
        return jsonify({'error': f'Network error: {str(e)}'}), 500
    except Exception as e:
        print(f"服務器錯誤: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/test', methods=['GET', 'OPTIONS'])
def test_connection():
    """測試連接端點"""
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        return jsonify({'error': 'Missing API Key'}), 400

    try:
        headers = {
            'X-API-KEY': api_key,
            'Accept': 'application/json'
        }

        # 嘗試訪問 API
        response = requests.get(
            f"{PIKA_BASE_URL}/generate/v0/image-to-video",
            headers=headers,
            timeout=10
        )

        return jsonify({
            'status': 'success',
            'api_status': response.status_code,
            'message': 'Connection test successful'
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 啟動 Pika API 代理服務器...")
    print("📱 前端頁面: http://localhost:5003")
    print("🔧 API 代理: http://localhost:5003/generate/v0/image-to-video")
    
    app.run(
        host='0.0.0.0',
        port=5003,
        debug=True
    ) 