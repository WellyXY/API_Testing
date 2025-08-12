#!/usr/bin/env python3
"""
Snax batch video generation server
Supports multi-image batch generation and one-click download
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
CORS(app)  # allow all CORS requests

# Snax API config (Staging)
PIKA_BASE_URL = "https://089e99349ace.pikalabs.app"

# Storage config
UPLOAD_FOLDER = 'uploads'
VIDEOS_FOLDER = 'generated_videos'
DOWNLOADS_FOLDER = 'downloads'

# Ensure folders exist
for folder in [UPLOAD_FOLDER, VIDEOS_FOLDER, DOWNLOADS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# In-memory batch tasks storage
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
    """Serve batch frontend page"""
    return send_from_directory('.', 'batch_frontend.html')

@app.route('/batch/generate', methods=['POST'])
def batch_generate():
    """Start batch video generation"""
    try:
        # Get API Key
        api_key = request.headers.get('X-API-KEY')
        if not api_key:
            return jsonify({'error': 'Missing API Key'}), 400

        # Get prompt
        prompt_text = request.form.get('promptText', '').strip()
        if not prompt_text:
            return jsonify({'error': 'Missing prompt text'}), 400

        # Get uploaded images
        images = request.files.getlist('images')
        if not images or len(images) == 0:
            return jsonify({'error': 'No images uploaded'}), 400

        print(f"Received batch request: {len(images)} images, prompt: {prompt_text}")

        # Create batch task
        task_id = str(uuid.uuid4())
        task = BatchTask(task_id)
        task.total_images = len(images)
        task.status = 'processing'
        batch_tasks[task_id] = task

        # Save uploaded images
        image_paths = []
        for i, image in enumerate(images):
            if image.filename:
                filename = f"{task_id}_{i}_{image.filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                image.save(filepath)
                image_paths.append((filepath, image.filename))

        # Start background worker thread
        thread = threading.Thread(
            target=process_batch_generation,
            args=(task_id, image_paths, prompt_text, api_key)
        )
        thread.daemon = True
        thread.start()

        return jsonify({'success': True, 'task_id': task_id, 'message': f'Started batch generation for {len(images)} images'})

    except Exception as e:
        print(f"Batch error: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

def process_batch_generation(task_id, image_paths, prompt_text, api_key):
    """Background: process batch generation"""
    task = batch_tasks[task_id]
    
    def generate_single_video(image_info):
        """Generate a single video"""
        image_path, original_filename = image_info
        try:
            # Prepare request
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
                
                # Send generation request
                response = requests.post(
                    f"{PIKA_BASE_URL}/generate/2.2/i2v",
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    video_id = result.get('id')
                    
                    if video_id:
                        # Wait for video to finish
                        video_url = wait_for_video_completion(video_id, api_key)
                        
                        if video_url:
                            # Download video
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
            print(f"Failed to generate video for {original_filename}: {e}")
            task.error_log.append(f"{original_filename}: {str(e)}")
            
        task.failed_videos += 1
        return None
    
    # Parallel processing
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(generate_single_video, image_paths))
    
    # Collect results
    for result in results:
        if result:
            task.video_results.append(result)
            task.completed_videos += 1
    
    # Cleanup uploads
    for image_path, _ in image_paths:
        try:
            os.remove(image_path)
        except:
            pass
    
    task.status = 'completed'
    print(f"Batch task {task_id} completed: {task.completed_videos}/{task.total_images} succeeded")

def wait_for_video_completion(video_id, api_key, max_wait=300):
    """Wait for video to finish"""
    headers = {
        'X-API-KEY': api_key,
        'Accept': 'application/json'
    }
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(
                f"{PIKA_BASE_URL}/videos/{video_id}",
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
            print(f"Error checking video status: {e}")
        
    time.sleep(5)  # wait 5 seconds before retrying
    
    return None

def download_video(video_url, filename):
    """Download video file"""
    try:
        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            filepath = os.path.join(VIDEOS_FOLDER, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return filepath
    except Exception as e:
        print(f"Download video failed: {e}")
    return None

@app.route('/batch/status/<task_id>', methods=['GET'])
def get_batch_status(task_id):
    """Get batch task status"""
    if task_id not in batch_tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    task = batch_tasks[task_id]
    return jsonify(task.to_dict())

@app.route('/batch/download/<task_id>', methods=['GET'])
def download_batch_videos(task_id):
    """Download all generated videos"""
    if task_id not in batch_tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    task = batch_tasks[task_id]
    
    if not task.video_results:
        return jsonify({'error': 'No videos to download'}), 404
    
    try:
        # Create ZIP file
        zip_filename = f"batch_videos_{task_id}.zip"
        zip_path = os.path.join(DOWNLOADS_FOLDER, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for video_result in task.video_results:
                video_path = video_result.get('video_path')
                if video_path and os.path.exists(video_path):
                    # Add to ZIP using original image name as prefix
                    arc_name = f"{video_result['image_filename']}_{video_result['video_filename']}"
                    zipf.write(video_path, arc_name)
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=zip_filename,
            mimetype='application/zip'
        )
        
    except Exception as e:
        print(f"Error creating download package: {e}")
        return jsonify({'error': f'Download error: {str(e)}'}), 500

@app.route('/batch/tasks', methods=['GET'])
def list_batch_tasks():
    """List all batch tasks"""
    tasks = []
    for task_id, task in batch_tasks.items():
        tasks.append(task.to_dict())
    
    # Sort by creation time
    tasks.sort(key=lambda x: x['created_at'], reverse=True)
    
    return jsonify({'tasks': tasks})

@app.route('/batch/delete/<task_id>', methods=['DELETE'])
def delete_batch_task(task_id):
    """Delete batch task and related files"""
    if task_id not in batch_tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    try:
        task = batch_tasks[task_id]
        
        # Delete video files
        for video_result in task.video_results:
            video_path = video_result.get('video_path')
            if video_path and os.path.exists(video_path):
                os.remove(video_path)
        
        # Delete ZIP file
        zip_filename = f"batch_videos_{task_id}.zip"
        zip_path = os.path.join(DOWNLOADS_FOLDER, zip_filename)
        if os.path.exists(zip_path):
            os.remove(zip_path)
        
        # Remove task from memory
        del batch_tasks[task_id]
        
        return jsonify({'success': True, 'message': 'Task deleted'})
        
    except Exception as e:
        print(f"Error deleting task: {e}")
        return jsonify({'error': f'Delete error: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Starting Snax batch video server...")
    print("📱 Frontend: http://localhost:5004")
    print("🔧 Batch API: http://localhost:5004/batch/generate")
    
    app.run(
        host='0.0.0.0',
        port=5004,
        debug=True
    ) 