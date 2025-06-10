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

# API 提供商配置
API_PROVIDERS = {
    'original': {
        'name': 'Original',
        'base_url': 'https://qazwsxedcrf3g5h.pika.art',
        'api_key': 'pk_GW7ITxUVnC271AoJaasgdATrmzjl4OnQKTmD2j6tLZM',  # 用戶的 API Key
        'supported_versions': {
            'v0': '/generate/v0/image-to-video'
        }
    },
    'staging': {
        'name': 'Staging',
        'base_url': 'https://089e99349ace.pikalabs.app',
        'api_key': 'pk_K7IwcgVkFiQySdmoW4kNfgiR_G8C0nSmsd-sIo8Axn0',  # 新的 API Token
        'supported_versions': {
            'v2.2': '/generate/2.2/i2v',
            'turbo': '/generate/turbo/i2v'
        }
    }
}

@app.route('/')
def index():
    """提供前端頁面"""
    return send_from_directory('.', 'pika_api_frontend.html')

@app.route('/generate/v0/image-to-video', methods=['POST'])
def generate_video():
    """代理圖片轉視頻請求 - 保持原有端點兼容性"""
    return _generate_video_internal('original', 'v0')

@app.route('/generate/2.2/i2v', methods=['POST']) 
def generate_video_v22():
    """2.2 版本的圖片轉視頻"""
    return _generate_video_internal('staging', 'v2.2')

@app.route('/generate/turbo/i2v', methods=['POST'])
def generate_video_turbo():
    """Turbo 版本的圖片轉視頻"""
    return _generate_video_internal('staging', 'turbo')

@app.route('/api/generate', methods=['POST'])
def generate_video_flexible():
    """靈活的生成端點，支持提供商和版本選擇"""
    provider = request.form.get('provider', 'original')
    version = request.form.get('version', 'v0')
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

        print(f"收到圖片轉視頻請求 ({provider} - {api_version})，API Key: {api_key[:10]}...")

        # 獲取端點和基礎 URL
        endpoint = provider_config['supported_versions'][api_version]
        base_url = provider_config['base_url']

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

        full_url = f"{base_url}{endpoint}"
        print(f"轉發請求到: {full_url}")
        
        response = requests.post(
            full_url,
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
    print("🚀 啟動 Pika API 代理服務器...")
    print("📱 前端頁面: http://localhost:5003")
    print("🔧 API 代理: http://localhost:5003/generate/v0/image-to-video")
    
    app.run(
        host='0.0.0.0',
        port=5003,
        debug=True
    ) 