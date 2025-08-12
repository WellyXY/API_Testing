# Snax API Testing Tool

A tool for testing the Snax Labs API that supports image-to-video, with Staging provider only.

## 🌟 Features

- 📸 **Image to Video**: Upload an image to generate a video
- 🎬 **Provider**: Staging API only
- 🔄 **Live Status**: Auto-poll for generation progress
- ⚡ **Batch**: Upload and process in bulk
- 🔧 **Proxy Server**: Built-in Flask proxy to resolve CORS
- 💾 **Downloads**: Single and batch download

## 🔧 API Provider

### Staging API  
- **Base URL**: `https://089e99349ace.pikalabs.app`
- **API Key**: `pk_fnOLPQFrhk96QscYG9hIUSw-Jn5ygl_ehSUWa9PvwZM`
- **Supported versions**: v2.2
- **Endpoint**: `/generate/2.2/i2v`

## 🚀 Getting Started

### 1. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Start proxy server
```bash
python3 pika_proxy_server.py
```
Server starts on http://localhost:5003

### 3. Open browser
Visit http://localhost:5003 to use the tool

## 📋 Usage

1. **Provider**: Fixed to Staging
2. **API Version**: Staging-only versions
3. **API Key**: Optional, falls back to server default
4. **Test Connection**: Click to validate API is reachable
5. **Upload Image**: Drag and drop or click to upload
6. **Prompt**: Optional; describe desired effect
7. **Generate**: Click "Start Generating Video"
8. **Progress**: Auto-updates
9. **Download**: Download when finished

## 🔍 API Endpoints

### Proxy Server Endpoints
- `GET /` - Frontend
- `POST /generate/2.2/i2v` - Staging API v2.2 (direct proxy)  
- `POST /api/generate` - Generation endpoint (Staging only)
- `GET /videos/{video_id}` - Check video status
- `GET /api/info` - Providers info

### Request parameters
- `image` - image file (required)
- `promptText` - prompt text (optional)
- `provider` - fixed to 'staging'
- `version` - fixed to 'v2.2'

## 🛠️ Tech Stack

- **Backend**: Python Flask + Flask-CORS + requests
- **Frontend**: HTML + CSS + JavaScript
- **API**: Snax Labs API (Staging)

## 📝 Changelog

### Latest
- ✅ Rebranded to Snax
- ✅ Staging-only
- ✅ Simplified provider/version selection
- ✅ Unified proxy endpoint structure
- ✅ Improved error handling and debugging info
 

### Previous
- ✅ Basic image-to-video
- ✅ Batch support
- ✅ Video download
- ✅ Proxy server for CORS

## 🔐 Security

- API Keys stored in config; handle securely
- Use environment variables for secrets in production
- Proxy is for development/testing; use a production-ready proxy in prod