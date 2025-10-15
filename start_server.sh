#!/bin/bash

# 启动 Parrot API 服务器的脚本（自动使用虚拟环境）

clear
cat << "EOF"
╔═══════════════════════════════════════════════╗
║   🦜 Parrot API Server - 启动脚本           ║
╚═══════════════════════════════════════════════╝
EOF

echo ""
echo "📋 检查环境..."
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在"
    echo "   正在创建虚拟环境..."
    python3 -m venv venv
    echo "✅ 虚拟环境已创建"
    echo ""
    echo "   正在安装依赖..."
    source venv/bin/activate
    pip install -r requirements.txt > /dev/null 2>&1
    echo "✅ 依赖已安装"
else
    echo "✅ 虚拟环境存在"
fi

echo ""
echo "🚀 激活虚拟环境..."
source venv/bin/activate
echo "✅ 虚拟环境已激活"

echo ""
echo "═══════════════════════════════════════════════"
echo ""
echo "🎯 启动服务器..."
echo ""
echo "📍 服务器将运行在: http://localhost:8000"
echo "🔗 API 端点: /api/generate"
echo "📝 按 Ctrl+C 停止服务器"
echo ""
echo "═══════════════════════════════════════════════"
echo ""

# 根据目录中的服务器脚本启动
if [ -f "parrot_proxy_server.py" ]; then
    python parrot_proxy_server.py
elif [ -f "parrot_batch_server.py" ]; then
    python parrot_batch_server.py
else
    echo "❌ 找不到服务器脚本"
    echo "   请确保以下文件之一存在:"
    echo "   - parrot_proxy_server.py"
    echo "   - parrot_batch_server.py"
    exit 1
fi

