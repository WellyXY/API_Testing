#!/bin/bash

# 快速图像生成脚本 - 直接输入prompt
# 使用方法: ./quick_generate.sh "your prompt here"

API_KEY="70f23192-0f0c-47d2-9bbf-961f70a17a92"
BASE_URL="https://ark.ap-southeast.bytepluses.com/api/v3"
SEEDREAM_4_MODEL="ep-20250921042133-t769x"

if [ $# -eq 0 ]; then
    echo "使用方法: ./quick_generate.sh \"your prompt here\""
    echo "例如: ./quick_generate.sh \"a beautiful woman in red dress\""
    exit 1
fi

USER_PROMPT="$1"

# 添加高质量增强关键词
ENHANCED_PROMPT="$USER_PROMPT, ultra high quality, 8K resolution, hyperrealistic, professional photography, perfect lighting, sharp focus, detailed, masterpiece, best quality"

echo "🎨 快速图像生成"
echo "📝 原始 prompt: $USER_PROMPT"
echo "✨ 增强 prompt: $ENHANCED_PROMPT"
echo "⏳ 生成中..."

# 生成图像
curl -s -X POST "${BASE_URL}/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d "{
    \"model\": \"${SEEDREAM_4_MODEL}\",
    \"prompt\": \"${ENHANCED_PROMPT}\",
    \"n\": 1,
    \"size\": \"1024x1024\",
    \"response_format\": \"url\"
  }" > temp_response.json

# 检查响应
if command -v jq >/dev/null 2>&1; then
    echo "📄 API 响应:"
    cat temp_response.json | jq '.'
    
    # 提取并下载图像
    url=$(cat temp_response.json | jq -r '.data[0].url' 2>/dev/null)
    if [ "$url" != "null" ] && [ "$url" != "" ]; then
        timestamp=$(date +%s)
        filename="quick_gen_${timestamp}.jpeg"
        echo "⬇️ 下载到: $filename"
        curl -s -o "$filename" "$url"
        echo "✅ 完成: $filename"
        
        # 显示文件信息
        ls -lah "$filename"
    else
        echo "❌ 无法获取图像URL"
    fi
else
    echo "📄 原始响应:"
    cat temp_response.json
fi

# 清理临时文件
rm -f temp_response.json
