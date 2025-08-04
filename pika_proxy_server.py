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
import socket
from contextlib import closing

app = Flask(__name__)
CORS(app)  # 允許所有跨域請求

# API 提供商配置
API_PROVIDERS = {
    'staging': {
        'name': 'Staging',
        'base_url': 'https://089e99349ace.pikalabs.app',
        'api_key': 'pk_fnOLPQFrhk96QscYG9hIUSw-Jn5ygl_ehSUWa9PvwZM',  # 更新的 API Token
        'supported_versions': {
            'v2.2': '/generate/2.2/i2v'
        }
    }
}

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

@app.route('/')
def index():
    """提供前端頁面"""
    return send_from_directory('.', 'pika_api_frontend.html')

@app.route('/generate/2.2/i2v', methods=['POST'])
def generate_video():
    """代理圖片轉視頻請求 - 使用staging環境"""
    return _generate_video_internal('staging', 'v2.2')

@app.route('/api/generate', methods=['POST'])
def generate_video_flexible():
    """靈活的生成端點，使用staging環境"""
    provider = request.form.get('provider', 'staging')
    version = request.form.get('version', 'v2.2')
    return _generate_video_internal(provider, version)

def _generate_video_internal(provider='original', api_version='v0'):
    """內部圖片轉視頻處理函數"""
    try:
        # 驗證提供商和版本
        if provider not in API_PROVIDERS:
            return jsonify({'error': f'Unsupported provider: {provider}'}), 400
            
        provider_config = API_PROVIDERS[provider]
        
        if api_version not in provider_config['supported_versions']:
            return jsonify({'error': f'Version {api_version} not supported by {provider} provider'}), 400

        # 獲取 API Key (優先使用用戶提供的，否則使用配置中的)
        api_key = request.headers.get('X-API-KEY') or request.form.get('api_key')
        if not api_key:
            api_key = provider_config['api_key']  # 使用配置中的默認 API Key

        print("=" * 60)
        print(f"🚀 收到圖片轉視頻請求")
        print(f"📍 Provider: {provider}")
        print(f"🔗 API Version: {api_version}")
        print(f"🔑 API Key: {api_key[:8]}...{api_key[-8:]}")
        print(f"📝 Provider Config: {provider_config['name']}")
        
        # 獲取端點和基礎 URL
        endpoint = provider_config['supported_versions'][api_version]
        base_url = provider_config['base_url']
        full_url = f"{base_url}{endpoint}"
        
        print(f"🌐 Base URL: {base_url}")
        print(f"🎯 Endpoint: {endpoint}")
        print(f"🔗 Full URL: {full_url}")
        print("=" * 60)

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

        # 處理提示詞和其他參數
        if 'promptText' in request.form:
            prompt_text = request.form['promptText']
            if prompt_text.strip():
                data['promptText'] = prompt_text
                print(f"提示詞: {prompt_text}")
        
        # 處理可選參數
        if 'seed' in request.form and request.form['seed'].strip():
            data['seed'] = int(request.form['seed'])
            
        if 'negativePrompt' in request.form and request.form['negativePrompt'].strip():
            data['negativePrompt'] = request.form['negativePrompt']

        # 發送請求到 Pika API
        headers = {
            'X-API-KEY': api_key,
            'Accept': 'application/json'
        }

        print(f"📤 發送請求到 Pika API...")
        print(f"📋 Request Headers: {headers}")
        print(f"📋 Request Data: {data}")
        if files:
            print(f"📎 Files: {list(files.keys())}")
        
        response = requests.post(
            full_url,
            headers=headers,
            files=files,
            data=data,
            timeout=30
        )

        print("=" * 60)
        print(f"📥 Pika API 響應收到")
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        # 讀取和記錄響應內容
        response_content = response.text
        print(f"📝 Response Content: {response_content}")
        
        # 如果成功，記錄更多詳細信息
        if response.status_code == 200:
            try:
                json_response = response.json()
                video_id = json_response.get('video_id', 'N/A')
                worker = json_response.get('worker', 'Not specified')
                status = json_response.get('status', 'pending')
                
                print("🎉 視頻生成請求成功提交!")
                print(f"🆔 Video ID: {video_id}")
                print(f"🏗️ Worker: {worker}")
                print(f"📊 Initial Status: {status}")
                print(f"📍 Provider: {provider}")
                print(f"🔗 API Version: {api_version}")
                print(f"🌐 Base URL: {base_url}")
                print(f"🎯 Endpoint: {endpoint}")
                print(f"📝 Prompt: {data.get('promptText', 'No prompt')}")
                if files:
                    print(f"📎 Image Files: {list(files.keys())}")
            except:
                print("⚠️ Could not parse JSON response for detailed logging")
        
        print("=" * 60)
        
        # 返回響應
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                return jsonify(response.json()), response.status_code
            except:
                return jsonify({"error": "Invalid JSON response", "content": response_content}), response.status_code
        else:
            return response_content, response.status_code

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
        # 獲取提供商參數，默認為 original
        provider = request.args.get('provider', 'original')
        
        if provider not in API_PROVIDERS:
            return jsonify({'error': f'Unsupported provider: {provider}'}), 400
            
        provider_config = API_PROVIDERS[provider]

        # 獲取 API Key (優先使用用戶提供的，否則使用配置中的)
        api_key = request.headers.get('X-API-KEY') or request.args.get('api_key')
        if not api_key:
            api_key = provider_config['api_key']

        print(f"查詢視頻狀態: {video_id} (使用 {provider} 提供商)")

        # 轉發請求到 Pika API
        headers = {
            'X-API-KEY': api_key,
            'Accept': 'application/json'
        }

        response = requests.get(
            f"{provider_config['base_url']}/videos/{video_id}",
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

@app.route('/api/info', methods=['GET'])
def api_info():
    """返回支持的 API 提供商和版本信息"""
    return jsonify({
        'providers': API_PROVIDERS
    })

@app.route('/test', methods=['GET', 'OPTIONS'])
def test_connection():
    """測試連接端點"""
    provider = request.args.get('provider', 'original')
    
    if provider not in API_PROVIDERS:
        return jsonify({'error': f'Unsupported provider: {provider}'}), 400
        
    provider_config = API_PROVIDERS[provider]
    
    api_key = request.headers.get('X-API-KEY') or request.args.get('api_key')
    if not api_key:
        api_key = provider_config['api_key']

    try:
        headers = {
            'X-API-KEY': api_key,
            'Accept': 'application/json'
        }

        # 測試基礎 URL 連通性
        test_url = f"{provider_config['base_url']}/videos/test"
        response = requests.get(
            test_url,
            headers=headers,
            timeout=10
        )

        return jsonify({
            'status': 'success',
            'provider': provider,
            'api_status': response.status_code,
            'message': 'Connection test successful',
            'base_url': provider_config['base_url']
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'provider': provider,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    port = 5003
    try:
        app.run(port=port, debug=True)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"⚠️ Port {port} is in use. Trying to find a free port...")
            try:
                free_port = find_free_port()
                print(f"✅ Found free port: {free_port}. Starting server...")
                app.run(port=free_port, debug=True)
            except Exception as e_new:
                print(f"❌ Could not start server on a free port. Error: {e_new}")
        else:
            print(f"❌ An unexpected error occurred: {e}") 