from flask import Flask, request, jsonify, Response
import requests
import os

app = Flask(__name__)

# Load API keys from environment variables for security
PIKA_API_KEY_ORIGINAL = os.environ.get("PIKA_API_KEY_ORIGINAL")
PIKA_API_KEY_STAGING = os.environ.get("PIKA_API_KEY_STAGING")

BASE_URL_ORIGINAL = "https://api.pika.art/v1"
BASE_URL_STAGING = "https://staging-api.pika.art/v1"

def get_base_url_and_key(provider):
    if provider == 'staging':
        return BASE_URL_STAGING, PIKA_API_KEY_STAGING
    # Default to original
    return BASE_URL_ORIGINAL, PIKA_API_KEY_ORIGINAL

@app.route('/api/proxy', methods=['GET', 'POST'])
def proxy_request():
    # Determine target URL from request path
    path = request.args.get('path', '')
    provider = request.args.get('provider', 'original')

    base_url, api_key_server = get_base_url_and_key(provider)
    target_url = f"{base_url}/{path}"

    # Get API key from client header or use server's key
    api_key_client = request.headers.get('X-API-KEY')
    final_api_key = api_key_client or api_key_server
    
    if not final_api_key:
        return jsonify({"error": "API key is missing"}), 401

    headers = {
        "Authorization": f"Bearer {final_api_key}",
        "Content-Type": request.content_type,
        "Accept": request.accept_mimetypes.to_header()
    }

    try:
        if request.method == 'POST':
            resp = requests.post(target_url, headers=headers, data=request.get_data())
        else: # GET
            resp = requests.get(target_url, headers=headers)

        # Forward the response from the target API
        return Response(resp.content, status=resp.status_code, content_type=resp.headers.get('content-type'))

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502

# This allows Vercel to pick up the Flask app
if __name__ == "__main__":
    app.run() 