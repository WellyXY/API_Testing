#!/usr/bin/env python3
"""
Snax API proxy server
Resolves browser CORS issues
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
import json
import socket
from contextlib import closing
import tempfile
import subprocess
import mimetypes

app = Flask(__name__)
CORS(app)  # allow all CORS requests

# API providers (Staging only)
API_PROVIDERS = {
    'staging': {
        'name': 'Staging',
        'base_url': 'https://089e99349ace.pikalabs.app',
        'api_key': 'pk_fnOLPQFrhk96QscYG9hIUSw-Jn5ygl_ehSUWa9PvwZM',
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
    """Serve frontend page"""
    return send_from_directory('.', 'pika_api_frontend.html')

@app.route('/test_endpoints')
def test_endpoints():
    """Serve endpoints test page"""
    return send_from_directory('.', 'test_endpoints.html')


@app.route('/generate/2.2/i2v', methods=['POST'])
def generate_video_v22():
    """Proxy image-to-video request - staging environment"""
    return _generate_video_internal('staging', 'v2.2')

## Removed Original v0 endpoints; keep Staging v2.2 only

@app.route('/api/generate', methods=['POST'])
def generate_video_flexible():
    """Generation endpoint (Staging only)"""
    # use staging environment only
    provider = 'staging'
    version = 'v2.2'
    return _generate_video_internal(provider, version, None, expect_audio=False)

def _generate_video_internal(provider='staging', api_version='v2.2', endpoint_type=None, expect_audio=False):
    """Internal image-to-video handler"""
    try:
        # Validate provider and version
        if provider not in API_PROVIDERS:
            return jsonify({'error': f'Unsupported provider: {provider}'}), 400
            
        provider_config = API_PROVIDERS[provider]
        
        if api_version not in provider_config['supported_versions']:
            return jsonify({'error': f'Version {api_version} not supported by {provider} provider'}), 400

        # Get API Key (prefer user-provided; fallback to configured)
        api_key = request.headers.get('X-API-KEY') or request.form.get('api_key')
        if not api_key:
            api_key = provider_config['api_key']  # use default API Key from config

        print("=" * 60)
        print(f"🚀 Received image-to-video request")
        print(f"📍 Provider: {provider}")
        print(f"🔗 API Version: {api_version}")
        print(f"🔑 API Key: {api_key[:8]}...{api_key[-8:]}")
        print(f"📝 Provider Config: {provider_config['name']}")
        
        # Resolve endpoint and base URL
        version_config = provider_config['supported_versions'][api_version]
        
        # Handle different endpoint config types
        if isinstance(version_config, dict):
            # Original API supports multiple endpoints (kept for reference)
            if endpoint_type and endpoint_type in version_config:
                endpoint = version_config[endpoint_type]
            else:
                # Default to the first endpoint
                endpoint = list(version_config.values())[0]
        else:
            # Staging API uses a single endpoint
            endpoint = version_config
            
        base_url = provider_config['base_url']
        full_url = f"{base_url}{endpoint}"
        
        print(f"🌐 Base URL: {base_url}")
        print(f"🎯 Endpoint: {endpoint}")
        print(f"🔗 Full URL: {full_url}")
        print("=" * 60)

        # Prepare request payload
        files = {}
        data = {}
        
        # Handle image file
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename:
                files['image'] = (
                    image_file.filename,
                    image_file.stream,
                    image_file.content_type
                )
                print(f"Received image file: {image_file.filename}")

        # Handle audio file (only if endpoint expects audio)
        if expect_audio:
            if 'audio' in request.files and request.files['audio'].filename:
                audio_file = request.files['audio']
                audio_ct = audio_file.content_type or mimetypes.guess_type(audio_file.filename)[0] or ''
                print(f"Received audio file: {audio_file.filename} (content-type: {audio_ct})")

                def _convert_mp4_to_audio(file_storage):
                    """Extract audio from video/mp4 to m4a; fallback to mp3. Returns (path, mime, filename)."""
                    # Save temp input
                    in_fd, in_path = tempfile.mkstemp(suffix=os.path.splitext(file_storage.filename)[1] or '.mp4')
                    os.close(in_fd)
                    file_storage.save(in_path)

                    # Prefer m4a output (audio container, mime audio/mp4)
                    out_m4a = tempfile.mktemp(suffix='.m4a')
                    try:
                        subprocess.run([
                            'ffmpeg','-y','-i', in_path,
                            '-vn','-acodec','copy', out_m4a
                        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        return out_m4a, 'audio/mp4', os.path.basename(file_storage.filename).rsplit('.',1)[0] + '.m4a'
                    except Exception:
                        # Fallback to mp3
                        out_mp3 = tempfile.mktemp(suffix='.mp3')
                        try:
                            subprocess.run([
                                'ffmpeg','-y','-i', in_path,
                                '-vn','-ac','2','-ar','44100','-b:a','192k', out_mp3
                            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            return out_mp3, 'audio/mpeg', os.path.basename(file_storage.filename).rsplit('.',1)[0] + '.mp3'
                        except Exception as e:
                            raise RuntimeError(f'ffmpeg conversion failed: {e}')
                    finally:
                        try:
                            os.remove(in_path)
                        except Exception:
                            pass

                # If video/mp4, extract audio first
                if audio_ct.startswith('video/') or audio_file.filename.lower().endswith('.mp4'):
                    try:
                        converted_path, converted_mime, converted_name = _convert_mp4_to_audio(audio_file)
                        files['audio'] = (
                            converted_name,
                            open(converted_path, 'rb'),
                            converted_mime
                        )
                        # Record temp converted file for later cleanup
                        data['_temp_audio_path'] = converted_path
                        print(f"Converted audio: {converted_name} (mime: {converted_mime})")
                    except FileNotFoundError:
                        return jsonify({'error': 'ffmpeg not found. Please install ffmpeg to support mp4 audio extraction.'}), 400
                    except RuntimeError as e:
                        return jsonify({'error': f'Could not extract audio from mp4: {str(e)}'}), 400
                else:
                    # Already audio; forward as-is
                    files['audio'] = (
                        audio_file.filename,
                        audio_file.stream,
                        audio_ct or 'audio/mpeg'
                    )
            else:
                return jsonify({'error': 'audio file is required for audio-to-video endpoint'}), 400

        # Handle prompt and other params
        if 'promptText' in request.form:
            prompt_text = request.form['promptText']
            if prompt_text.strip():
                data['promptText'] = prompt_text
        print(f"Prompt: {prompt_text}")
        
        # Optional params
        if 'seed' in request.form and request.form['seed'].strip():
            data['seed'] = int(request.form['seed'])
            
        if 'negativePrompt' in request.form and request.form['negativePrompt'].strip():
            data['negativePrompt'] = request.form['negativePrompt']

        # Send request to Snax API
        headers = {
            'X-API-KEY': api_key,
            'Accept': 'application/json'
        }

        print(f"📤 Sending request to Snax API...")
        print(f"📋 Request Headers: {headers}")
        print(f"📋 Request Data: {data}")
        if files:
            print(f"📎 Files: {list(files.keys())}")
        
        response = requests.post(
            full_url,
            headers=headers,
            files=files,
            data={k:v for k,v in data.items() if not k.startswith('_temp_')},
            timeout=60
        )

        print("=" * 60)
        print(f"📥 Snax API response received")
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        # Read and log response content
        response_content = response.text
        print(f"📝 Response Content: {response_content}")
        
        # If successful, log more details
        if response.status_code == 200:
            try:
                json_response = response.json()
                video_id = json_response.get('video_id', 'N/A')
                worker = json_response.get('worker', 'Not specified')
                status = json_response.get('status', 'pending')
                
                print("🎉 Video generation request submitted!")
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
        
        # Return response
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                return jsonify(response.json()), response.status_code
            except:
                return jsonify({"error": "Invalid JSON response", "content": response_content}), response.status_code
        else:
            return response_content, response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return jsonify({'error': f'Network error: {str(e)}'}), 500
    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/videos/<video_id>', methods=['GET'])
def get_video_status(video_id):
    """Proxy video status request"""
    try:
        # Staging only
        provider = 'staging'
        
        if provider not in API_PROVIDERS:
            return jsonify({'error': f'Unsupported provider: {provider}'}), 400
            
        provider_config = API_PROVIDERS[provider]

        # Get API Key (prefer user-provided; fallback to configured)
        api_key = request.headers.get('X-API-KEY') or request.args.get('api_key')
        if not api_key:
            api_key = provider_config['api_key']

        print(f"Query video status: {video_id} (provider {provider})")

        # Forward request to Snax API
        headers = {
            'X-API-KEY': api_key,
            'Accept': 'application/json'
        }

        response = requests.get(
            f"{provider_config['base_url']}/videos/{video_id}",
            headers=headers,
            timeout=30
        )

        print(f"Video status response: {response.status_code}")
        
        # Verbose logging for response
        try:
            response_data = response.json()
            print(f"Response JSON: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        except:
            print(f"Response text: {response.text}")

        # Return response
        if response.headers.get('content-type', '').startswith('application/json'):
            return jsonify(response.json()), response.status_code
        else:
            return response.text, response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return jsonify({'error': f'Network error: {str(e)}'}), 500
    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/info', methods=['GET'])
def api_info():
    """Return supported API providers and versions"""
    return jsonify({
        'providers': API_PROVIDERS
    })

@app.route('/test', methods=['GET', 'OPTIONS'])
def test_connection():
    """Connection test endpoint"""
    provider = request.args.get('provider', 'staging')
    
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

        # Test base URL connectivity
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