#!/usr/bin/env python3
"""
Snax batch video generator launcher
"""

import os
import sys
import subprocess

def install_dependencies():
    """Install required dependencies"""
    print("🔄 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Check network connectivity.")
        return False
    return True

def create_directories():
    """Create required directories"""
    print("📁 Creating directories...")
    directories = ['uploads', 'generated_videos', 'downloads']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directories ready")

def start_server():
    """Start server"""
    print("🚀 Starting Snax batch video server...")
    print("📱 Frontend: http://localhost:5004")
    print("🔧 API: http://localhost:5004/batch/generate")
    print("⚠️  Please ensure you have a valid Snax API Key")
    print("-" * 50)
    
    try:
        # Import and run server
        from pika_batch_server import app
        app.run(
            host='0.0.0.0',
            port=5004,
            debug=True
        )
    except ImportError:
        print("❌ pika_batch_server.py not found")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def main():
    print("=" * 60)
    print("🎬 Snax Batch Video Generator Launcher")
    print("=" * 60)
    
    # Check requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        return
    
    # Check required files
    required_files = ['pika_batch_server.py', 'batch_frontend.html']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Missing required file: {file}")
            return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Create directories
    create_directories()
    
    # Start server
    start_server()

if __name__ == '__main__':
    main() 