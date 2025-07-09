import requests
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.proxy_request('GET')

    def do_POST(self):
        self.proxy_request('POST')

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-API-KEY')
        self.end_headers()

    def proxy_request(self, method):
        # Base URL for the target API
        BASE_URL = "https://devapi.pika.art"
        
        # Parse path from query parameters
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        target_path = query_params.get('path', [''])[0]

        if not target_path:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': "Query parameter 'path' is missing"}).encode('utf-8'))
            return

        target_url = f"{BASE_URL}/{target_path.lstrip('/')}"
        
        # Get API key from client's header
        api_key = self.headers.get('X-API-KEY')
        if not api_key:
            self.send_response(401)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': "Header 'X-API-KEY' is missing"}).encode('utf-8'))
            return

        # Prepare headers for the forwarded request
        forward_headers = {
            'X-API-KEY': api_key,
            'Accept': self.headers.get('Accept', 'application/json')
        }
        
        body = None
        if method == 'POST':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            if 'Content-Type' in self.headers:
                forward_headers['Content-Type'] = self.headers['Content-Type']

        try:
            # Forward the request to the target API
            if method == 'POST':
                resp = requests.post(target_url, headers=forward_headers, data=body)
            else: # GET
                resp = requests.get(target_url, headers=forward_headers)

            # Send response back to the client
            self.send_response(resp.status_code)
            for key, value in resp.headers.items():
                if key.lower() not in ['content-encoding', 'transfer-encoding', 'connection']:
                    self.send_header(key, value)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(resp.content)

        except requests.exceptions.RequestException as e:
            self.send_response(502)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))