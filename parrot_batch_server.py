#!/usr/bin/env python3
"""
Parrot 批量視頻生成服務器
支持多圖批量生成和一鍵全部下載
"""

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import requests
import os
import json
import time
import uuid
import threading
from concurrent.futures import ThreadPoolExecutor
import zipfile
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 允許所有跨域請求

# Parrot API 配置
PARROT_BASE_URL = "https://qazwsxedcrf3g5h.parrot.art"

# 存儲配置
UPLOAD_FOLDER = 'uploads'
VIDEOS_FOLDER = 'generated_videos'
DOWNLOADS_FOLDER = 'downloads'

# 確保資料夾存在
for folder in [UPLOAD_FOLDER, VIDEOS_FOLDER, DOWNLOADS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# 全局變量存儲批量任務狀態
batch_tasks = {}

class BatchTask:
    def __init__(self, task_id):
        self.task_id = task_id
        self.status = 'pending'
        self.total_images = 0
        self.completed_videos = 0
        self.failed_videos = 0
        self.video_results = []
        self.error_log = []
        self.created_at = datetime.now()
        
    def to_dict(self):
        return {
            'task_id': self.task_id,
            'status': self.status,
            'total_images': self.total_images,
            'completed_videos': self.completed_videos,
            'failed_videos': self.failed_videos,
            'progress': (self.completed_videos + self.failed_videos) / max(self.total_images, 1) * 100,
            'video_results': self.video_results,
            'error_log': self.error_log,
            'created_at': self.created_at.isoformat()
        }

@app.route('/')
def index():
    """提供批量處理前端頁面"""
    return send_from_directory('.', 'batch_frontend.html')

@app.route('/batch/generate', methods=['POST'])
def batch_generate():
    """批量生成視頻"""
    try:
        # 獲取 API Key
        api_key = request.headers.get('X-API-KEY')
        if not api_key:
            return jsonify({'error': 'Missing API Key'}), 400

        # 獲取提示詞
        prompt_text = request.form.get('promptText', '').strip()
        if not prompt_text:
            return jsonify({'error': 'Missing prompt text'}), 400

        # 獲取上傳的圖片
        images = request.files.getlist('images')
        if not images or len(images) == 0:
            return jsonify({'error': 'No images uploaded'}), 400

        print(f"收到批量生成請求: {len(images)} 個圖片, 提示詞: {prompt_text}")

        # 創建批量任務
        task_id = str(uuid.uuid4())
        task = BatchTask(task_id)
        task.total_images = len(images)
        task.status = 'processing'
        batch_tasks[task_id] = task

        # 保存上傳的圖片
        image_paths = []
        for i, image in enumerate(images):
            if image.filename:
                filename = f"{task_id}_{i}_{image.filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                image.save(filepath)
                image_paths.append((filepath, image.filename))

        # 啟動後台處理線程
        thread = threading.Thread(
            target=process_batch_generation,
            args=(task_id, image_paths, prompt_text, api_key)
        )
        thread.daemon = True
        thread.start()

        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': f'Started batch generation for {len(images)} images'
        })

    except Exception as e:
        print(f"批量生成錯誤: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

def process_batch_generation(task_id, image_paths, prompt_text, api_key):
    """後台處理批量生成"""
    task = batch_tasks[task_id]
    
    def generate_single_video(image_info):
        """生成單個視頻"""
        image_path, original_filename = image_info
        try:
            # 準備請求
            headers = {
                'X-API-KEY': api_key,
                'Accept': 'application/json'
            }
            
            with open(image_path, 'rb') as img_file:
                files = {
                    'image': (original_filename, img_file, 'image/jpeg')
                }
                data = {
                    'promptText': prompt_text
                }
                
                # 發送生成請求
                response = requests.post(
                    f"{PARROT_BASE_URL}/generate/v0/image-to-video",
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    video_id = result.get('id')
                    
                    if video_id:
                        # 等待視頻生成完成
                        video_url = wait_for_video_completion(video_id, api_key)
                        
                        if video_url:
                            # 下載視頻
                            video_filename = f"{task_id}_{original_filename}_{video_id}.mp4"
                            video_path = download_video(video_url, video_filename)
                            
                            return {
                                'success': True,
                                'image_filename': original_filename,
                                'video_id': video_id,
                                'video_url': video_url,
                                'video_path': video_path,
                                'video_filename': video_filename
                            }
                    
        except Exception as e:
            print(f"生成視頻失敗 {original_filename}: {e}")
            task.error_log.append(f"{original_filename}: {str(e)}")
            
        task.failed_videos += 1
        return None
    
    # 使用線程池並行處理
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(generate_single_video, image_paths))
    
    # 處理結果
    for result in results:
        if result:
            task.video_results.append(result)
            task.completed_videos += 1
    
    # 清理上傳的圖片
    for image_path, _ in image_paths:
        try:
            os.remove(image_path)
        except:
            pass
    
    task.status = 'completed'
    print(f"批量任務 {task_id} 完成: {task.completed_videos}/{task.total_images} 成功")

def wait_for_video_completion(video_id, api_key, max_wait=300):
    """等待視頻生成完成"""
    headers = {
        'X-API-KEY': api_key,
        'Accept': 'application/json'
    }
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(
                f"{PARROT_BASE_URL}/videos/{video_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                status = data.get('status')
                
                if status == 'finished':
                    return data.get('videoUrl')
                elif status == 'failed':
                    return None
                    
        except Exception as e:
            print(f"查詢視頻狀態錯誤: {e}")
        
        time.sleep(5)  # 等待5秒後重試
    
    return None

def download_video(video_url, filename):
    """下載視頻文件"""
    try:
        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            filepath = os.path.join(VIDEOS_FOLDER, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return filepath
    except Exception as e:
        print(f"下載視頻失敗: {e}")
    return None

@app.route('/batch/status/<task_id>', methods=['GET'])
def get_batch_status(task_id):
    """獲取批量任務狀態"""
    if task_id not in batch_tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    task = batch_tasks[task_id]
    return jsonify(task.to_dict())

@app.route('/batch/download/<task_id>', methods=['GET'])
def download_batch_videos(task_id):
    """一鍵下載所有生成的視頻"""
    if task_id not in batch_tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    task = batch_tasks[task_id]
    
    if not task.video_results:
        return jsonify({'error': 'No videos to download'}), 404
    
    try:
        # 創建 ZIP 文件
        zip_filename = f"batch_videos_{task_id}.zip"
        zip_path = os.path.join(DOWNLOADS_FOLDER, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for video_result in task.video_results:
                video_path = video_result.get('video_path')
                if video_path and os.path.exists(video_path):
                    # 添加到 ZIP，使用原始圖片名稱作為前綴
                    arc_name = f"{video_result['image_filename']}_{video_result['video_filename']}"
                    zipf.write(video_path, arc_name)
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=zip_filename,
            mimetype='application/zip'
        )
        
    except Exception as e:
        print(f"創建下載包錯誤: {e}")
        return jsonify({'error': f'Download error: {str(e)}'}), 500

@app.route('/batch/tasks', methods=['GET'])
def list_batch_tasks():
    """列出所有批量任務"""
    tasks = []
    for task_id, task in batch_tasks.items():
        tasks.append(task.to_dict())
    
    # 按創建時間排序
    tasks.sort(key=lambda x: x['created_at'], reverse=True)
    
    return jsonify({'tasks': tasks})

@app.route('/batch/delete/<task_id>', methods=['DELETE'])
def delete_batch_task(task_id):
    """刪除批量任務和相關文件"""
    if task_id not in batch_tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    try:
        task = batch_tasks[task_id]
        
        # 刪除視頻文件
        for video_result in task.video_results:
            video_path = video_result.get('video_path')
            if video_path and os.path.exists(video_path):
                os.remove(video_path)
        
        # 刪除 ZIP 文件
        zip_filename = f"batch_videos_{task_id}.zip"
        zip_path = os.path.join(DOWNLOADS_FOLDER, zip_filename)
        if os.path.exists(zip_path):
            os.remove(zip_path)
        
        # 從記憶體中刪除任務
        del batch_tasks[task_id]
        
        return jsonify({'success': True, 'message': 'Task deleted'})
        
    except Exception as e:
        print(f"刪除任務錯誤: {e}")
        return jsonify({'error': f'Delete error: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 啟動 Parrot 批量視頻生成服務器...")
    print("📱 前端頁面: http://localhost:5004")
    print("🔧 批量 API: http://localhost:5004/batch/generate")
    
    app.run(
        host='0.0.0.0',
        port=5004,
        debug=True
    ) 