#!/bin/bash

# Seedream 4.0 图像到图像 (i2i) 脚本
# 支持真正的图像编辑功能

API_KEY="70f23192-0f0c-47d2-9bbf-961f70a17a92"
BASE_URL="https://ark.ap-southeast.bytepluses.com/api/v3"
SEEDREAM_4_MODEL="ep-20250921042133-t769x"

echo "🎨 Seedream 4.0 图像到图像编辑"
echo "=================================================="

# 显示可用图像
echo "📁 可用的输入图像:"
ls -la *.jpeg *.jpg *.png 2>/dev/null | head -5

echo ""
read -p "请输入输入图像文件名: " input_image

if [ ! -f "$input_image" ]; then
    echo "❌ 文件不存在: $input_image"
    exit 1
fi

echo ""
read -p "请输入编辑指令: " edit_prompt

echo ""
echo "📝 编辑指令: $edit_prompt"
echo "🖼️ 输入图像: $input_image"
echo "⏳ 正在处理..."

# 将图像转换为base64
echo "🔄 转换图像为base64..."
image_b64=$(base64 -i "$input_image")

# 调用 Seedream 4.0 i2i API
curl -s -X POST "${BASE_URL}/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d "{
    \"model\": \"${SEEDREAM_4_MODEL}\",
    \"prompt\": \"${edit_prompt}\",
    \"image\": \"data:image/jpeg;base64,${image_b64}\",
    \"n\": 1,
    \"size\": \"1024x1024\",
    \"response_format\": \"url\"
  }" > i2i_response.json

echo ""
echo "📄 API 响应:"
if command -v jq >/dev/null 2>&1; then
    cat i2i_response.json | jq '.'
    
    # 提取URL并下载
    url=$(cat i2i_response.json | jq -r '.data[0].url' 2>/dev/null)
    if [ "$url" != "null" ] && [ "$url" != "" ]; then
        timestamp=$(date +%s)
        filename="i2i_${timestamp}.jpeg"
        echo "⬇️ 下载编辑后的图像到: $filename"
        curl -s -o "$filename" "$url"
        echo "✅ 完成: $filename"
        ls -lah "$filename"
    else
        echo "❌ 未能获取图像URL"
    fi
else
    echo "📄 原始响应:"
    cat i2i_response.json
fi

# 清理临时文件
rm -f i2i_response.json

echo ""
echo "🎯 Seedream 4.0 i2i 编辑完成!"
