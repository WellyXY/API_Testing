#!/bin/bash

# 测试新架构后端连接的脚本

echo "🧪 Testing Backend 连接测试"
echo "================================"
echo ""

# 检查端口是否开放
echo "1️⃣  检查端口 9580 是否开放..."
if lsof -Pi :9580 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "   ✅ 端口 9580 已开放（SSH 隧道可能已建立）"
else
    echo "   ❌ 端口 9580 未开放"
    echo "   请先运行: ./setup_ssh_tunnel.sh"
    exit 1
fi

echo ""
echo "2️⃣  测试 API 连接..."

# 创建一个 1x1 像素的测试图片
echo "   创建测试图片..."
convert -size 1x1 xc:black test_image.png 2>/dev/null || {
    # 如果没有 ImageMagick，使用 Python 创建
    python3 -c "from PIL import Image; Image.new('RGB', (1,1), 'black').save('test_image.png')" 2>/dev/null || {
        echo "   ⚠️  无法创建测试图片，跳过完整测试"
        echo "   安装 ImageMagick 或 Pillow 以进行完整测试: brew install imagemagick"
        
        # 仅测试 GET 请求
        echo ""
        echo "3️⃣  测试基础连接（无图片）..."
        response=$(curl -s -w "\n%{http_code}" -X GET "http://localhost:9580/api/v1/generate/v0/videos/test-id" \
             -H "X-API-Key: test-api-key-123456" 2>&1)
        
        http_code=$(echo "$response" | tail -n1)
        body=$(echo "$response" | head -n-1)
        
        echo "   HTTP 状态码: $http_code"
        echo "   响应内容: $body"
        
        if [ "$http_code" == "200" ] || [ "$http_code" == "404" ]; then
            echo "   ✅ 基础连接成功（服务器可达）"
        else
            echo "   ❌ 连接失败"
        fi
        
        exit 0
    }
}

# 测试 POST 请求
echo "   发送测试请求..."
response=$(curl -s -w "\n%{http_code}" -X POST "http://localhost:9580/api/v1/generate/v0/image-to-video" \
     -H "X-API-Key: test-api-key-123456" \
     -F "image=@test_image.png" \
     -F "promptText=test connection" 2>&1)

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

echo ""
echo "3️⃣  结果分析..."
echo "   HTTP 状态码: $http_code"
echo "   响应内容:"
echo "$body" | head -c 500
echo ""

# 清理测试文件
rm -f test_image.png

# 判断结果
if [ "$http_code" == "200" ] || [ "$http_code" == "201" ] || [ "$http_code" == "202" ]; then
    echo ""
    echo "✅ 测试成功！"
    echo "   - SSH 隧道工作正常"
    echo "   - API 服务可访问"
    echo "   - 认证通过"
    echo ""
    echo "📌 你现在可以在前端界面中使用 Testing Provider 了"
    exit 0
elif [ "$http_code" == "401" ] || [ "$http_code" == "403" ]; then
    echo ""
    echo "⚠️  认证失败"
    echo "   - SSH 隧道正常"
    echo "   - 但 API Key 可能无效"
    echo "   - 请检查 API Key: test-api-key-123456"
    exit 1
elif [ "$http_code" == "000" ] || [ -z "$http_code" ]; then
    echo ""
    echo "❌ 连接失败"
    echo "   - 无法连接到 localhost:9580"
    echo "   - 请确认 SSH 隧道是否已建立"
    echo "   - 运行: ./setup_ssh_tunnel.sh"
    exit 1
else
    echo ""
    echo "⚠️  收到意外响应"
    echo "   - HTTP 状态码: $http_code"
    echo "   - 请检查服务器状态"
    exit 1
fi

