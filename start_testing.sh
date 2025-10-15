#!/bin/bash

# 一键启动 Testing Backend 的脚本
# 自动完成所有设置步骤

clear
cat << "EOF"
╔═══════════════════════════════════════════════╗
║   🧪 Testing Backend - 一键启动              ║
╚═══════════════════════════════════════════════╝
EOF

echo ""
echo "📋 检查环境..."
echo ""

# 1. 检查 ssh_key 是否存在
if [ ! -f "ssh_key" ]; then
    echo "❌ 错误: 找不到 ssh_key 文件"
    echo "   请确保 ssh_key 在当前目录"
    exit 1
fi
echo "✅ SSH 密钥文件存在"

# 2. 设置正确的权限
chmod 600 ssh_key
echo "✅ SSH 密钥权限已设置 (600)"

# 3. 检查端口是否被占用
if lsof -Pi :9580 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  端口 9580 已被占用"
    read -p "   是否要终止占用该端口的进程? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        lsof -ti:9580 | xargs kill -9 2>/dev/null
        echo "   ✅ 已终止占用进程"
        sleep 1
    else
        echo "   ⚠️  继续可能会失败"
    fi
fi

# 4. 检查是否已有 SSH 隧道在运行
ssh_tunnel_running=false
if pgrep -f "ssh.*52.54.232.223.*9580" >/dev/null 2>&1; then
    echo "⚠️  检测到 SSH 隧道已在运行"
    ssh_tunnel_running=true
fi

echo ""
echo "═══════════════════════════════════════════════"
echo ""

if [ "$ssh_tunnel_running" = true ]; then
    echo "✅ SSH 隧道已经在运行中"
    echo ""
    echo "🔍 正在测试连接..."
else
    echo "🚀 正在启动 SSH 隧道..."
    echo ""
    echo "⚠️  SSH 隧道将在后台运行"
    echo "⚠️  使用 'pkill -f \"ssh.*52.54.232.223.*9580\"' 来停止"
    echo ""
    
    # 在后台启动 SSH 隧道
    ssh -i ssh_key \
        -L 9580:localhost:9580 \
        -N \
        -o "ServerAliveInterval=60" \
        -o "ServerAliveCountMax=3" \
        -o "StrictHostKeyChecking=no" \
        -f \
        ec2-user@52.54.232.223
    
    if [ $? -eq 0 ]; then
        echo "✅ SSH 隧道已启动"
        sleep 2  # 等待隧道建立
    else
        echo "❌ SSH 隧道启动失败"
        echo "   请检查网络连接和服务器状态"
        exit 1
    fi
    
    echo ""
    echo "🔍 正在测试连接..."
fi

echo ""

# 5. 测试连接
if command -v curl &> /dev/null; then
    response=$(curl -s -o /dev/null -w "%{http_code}" -X GET "http://localhost:9580/api/v1/generate/v0/videos/test-id" \
         -H "X-API-Key: test-api-key-123456" --max-time 5 2>/dev/null)
    
    if [ "$response" == "200" ] || [ "$response" == "404" ] || [ "$response" == "401" ]; then
        echo "✅ API 服务可访问"
        echo "   HTTP 状态码: $response"
    else
        echo "⚠️  API 响应异常"
        echo "   HTTP 状态码: $response"
    fi
else
    echo "⚠️  未安装 curl，跳过连接测试"
fi

echo ""
echo "═══════════════════════════════════════════════"
echo ""
echo "🎉 设置完成！"
echo ""
echo "📌 下一步操作："
echo ""
echo "   1. 在浏览器中打开: parrot_api_frontend.html"
echo "   2. 选择 Provider: 🧪 Testing (New Architecture)"
echo "   3. 开始测试！"
echo ""
echo "═══════════════════════════════════════════════"
echo ""
echo "💡 有用的命令："
echo ""
echo "   • 查看 SSH 隧道状态:"
echo "     lsof -i :9580"
echo ""
echo "   • 停止 SSH 隧道:"
echo "     pkill -f \"ssh.*52.54.232.223.*9580\""
echo ""
echo "   • 详细测试:"
echo "     ./test_testing_backend.sh"
echo ""
echo "   • 查看文档:"
echo "     cat QUICKSTART_TESTING.md"
echo ""
echo "═══════════════════════════════════════════════"
echo ""

