import requests
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import cgi
import io

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 解析 multipart/form-data
            content_type = self.headers.get('Content-Type', '')
            
            if 'multipart/form-data' in content_type:
                # 獲取 API Key
                api_key = self.headers.get('X-API-KEY')
                if not api_key:
                    self.send_error(400, 'Missing API Key')
                    return

                # 解析 form data
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                # 準備請求數據
                files = {}
                data = {}
                
                # 處理圖片文件
                if 'image' in form:
                    image_field = form['image']
                    if image_field.filename:
                        files['image'] = (
                            image_field.filename,
                            image_field.file.read(),
                            image_field.type
                        )

                # 處理提示詞
                if 'promptText' in form:
                    prompt_text = form['promptText'].value
                    if prompt_text.strip():
                        data['promptText'] = prompt_text

                # 發送請求到 Pika API
                headers = {
                    'X-API-KEY': api_key,
                    'Accept': 'application/json'
                }

                response = requests.post(
                    "https://qazwsxedcrf3g5h.pika.art/generate/v0/image-to-video",
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=30
                )

                # 返回響應
                self.send_response(response.status_code)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'X-API-KEY, Content-Type')
                self.end_headers()
                
                self.wfile.write(response.content)

            else:
                self.send_error(400, 'Invalid Content-Type')

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = json.dumps({'error': f'Server error: {str(e)}'})
            self.wfile.write(error_response.encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-API-KEY, Content-Type')
        self.end_headers() 