#!/usr/bin/env python3
"""
Seedream API 本地服务器
解决CORS问题并提供Web界面
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import base64
import requests
from urllib.parse import parse_qs
import os

API_KEY = "70f23192-0f0c-47d2-9bbf-961f70a17a92"
BASE_URL = "https://ark.ap-southeast.bytepluses.com/api/v3"

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
                api_data = {
                    "model": data.get("model", "ep-20250921042133-t769x"),
                    "prompt": data.get("prompt", ""),
                    "response_format": "url",
                    "size": data.get("size", "2K"),
                    "watermark": data.get("watermark", False)
                }
                
                # 处理图片
                if "image" in data:
                    api_data["image"] = data["image"]
                
                response = requests.post(
                    f"{BASE_URL}/images/generations",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {API_KEY}"
                    },
                    json=api_data
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
        else:
            self.send_error(404)

    def do_GET(self):
        """处理GET请求"""
        if self.path == '/' or self.path == '/index.html':
            self.path = '/seedream_web_local.html'
        return SimpleHTTPRequestHandler.do_GET(self)

def run_server(port=8080):
    """运行服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, SeedreamHandler)
    print(f"🚀 Seedream 服务器启动成功!")
    print(f"📱 请在浏览器中打开: http://localhost:{port}")
    print(f"⏹️  按 Ctrl+C 停止服务器")
    httpd.serve_forever()

if __name__ == '__main__':
    # 切换到脚本所在目录
    os.chdir('/Users/welly/Desktop/Character folder')
    run_server(8080)
