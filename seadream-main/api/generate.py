"""
Vercel Serverless Function for Seedream API
"""
from http.server import BaseHTTPRequestHandler
import json
import base64
import requests
from io import BytesIO
from PIL import Image
import os

API_KEY = os.environ.get('SEEDREAM_API_KEY', '70f23192-0f0c-47d2-9bbf-961f70a17a92')
BASE_URL = "https://ark.ap-southeast.bytepluses.com/api/v3"

def base64_to_pil(base64_string):
    """将 base64 字符串转换为 PIL Image"""
    if ',' in base64_string:
        base64_string = base64_string.split(',', 1)[1]
    
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    return image

def pil_to_base64_optimized(image):
    """将 PIL Image 转换为优化的 base64"""
    buffered = BytesIO()
    
    # 转换为 RGB 模式
    if image.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
        image = background
    elif image.mode != 'RGB':
        image = image.convert('RGB')
    
    # 缩小尺寸
    max_dimension = 2560
    width, height = image.size
    if max(width, height) > max_dimension:
        ratio = max_dimension / max(width, height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # 保存为 JPEG
    image.save(buffered, format="JPEG", quality=95, optimize=True)
    
    # 如果太大，降低质量
    if len(buffered.getvalue()) / (1024 * 1024) > 8:
        buffered = BytesIO()
        image.save(buffered, format="JPEG", quality=85, optimize=True)
    
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{img_base64}"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """处理 POST 请求"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # 构建 API 数据
            api_data = {
                "model": data.get("model", "ep-20250921042133-t769x"),
                "prompt": data.get("prompt", ""),
                "response_format": "url",
                "size": data.get("size", "1440x2560"),
                "watermark": data.get("watermark", False)
            }
            
            # 处理图片
            if "image" in data:
                image_data = data["image"]
                
                if isinstance(image_data, list):
                    processed_images = []
                    for img in image_data:
                        pil_image = base64_to_pil(img)
                        optimized_base64 = pil_to_base64_optimized(pil_image)
                        processed_images.append(optimized_base64)
                    api_data["image"] = processed_images
                else:
                    pil_image = base64_to_pil(image_data)
                    optimized_base64 = pil_to_base64_optimized(pil_image)
                    api_data["image"] = optimized_base64
            
            # 调用 API
            response = requests.post(
                f"{BASE_URL}/images/generations",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}"
                },
                json=api_data,
                timeout=120
            )
            
            result = response.json()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {"error": {"message": str(e)}}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        """处理 OPTIONS 请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

