from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)

# The base URL for the target API
BASE_URL = "https://api.pika.art/v1"

@app.route('/api/proxy', methods=['GET', 'POST', 'OPTIONS'])
def proxy_request():
    # Handle CORS preflight requests for browser compatibility
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, X-API-KEY',
        }
        return ('', 204, headers)

    # Get the target path from the 'path' query parameter
    path = request.args.get('path', '')
    if not path:
        return jsonify({"error": "Query parameter 'path' is missing"}), 400
        
    target_url = f"{BASE_URL}/{path.lstrip('/')}"

    # Get the API key from the client's custom X-API-KEY header
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        return jsonify({"error": "Header 'X-API-KEY' is missing"}), 401

    # Prepare headers for the forwarded request
    forward_headers = {
        'Accept': request.headers.get('Accept', 'application/json'),
        'Authorization': f"Bearer {api_key}"
    }
    if request.method == 'POST' and 'Content-Type' in request.headers:
        forward_headers['Content-Type'] = request.headers['Content-Type']

    try:
        # Forward the request to the target API
        if request.method == 'POST':
            resp = requests.post(target_url, headers=forward_headers, data=request.get_data(), params=request.args)
        else: # GET
            resp = requests.get(target_url, headers=forward_headers, params=request.args)

        # Create a new response to forward back to the client
        response_headers = {
            'Content-Type': resp.headers.get('content-type', 'application/json'),
            'Access-Control-Allow-Origin': '*' # Add CORS header for the actual response
        }
        return Response(resp.content, status=resp.status_code, headers=response_headers)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502 