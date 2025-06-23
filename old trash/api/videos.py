import requests
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 獲取 API Key
            api_key = self.headers.get('X-API-KEY')
            if not api_key:
                self.send_error(400, 'Missing API Key')
                return

            # 解析 URL 獲取視頻 ID
            parsed_url = urlparse(self.path)
            path_parts = parsed_url.path.strip('/').split('/')
            
            if len(path_parts) > 1:
                video_id = path_parts[1]  # /videos/{video_id}
            else:
                query_params = parse_qs(parsed_url.query)
                video_id = query_params.get('id', [''])[0]

            if not video_id:
                self.send_error(400, 'Missing video ID')
                return

            # 發送請求到 Pika API
            headers = {
                'X-API-KEY': api_key,
                'Accept': 'application/json'
            }

            response = requests.get(
                f"https://qazwsxedcrf3g5h.pika.art/videos/{video_id}",
                headers=headers,
                timeout=30
            )

            # 返回響應
            self.send_response(response.status_code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'X-API-KEY, Content-Type')
            self.end_headers()
            
            self.wfile.write(response.content)

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
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-API-KEY, Content-Type')
        self.end_headers() 