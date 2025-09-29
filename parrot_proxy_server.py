#!/usr/bin/env python3
"""
Parrot API 代理服務器
解決瀏覽器 CORS 跨域問題
"""

from flask import Flask, request, jsonify, send_from_directory, Response, send_file
import zipfile
from flask_cors import CORS
import requests
import os
import json
import socket
from contextlib import closing
import base64
import tempfile
import subprocess
import mimetypes
import time

app = Flask(__name__)
CORS(app)  # 允許所有跨域請求

# API 提供商配置
API_PROVIDERS = {
    'original': {
        'name': 'Original',
        'base_url': 'https://qazwsxedcrf3g5h.pika.art',
        'api_key': 'pk_GW7ITxUVnC271AoJaasgdATrmzjl4OnQKTmD2j6tLZM',
        'supported_versions': {
            'v0': {
                'image-to-video': '/generate/v0/image-to-video',
                'image-to-video-new': '/generate/v0/image-to-video-new',
                'image-to-video-inner': '/generate/v0/image-to-video-inner',
                'image-to-video-nmd': '/generate/v0/image-to-video-nmd',
                'audio-to-video': '/generate/v0/audio-to-video'
            }
        }
    },
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
    """提供前端頁面"""
    return send_from_directory('.', 'parrot_api_frontend.html')

@app.route('/test_endpoints')
def test_endpoints():
    """提供端點測試頁面"""
    return send_from_directory('.', 'test_endpoints.html')

@app.route('/generate/v0/image-to-video', methods=['POST'])
def generate_video_v0():
    """代理圖片轉視頻請求 - 使用original環境"""
    return _generate_video_internal('original', 'v0', 'image-to-video')

@app.route('/generate/v0/image-to-video-new', methods=['POST'])
def generate_video_v0_new():
    """代理圖片轉視頻請求 - 使用original環境 (new端點)"""
    return _generate_video_internal('original', 'v0', 'image-to-video-new')

@app.route('/generate/v0/image-to-video-inner', methods=['POST'])
def generate_video_v0_inner():
    """代理圖片轉視頻請求 - 使用original環境 (inner端點)"""
    return _generate_video_internal('original', 'v0', 'image-to-video-inner')

@app.route('/generate/v0/image-to-video-nmd', methods=['POST'])
def generate_video_v0_nmd():
    """代理圖片轉視頻請求 - 使用original環境 (nmd端點)"""
    return _generate_video_internal('original', 'v0', 'image-to-video-nmd')

@app.route('/benchmark/merge', methods=['POST'])
def benchmark_merge():
    """下載兩個視頻並使用 ffmpeg 合併為左右拼接，返回 mp4。
    請求: form 或 json
      - left_url: 左側視頻 URL（必填）
      - right_url: 右側視頻 URL（必填）
      - filename: 下載文件名（可選，默認 merged.mp4）
    """
    try:
        left_url = request.form.get('left_url') or (request.json or {}).get('left_url')
        right_url = request.form.get('right_url') or (request.json or {}).get('right_url')
        file_name = request.form.get('filename') or (request.json or {}).get('filename') or 'merged.mp4'
        if not left_url or not right_url:
            return jsonify({'error': 'left_url and right_url are required'}), 400

        # 下載到臨時文件
        lpath = tempfile.mktemp(suffix='.mp4')
        rpath = tempfile.mktemp(suffix='.mp4')
        opath = tempfile.mktemp(suffix='.mp4')
        try:
            for url, path in [(left_url, lpath), (right_url, rpath)]:
                with requests.get(url, stream=True, timeout=120) as resp:
                    resp.raise_for_status()
                    with open(path, 'wb') as f:
                        for chunk in resp.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)

            # 使用 ffmpeg 進行左右拼接（將兩路縮放到同高 720，再 hstack）
            cmd = [
                'ffmpeg','-y',
                '-i', lpath,
                '-i', rpath,
                '-filter_complex', '[0:v]scale=-2:720[lv];[1:v]scale=-2:720[rv];[lv][rv]hstack=inputs=2[v]',
                '-map', '[v]',
                '-map', '0:a?',
                '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23',
                '-c:a', 'aac', '-shortest',
                opath
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # 返回文件
            return send_file(opath, mimetype='video/mp4', as_attachment=True, download_name=file_name)
        except FileNotFoundError:
            return jsonify({'error': 'ffmpeg not found. Please install ffmpeg.'}), 500
        except subprocess.CalledProcessError as e:
            return jsonify({'error': f'ffmpeg failed: {e}'}), 500
        except requests.RequestException as rexc:
            return jsonify({'error': f'download failed: {rexc}'}), 500
        finally:
            # 清理臨時文件
            for p in [lpath, rpath]:
                try:
                    if p and os.path.exists(p):
                        os.remove(p)
                except Exception:
                    pass
            # 輸出文件由 send_file 控制，不在此處刪除
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/benchmark/zip_pairs', methods=['POST'])
def benchmark_zip_pairs():
    """在無 ffmpeg 環境下的降級路由：僅把 A/B 原視頻打包為 ZIP 返回。
    請求 body JSON: { pairs: [ { left_url, right_url, filename? }, ... ] }
    """
    try:
        data = request.get_json(silent=True) or {}
        pairs = data.get('pairs') or []
        if not isinstance(pairs, list) or not pairs:
            return jsonify({'error': 'pairs is required'}), 400

        zip_path = tempfile.mktemp(suffix='.zip')
        errors = []
        with zipfile.ZipFile(zip_path, 'w') as zf:
            for idx, item in enumerate(pairs, start=1):
                left_url = item.get('left_url')
                right_url = item.get('right_url')
                base = (item.get('filename') or f'pair_{idx}').replace('/', '_')
                if not left_url or not right_url:
                    errors.append(f'pair#{idx}: missing url')
                    continue
                for tag, url in [('left', left_url), ('right', right_url)]:
                    try:
                        tmp = tempfile.mktemp(suffix='.mp4')
                        with requests.get(url, stream=True, timeout=300, headers={'User-Agent':'parrot-benchmark/1.0'}) as resp:
                            resp.raise_for_status()
                            with open(tmp, 'wb') as f:
                                for chunk in resp.iter_content(chunk_size=8192):
                                    if chunk:
                                        f.write(chunk)
                        zf.write(tmp, f'{base}_{tag}.mp4')
                    except Exception as e:
                        errors.append(f'pair#{idx}-{tag}: {type(e).__name__}: {e}')
                    finally:
                        try:
                            if 'tmp' in locals() and tmp and os.path.exists(tmp):
                                os.remove(tmp)
                        except Exception:
                            pass
            if errors:
                zf.writestr('errors.txt', '\n'.join(errors))

        return send_file(zip_path, mimetype='application/zip', as_attachment=True, download_name='benchmark_raw_pairs.zip')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/benchmark/merge_batch', methods=['POST'])
def benchmark_merge_batch():
    """批量左右拼接，返回 ZIP。
    請求 body JSON: { pairs: [ { left_url, right_url, filename? }, ... ] }
    """
    try:
        data = request.get_json(silent=True) or {}
        pairs = data.get('pairs') or []
        if not isinstance(pairs, list) or not pairs:
            return jsonify({'error': 'pairs is required'}), 400

        tmp_files = []
        zip_path = tempfile.mktemp(suffix='.zip')
        added_count = 0
        errors = []
        with zipfile.ZipFile(zip_path, 'w') as zf:
            for idx, item in enumerate(pairs, start=1):
                left_url = item.get('left_url')
                right_url = item.get('right_url')
                out_name = item.get('filename') or f'merged_{idx}.mp4'
                if not left_url or not right_url:
                    errors.append(f'pair#{idx}: missing left/right url')
                    continue

                lpath = tempfile.mktemp(suffix='.mp4')
                rpath = tempfile.mktemp(suffix='.mp4')
                opath = tempfile.mktemp(suffix='.mp4')
                try:
                    print(f"[merge_batch] downloading pair#{idx}")
                    for url, path in [(left_url, lpath), (right_url, rpath)]:
                        with requests.get(url, stream=True, timeout=300, headers={'User-Agent':'parrot-benchmark/1.0'}) as resp:
                            resp.raise_for_status()
                            with open(path, 'wb') as f:
                                for chunk in resp.iter_content(chunk_size=8192):
                                    if chunk:
                                        f.write(chunk)

                    cmd = [
                        'ffmpeg','-y',
                        '-i', lpath,
                        '-i', rpath,
                        '-filter_complex', '[0:v]scale=-2:720[lv];[1:v]scale=-2:720[rv];[lv][rv]hstack=inputs=2[v]',
                        '-map', '[v]',
                        '-map', '0:a?',
                        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23',
                        '-c:a', 'aac', '-shortest',
                        opath
                    ]
                    run = subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if run.returncode != 0 or not os.path.exists(opath) or os.path.getsize(opath) == 0:
                        raise RuntimeError(f"ffmpeg failed rc={run.returncode} stderr={run.stderr.decode(errors='ignore')[:200]}")
                    # 添加到 ZIP
                    zf.write(opath, out_name)
                    added_count += 1
                except Exception as e:
                    err_msg = f'pair#{idx}: {type(e).__name__}: {e}'
                    print('[merge_batch][error]', err_msg)
                    errors.append(err_msg)
                    # 回退：至少把左右原視頻打包入 ZIP，避免空包
                    try:
                        if os.path.exists(lpath):
                            zf.write(lpath, f'pair_{idx}_left.mp4')
                        if os.path.exists(rpath):
                            zf.write(rpath, f'pair_{idx}_right.mp4')
                    except Exception:
                        pass
                finally:
                    for p in [lpath, rpath, opath]:
                        try:
                            if p and os.path.exists(p):
                                tmp_files.append(p)
                        except Exception:
                            pass
            # 如果有錯誤，將錯誤寫入壓縮包
            if errors:
                zf.writestr('errors.txt', '\n'.join(errors))

        # 清理臨時合併視頻
        for p in tmp_files:
            try:
                os.remove(p)
            except Exception:
                pass

        if added_count == 0:
            # 沒有任何成功合併，直接返回錯誤
            return jsonify({'error': 'no merged outputs', 'errors': errors}), 500
        return send_file(zip_path, mimetype='application/zip', as_attachment=True, download_name='benchmark_merged_all.zip')
    except FileNotFoundError:
        return jsonify({'error': 'ffmpeg not found. Please install ffmpeg.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate/2.2/i2v', methods=['POST'])
def generate_video_v22():
    """代理圖片轉視頻請求 - 使用staging環境"""
    return _generate_video_internal('staging', 'v2.2')

@app.route('/generate/v0/audio-to-video', methods=['POST'])
def generate_audio_to_video_v0():
    """代理圖片+音頻轉視頻請求 - 使用original環境 (v0)"""
    return _generate_video_internal('original', 'v0', 'audio-to-video', expect_audio=True)

@app.route('/api/generate', methods=['POST'])
def generate_video_flexible():
    """靈活的生成端點，支持多提供商"""
    provider = request.form.get('provider', 'staging')
    version = request.form.get('version', 'v2.2')
    endpoint_type = request.form.get('endpoint_type')
    expect_audio = endpoint_type == 'audio-to-video'
    return _generate_video_internal(provider, version, endpoint_type, expect_audio=expect_audio)

def _generate_video_internal(provider='staging', api_version='v2.2', endpoint_type=None, expect_audio=False):
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
        # 防呆：若選擇的 provider 與傳入的 key 不匹配，糾正為對應 provider 的默認 key
        try:
            original_key = API_PROVIDERS['original']['api_key']
            staging_key = API_PROVIDERS['staging']['api_key']
            if provider == 'original' and api_key == staging_key:
                api_key = original_key
            elif provider == 'staging' and api_key == original_key:
                api_key = staging_key
        except Exception:
            pass

        print("=" * 60)
        print(f"🚀 收到圖片轉視頻請求")
        print(f"📍 Provider: {provider}")
        print(f"🔗 API Version: {api_version}")
        print(f"🔑 API Key: {api_key[:8]}...{api_key[-8:]}")
        print(f"📝 Provider Config: {provider_config['name']}")
        
        # 獲取端點和基礎 URL
        version_config = provider_config['supported_versions'][api_version]
        
        # 處理不同的端點類型
        if isinstance(version_config, dict):
            # Original API 支持多個端點
            if endpoint_type and endpoint_type in version_config:
                endpoint = version_config[endpoint_type]
            else:
                # 默認使用第一個端點
                endpoint = list(version_config.values())[0]
        else:
            # Staging API 使用單一端點
            endpoint = version_config
            
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

        # 處理音頻文件（僅當端點需要音頻時）
        if expect_audio:
            if 'audio' in request.files and request.files['audio'].filename:
                audio_file = request.files['audio']
                audio_ct = audio_file.content_type or mimetypes.guess_type(audio_file.filename)[0] or ''
                print(f"收到音頻文件: {audio_file.filename} (content-type: {audio_ct})")

                def _convert_mp4_to_audio(file_storage):
                    """將 video/mp4 抽出音訊為 m4a；失敗則轉 mp3。返回 (path, mime, filename)"""
                    # 保存臨時輸入
                    in_fd, in_path = tempfile.mkstemp(suffix=os.path.splitext(file_storage.filename)[1] or '.mp4')
                    os.close(in_fd)
                    file_storage.save(in_path)

                    # 優先輸出 m4a（音訊容器，mime audio/mp4）
                    out_m4a = tempfile.mktemp(suffix='.m4a')
                    try:
                        subprocess.run([
                            'ffmpeg','-y','-i', in_path,
                            '-vn','-acodec','copy', out_m4a
                        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        return out_m4a, 'audio/mp4', os.path.basename(file_storage.filename).rsplit('.',1)[0] + '.m4a'
                    except Exception:
                        # 回退轉成 mp3
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

                # 若為 video/mp4，先抽音
                if audio_ct.startswith('video/') or audio_file.filename.lower().endswith('.mp4'):
                    try:
                        converted_path, converted_mime, converted_name = _convert_mp4_to_audio(audio_file)
                        files['audio'] = (
                            converted_name,
                            open(converted_path, 'rb'),
                            converted_mime
                        )
                        # 記錄轉檔路徑，稍後請求完嘗試清理
                        data['_temp_audio_path'] = converted_path
                        print(f"已轉換音訊: {converted_name} (mime: {converted_mime})")
                    except FileNotFoundError:
                        return jsonify({'error': 'ffmpeg not found. Please install ffmpeg to support mp4 audio extraction.'}), 400
                    except RuntimeError as e:
                        return jsonify({'error': f'Could not extract audio from mp4: {str(e)}'}), 400
                else:
                    # 已是音訊，直接透傳
                    files['audio'] = (
                        audio_file.filename,
                        audio_file.stream,
                        audio_ct or 'audio/mpeg'
                    )
            else:
                return jsonify({'error': 'audio file is required for audio-to-video endpoint'}), 400

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

        # 發送請求到 Parrot API
        headers = {
            'X-API-KEY': api_key,
            'Accept': 'application/json'
        }

        print(f"📤 發送請求到 Parrot API...")
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
        print(f"📥 Parrot API 響應收到")
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
        # 獲取提供商參數，默認為 staging
        provider = request.args.get('provider', 'staging')
        
        if provider not in API_PROVIDERS:
            return jsonify({'error': f'Unsupported provider: {provider}'}), 400
            
        provider_config = API_PROVIDERS[provider]

        # 獲取 API Key (優先使用用戶提供的，否則使用配置中的)
        api_key = request.headers.get('X-API-KEY') or request.args.get('api_key')
        if not api_key:
            api_key = provider_config['api_key']

        print(f"查詢視頻狀態: {video_id} (使用 {provider} 提供商)")

        # 轉發請求到 Parrot API
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

@app.route('/minimax/env', methods=['GET'])
def minimax_env():
    """返回 MiniMax 憑證（僅用於本地開發自動填充）
    Query:
      - full=1 時返回明文 api_key；否則僅返回掩碼
    """
    group_id = os.getenv('MINIMAX_GROUPID', '')
    api_key = os.getenv('MINIMAX_API_KEY', '')
    masked = f"{api_key[:8]}...{api_key[-6:]}" if api_key else ''
    if request.args.get('full') == '1':
        return jsonify({'group_id': group_id, 'api_key': api_key, 'api_key_masked': masked})
    return jsonify({'group_id': group_id, 'api_key_masked': masked})

@app.route('/minimax/t2a', methods=['POST'])
def minimax_t2a():
    """MiniMax 文本轉語音代理端點
    請求: multipart/form-data 或 application/json
      - text: 必填，待合成文本
      - voice_id: 選填，默認 "nova-default"
      - MINIMAX_GROUPID: 可由環境變量、Header("X-Minimax-GroupId")、或表單字段提供
      - MINIMAX_API_KEY: 可由環境變量、Header("X-Minimax-ApiKey")、或表單字段提供
    響應: audio/mp3 二進制數據
    """
    try:
        # 讀取權鑰
        group_id = (
            request.headers.get('X-Minimax-GroupId')
            or request.form.get('MINIMAX_GROUPID')
            or request.json.get('MINIMAX_GROUPID') if request.is_json else None
            or os.getenv('MINIMAX_GROUPID')
        )
        api_key = (
            request.headers.get('X-Minimax-ApiKey')
            or request.form.get('MINIMAX_API_KEY')
            or request.json.get('MINIMAX_API_KEY') if request.is_json else None
            or os.getenv('MINIMAX_API_KEY')
        )

        if not group_id or not api_key:
            return jsonify({'error': 'MINIMAX_GROUPID and MINIMAX_API_KEY are required'}), 400

        # 讀取文本與語音參數
        text = request.form.get('text') if not request.is_json else request.json.get('text')
        voice_id = request.form.get('voice_id') if not request.is_json else request.json.get('voice_id')
        if not text or not text.strip():
            return jsonify({'error': 'text is required'}), 400

        # 構造請求
        url = f"https://api.minimax.io/v1/t2a_v2?GroupId={group_id}"
        payload = {
            "model": "speech-02-turbo",
            "text": text,
            "stream": False,
            "audio_setting": {
                "sample_rate": 32000,
                "bitrate": 128000,
                "format": "mp3",
                "channel": 1
            },
            "language_boost": "auto"
        }
        if voice_id and str(voice_id).strip():
            payload["voice_setting"] = {
                "voice_id": voice_id,
                "speed": 1,
                "vol": 1,
                "pitch": 0,
                "english_normalization": True
            }
        headers = {
            'Authorization': api_key,  # 直接使用 JWT token，不加 Bearer 前缀
            'Content-Type': 'application/json'
        }

        r = requests.post(url, headers=headers, json=payload, timeout=60)
        # 嘗試解析 JSON
        parsed = None
        try:
            parsed = r.json()
        except Exception:
            parsed = None

        if r.status_code != 200:
            # 盡量透傳 MiniMax 的錯誤
            base_resp = None
            if isinstance(parsed, dict):
                base_resp = parsed.get('base_resp') or parsed.get('data', {}).get('base_resp')
            message = None
            if isinstance(base_resp, dict):
                code = base_resp.get('status_code')
                msg = base_resp.get('status_msg')
                message = f"MiniMax error {code}: {msg}" if code or msg else None
            provider_status_code = None
            provider_status_msg = None
            try:
                if isinstance(parsed, dict):
                    base_resp = parsed.get('base_resp') or parsed.get('data', {}).get('base_resp') or {}
                    if isinstance(base_resp, dict):
                        provider_status_code = base_resp.get('status_code')
                        provider_status_msg = base_resp.get('status_msg')
            except Exception:
                pass
            return jsonify({
                'error': message or 'MiniMax T2A failed',
                'status': r.status_code,
                'provider_status_code': provider_status_code,
                'provider_status_msg': provider_status_msg,
                'provider_response': parsed if parsed is not None else r.text
            }), 400

        if not isinstance(parsed, dict) or 'data' not in parsed or 'audio' not in parsed['data']:
            return jsonify({'error': 'Invalid MiniMax response', 'provider_response': parsed if parsed is not None else r.text}), 400

        audio_value = bytes.fromhex(parsed['data']['audio'])
        filename = f"tts-{int(time.time()*1000)}.mp3"

        return Response(audio_value, mimetype='audio/mpeg', headers={
            'Content-Disposition': f'attachment; filename="{filename}"'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/minimax/clone', methods=['POST'])
def minimax_clone():
    """MiniMax 聲音克隆代理端點
    請求: multipart/form-data
      - audio: 必填，音頻文件
      - userId: 可選
      - voice_prefix: 可選，默認 'nova'
      - MINIMAX_GROUPID / MINIMAX_API_KEY: 與 t2a 相同規則
    響應: JSON { voice_id, preview_audio (data url，可選) }
    """
    try:
        group_id = request.headers.get('X-Minimax-GroupId') or request.form.get('MINIMAX_GROUPID') or os.getenv('MINIMAX_GROUPID')
        api_key = request.headers.get('X-Minimax-ApiKey') or request.form.get('MINIMAX_API_KEY') or os.getenv('MINIMAX_API_KEY')

        print(f"Group ID: {group_id}")
        print(f"API Key length: {len(api_key) if api_key else 0}")
        print(f"API Key first 20 chars: {api_key[:20] if api_key else 'None'}...")

        if not group_id or not api_key:
            return jsonify({'error': 'MINIMAX_GROUPID and MINIMAX_API_KEY are required'}), 400

        if 'audio' not in request.files and 'file' not in request.files:
            return jsonify({'error': 'audio file is required'}), 400
        file_storage = request.files.get('audio') or request.files.get('file')

        user_id = request.form.get('userId') or 'user'
        voice_prefix = request.form.get('voice_prefix') or 'nova'
        voice_id = f"{voice_prefix}-{user_id}-{int(time.time())}"

        # 處理文件轉換（如果是視頻，提取音頻）
        final_filename = file_storage.filename or 'audio.mp3'
        final_content_type = file_storage.mimetype or 'audio/mpeg'
        file_bytes = None
        temp_audio_path = None

        try:
            # 檢查是否為視頻文件需要轉音頻
            if (file_storage.mimetype and file_storage.mimetype.startswith('video/')) or \
               (file_storage.filename and file_storage.filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))):
                
                print(f"檢測到視頻文件，準備提取音頻: {file_storage.filename}")
                
                # 保存原始視頻到臨時文件
                in_fd, in_path = tempfile.mkstemp(suffix=os.path.splitext(file_storage.filename)[1] or '.mp4')
                os.close(in_fd)
                file_storage.save(in_path)
                
                # 提取音頻為 M4A
                out_m4a = tempfile.mktemp(suffix='.m4a')
                try:
                    subprocess.run([
                        'ffmpeg', '-y', '-i', in_path,
                        '-vn', '-acodec', 'copy', out_m4a
                    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                    with open(out_m4a, 'rb') as f:
                        file_bytes = f.read()
                    final_filename = os.path.splitext(file_storage.filename)[0] + '.m4a'
                    final_content_type = 'audio/mp4'
                    temp_audio_path = out_m4a
                    print(f"音頻提取成功: {final_filename}")
                    
                except subprocess.CalledProcessError:
                    # 回退提取為 MP3
                    out_mp3 = tempfile.mktemp(suffix='.mp3')
                    try:
                        subprocess.run([
                            'ffmpeg', '-y', '-i', in_path,
                            '-vn', '-ac', '2', '-ar', '44100', '-b:a', '192k', out_mp3
                        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        
                        with open(out_mp3, 'rb') as f:
                            file_bytes = f.read()
                        final_filename = os.path.splitext(file_storage.filename)[0] + '.mp3'
                        final_content_type = 'audio/mpeg'
                        temp_audio_path = out_mp3
                        print(f"音頻提取成功（MP3回退）: {final_filename}")
                        
                    except subprocess.CalledProcessError as e:
                        return jsonify({'error': f'ffmpeg audio extraction failed: {str(e)}'}), 400
                finally:
                    try:
                        os.remove(in_path)
                    except Exception:
                        pass
            else:
                # 直接使用音頻文件
                file_bytes = file_storage.read()

            # Step 1: 上傳文件
            upload_url = f'https://api.minimax.io/v1/files/upload?GroupId={group_id}'
            print(f"Upload URL: {upload_url}")
            # 测试不同的 Authorization 格式
            headers_upload = {
                'Authorization': api_key  # 直接使用 JWT token，不加 Bearer 前缀
            }
            print(f"Upload headers: {headers_upload}")

            files = {
                'file': (
                    final_filename,
                    file_bytes,
                    final_content_type
                )
            }
            data_upload = {
                'purpose': 'voice_clone'
            }
            try:
                resp_upload = requests.post(upload_url, headers=headers_upload, data=data_upload, files=files, timeout=60)
            except requests.exceptions.RequestException as rexc:
                return jsonify({
                    'error': str(rexc),
                    'stage': 'upload',
                    'exception': type(reexc).__name__ if 'reexc' in locals() else type(rexc).__name__,
                    'debug_auth': {
                        'uses_bearer': isinstance(headers_upload.get('Authorization'), str) and headers_upload.get('Authorization').startswith('Bearer '),
                        'token_length': len(headers_upload.get('Authorization') or ''),
                        'token_head': (headers_upload.get('Authorization') or '')[:10]
                    }
                }), 500
            print(f"Upload response status: {resp_upload.status_code}")
            print(f"Upload response headers: {dict(resp_upload.headers)}")
            print(f"Upload response body: {resp_upload.text}")
            if resp_upload.status_code != 200:
                err_json = None
                try:
                    err_json = resp_upload.json()
                except Exception:
                    pass
                return jsonify({
                    'error': 'Upload failed',
                    'status': resp_upload.status_code,
                    'provider_response': err_json if err_json is not None else resp_upload.text,
                    'debug_auth': {
                        'uses_bearer': isinstance(headers_upload.get('Authorization'), str) and headers_upload.get('Authorization').startswith('Bearer '),
                        'token_length': len(headers_upload.get('Authorization') or ''),
                        'token_head': (headers_upload.get('Authorization') or '')[:10]
                    }
                }), 500
            upload_json = None
            try:
                upload_json = resp_upload.json()
                print(f"MiniMax upload response: {upload_json}")
            except Exception as e:
                print(f"Failed to parse upload response as JSON: {e}")
                upload_json = None
            file_id = None
            if isinstance(upload_json, dict):
                file_field = upload_json.get('file')
                print(f"File field from upload response: {file_field}")
                if isinstance(file_field, dict):
                    file_id = file_field.get('file_id')
                    print(f"Extracted file_id: {file_id}")
            if not file_id:
                # 更透明的錯誤回傳：把 MiniMax 的 status_code / status_msg 展開
                print(f"No file_id found. Full response: {upload_json}")
                provider_status_code = None
                provider_status_msg = None
                try:
                    if isinstance(upload_json, dict):
                        base_resp = upload_json.get('base_resp') or {}
                        if isinstance(base_resp, dict):
                            provider_status_code = base_resp.get('status_code')
                            provider_status_msg = base_resp.get('status_msg')
                except Exception:
                    pass
                return jsonify({
                    'error': 'Upload response missing file_id',
                    'provider_status_code': provider_status_code,
                    'provider_status_msg': provider_status_msg,
                    'provider_response': upload_json,
                    'debug_auth': {
                        'uses_bearer': isinstance(headers_upload.get('Authorization'), str) and headers_upload.get('Authorization').startswith('Bearer '),
                        'token_length': len(headers_upload.get('Authorization') or ''),
                        'token_head': (headers_upload.get('Authorization') or '')[:10]
                    }
                }), 500

            # Step 2: 發起克隆
            clone_url = f'https://api.minimax.io/v1/voice_clone?GroupId={group_id}'
            headers_clone = {
                'Authorization': api_key,  # 直接使用 JWT token，不加 Bearer 前缀
                'Content-Type': 'application/json'
            }
            payload_clone = {
                'file_id': file_id,
                'voice_id': voice_id
            }
            try:
                resp_clone = requests.post(clone_url, headers=headers_clone, json=payload_clone, timeout=120)
            except requests.exceptions.RequestException as rexc:
                return jsonify({
                    'error': str(rexc),
                    'stage': 'clone',
                    'exception': type(rexc).__name__,
                    'debug_auth': {
                        'uses_bearer': isinstance(headers_clone.get('Authorization'), str) and headers_clone.get('Authorization').startswith('Bearer '),
                        'token_length': len(headers_clone.get('Authorization') or ''),
                        'token_head': (headers_clone.get('Authorization') or '')[:10]
                    }
                }), 500
            if resp_clone.status_code != 200:
                err_json = None
                try:
                    err_json = resp_clone.json()
                except Exception:
                    pass
                provider_status_code = None
                provider_status_msg = None
                try:
                    if isinstance(err_json, dict):
                        base_resp = err_json.get('base_resp') or {}
                        if isinstance(base_resp, dict):
                            provider_status_code = base_resp.get('status_code')
                            provider_status_msg = base_resp.get('status_msg')
                except Exception:
                    pass
                return jsonify({
                    'error': 'Clone failed',
                    'status': resp_clone.status_code,
                    'provider_status_code': provider_status_code,
                    'provider_status_msg': provider_status_msg,
                    'provider_response': err_json if err_json is not None else resp_clone.text
                }), 500

            # 可選：生成預覽音頻
            preview_audio_data_url = None
            try:
                t2a_url = f"https://api.minimax.io/v1/t2a_v2?GroupId={group_id}"
                payload_t2a = {
                    "model": "speech-02-turbo",
                    "text": "Hi, this is a preview of your cloned voice.",
                    "stream": False,
                    "voice_setting": {
                        "voice_id": voice_id,
                        "speed": 1,
                        "vol": 1,
                        "pitch": 0,
                        "english_normalization": True
                    },
                    "audio_setting": {
                        "sample_rate": 32000,
                        "bitrate": 128000,
                        "format": "mp3",
                        "channel": 1
                    },
                    "language_boost": "auto"
                }
                headers_t2a = {
                    'Authorization': api_key,  # 直接使用 JWT token，不加 Bearer 前缀
                    'Content-Type': 'application/json'
                }
                try:
                    r2 = requests.post(t2a_url, headers=headers_t2a, json=payload_t2a, timeout=60)
                except requests.exceptions.RequestException as rexc:
                    print(f"T2A preview request failed: {rexc}")
                    r2 = None
                if r2 is not None and r2.status_code == 200:
                    parsed2 = r2.json()
                    audio_hex = parsed2.get('data', {}).get('audio')
                    if audio_hex:
                        audio_bytes = bytes.fromhex(audio_hex)
                        preview_audio_data_url = 'data:audio/mpeg;base64,' + base64.b64encode(audio_bytes).decode('ascii')
            except Exception:
                pass

            return jsonify({
                'voice_id': voice_id,
                'preview_audio': preview_audio_data_url
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # 清理臨時文件
            if temp_audio_path:
                try:
                    os.remove(temp_audio_path)
                except Exception:
                    pass
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET', 'OPTIONS'])
def test_connection():
    """測試連接端點"""
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
    # 允許通過環境變量配置端口與主機
    try:
        port = int(os.getenv('PORT', '5003'))
    except Exception:
        port = 5003
    host = os.getenv('HOST', '0.0.0.0')
    try:
        # 關閉自動重載，以避免請求中途重啟導致 connection reset
        app.run(host=host, port=port, debug=False, use_reloader=False)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"⚠️ Port {port} is in use. Trying to find a free port...")
            try:
                free_port = find_free_port()
                print(f"✅ Found free port: {free_port}. Starting server...")
                app.run(host=host, port=free_port, debug=False, use_reloader=False)
            except Exception as e_new:
                print(f"❌ Could not start server on a free port. Error: {e_new}")
        else:
            print(f"❌ An unexpected error occurred: {e}")