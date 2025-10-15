#!/bin/bash

# 基于参考图像的生成脚本
# 使用 SeedEdit 进行图像编辑，保持人物相似度

API_KEY="70f23192-0f0c-47d2-9bbf-961f70a17a92"
BASE_URL="https://ark.ap-southeast.bytepluses.com/api/v3"
SEEDEDIT_MODEL="ep-20250806055507-zhskr"

echo "🎨 基于参考图像的生成工具"
echo "=================================================="

# 显示可用图像
echo "📁 可用的参考图像:"
ls -la *.jpeg *.jpg *.png 2>/dev/null | head -10

echo ""
read -p "请输入参考图像文件名: " reference_image

if [ ! -f "$reference_image" ]; then
    echo "❌ 文件不存在: $reference_image"
    exit 1
fi

echo ""
read -p "请输入您想要的变化描述: " user_prompt

# 构建保持人物特征的prompt
enhanced_prompt="$user_prompt, keep the same facial features, maintain the same person's identity, same face structure, high quality, detailed, professional photography"

echo ""
echo "📝 原始描述: $user_prompt"
echo "✨ 增强描述: $enhanced_prompt"
echo "🖼️ 参考图像: $reference_image"
echo "⏳ 正在处理..."

# 使用 SeedEdit 进行图像编辑
curl -X POST "${BASE_URL}/images/edits" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "model=${SEEDEDIT_MODEL}" \
  -F "image=@${reference_image}" \
  -F "prompt=${enhanced_prompt}" \
  -F "n=1" \
  -F "size=1024x1024" \
  -o edit_response.json

echo ""
echo "📄 API 响应:"

# 检查响应是否为JSON
if command -v jq >/dev/null 2>&1; then
    if jq empty edit_response.json 2>/dev/null; then
        cat edit_response.json | jq '.'
        
        # 尝试提取URL
        url=$(cat edit_response.json | jq -r '.data[0].url' 2>/dev/null)
        if [ "$url" != "null" ] && [ "$url" != "" ]; then
            timestamp=$(date +%s)
            filename="edited_${timestamp}.jpeg"
            echo "⬇️ 下载编辑后的图像到: $filename"
            curl -s -o "$filename" "$url"
            echo "✅ 图像已保存: $filename"
            ls -lah "$filename"
        else
            echo "⚠️ 未找到图像URL，可能需要检查API响应"
        fi
    else
        echo "📄 原始响应 (非JSON格式):"
        cat edit_response.json
    fi
else
    echo "📄 原始响应:"
    cat edit_response.json
fi

# 清理临时文件
rm -f edit_response.json

echo ""
echo "🎯 完成!"
