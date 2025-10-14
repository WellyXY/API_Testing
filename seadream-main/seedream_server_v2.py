#!/usr/bin/env python3
"""
Seedream API 本地服务器 V2
使用改进的图片处理逻辑，模仿同事的实现方式
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import base64
import requests
from io import BytesIO
from PIL import Image
import os
import re

API_KEY = "70f23192-0f0c-47d2-9bbf-961f70a17a92"
BASE_URL = "https://ark.ap-southeast.bytepluses.com/api/v3"

def base64_to_pil(base64_string):
    """将 base64 字符串转换为 PIL Image"""
    # 移除 data:image/xxx;base64, 前缀
    if ',' in base64_string:
        base64_string = base64_string.split(',', 1)[1]
    
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    return image

def pil_to_base64_optimized(image):
    """将 PIL Image 转换为优化的 base64（保证质量的同时控制大小）"""
    buffered = BytesIO()
    
    # 转换为 RGB 模式（如果是 RGBA 或其他模式）
    if image.mode in ('RGBA', 'LA', 'P'):
        # 创建白色背景
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
        image = background
    elif image.mode != 'RGB':
        image = image.convert('RGB')
    
    # 如果图片很大，先缩小尺寸
    max_dimension = 2560  # 最大边长
    width, height = image.size
    if max(width, height) > max_dimension:
        ratio = max_dimension / max(width, height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        print(f"   📐 图片缩放: {width}x{height} → {new_width}x{new_height}", flush=True)
    
    # 尝试 JPEG 格式（更小）
    image.save(buffered, format="JPEG", quality=95, optimize=True)
    size_mb = len(buffered.getvalue()) / (1024 * 1024)
    
    # 如果还是太大，降低质量
    if size_mb > 8:  # 留一些余量
        buffered = BytesIO()
        image.save(buffered, format="JPEG", quality=85, optimize=True)
        size_mb = len(buffered.getvalue()) / (1024 * 1024)
        print(f"   🗜️  降低质量以减小文件: {size_mb:.2f} MB", flush=True)
    
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    print(f"   📦 最终大小: {size_mb:.2f} MB", flush=True)
    
    return f"data:image/jpeg;base64,{img_base64}"

class SeedreamHandler(SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        """处理预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """处理API请求"""
        if self.path == '/api/generate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # 调用Seedream API
            try:
                print(f"📥 收到生成请求", flush=True)
                
                # 构建 API 数据
                api_data = {
                    "model": data.get("model", "ep-20250921042133-t769x"),
                    "prompt": data.get("prompt", ""),
                    "response_format": "url",
                    "size": data.get("size", "1440x2560"),
                    "watermark": data.get("watermark", False)
                }
                
                # 处理图片 - 统一转换为 PNG 格式的 base64
                if "image" in data:
                    image_data = data["image"]
                    
                    if isinstance(image_data, list):
                        # 多张图片
                        print(f"🖼️  处理 {len(image_data)} 张参考图片...", flush=True)
                        processed_images = []
                        for idx, img in enumerate(image_data):
                            print(f"   🖼️  处理图片 {idx+1}...", flush=True)
                            pil_image = base64_to_pil(img)
                            optimized_base64 = pil_to_base64_optimized(pil_image)
                            processed_images.append(optimized_base64)
                        api_data["image"] = processed_images
                    else:
                        # 单张图片
                        print(f"🖼️  处理 1 张参考图片...", flush=True)
                        pil_image = base64_to_pil(image_data)
                        optimized_base64 = pil_to_base64_optimized(pil_image)
                        api_data["image"] = optimized_base64
                
                print(f"🚀 调用 API: {api_data['model']}, size: {api_data['size']}", flush=True)
                
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
                
                if result.get('data'):
                    print(f"✅ 生成成功!", flush=True)
                else:
                    print(f"⚠️  API 返回: {result}", flush=True)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                
            except Exception as e:
                print(f"❌ 错误: {e}", flush=True)
                import traceback
                traceback.print_exc()
                
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {"error": {"message": str(e)}}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_error(404)

    def do_GET(self):
        """处理GET请求"""
        if self.path == '/' or self.path == '/index.html':
            self.path = '/seedream_web_local.html'
        return SimpleHTTPRequestHandler.do_GET(self)
    
    def log_message(self, format, *args):
        """自定义日志，减少噪音"""
        if '404' not in str(args):
            return  # 忽略 404 错误日志

def run_server(port=8080):
    """运行服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, SeedreamHandler)
    print(f"🚀 Seedream 服务器 V2 启动成功!")
    print(f"📱 请在浏览器中打开: http://localhost:{port}")
    print(f"🎨 改进:")
    print(f"   - 统一 RGB 颜色模式处理")
    print(f"   - 智能压缩（JPEG 95% 质量）")
    print(f"   - 自动缩放超大图片")
    print(f"   - 确保不超过 10MB 限制")
    print(f"⏹️  按 Ctrl+C 停止服务器")
    print(f"{'='*60}")
    httpd.serve_forever()

if __name__ == '__main__':
    # 切换到脚本所在目录
    os.chdir('/Users/welly/Desktop/Character folder')
    run_server(8888)

