#!/bin/bash

# SeedEdit API 测试脚本
# 专门用于图像编辑功能

API_KEY="70f23192-0f0c-47d2-9bbf-961f70a17a92"
BASE_URL="https://ark.ap-southeast.bytepluses.com/api/v3"
SEEDEDIT_MODEL="ep-20250806055507-zhskr"

echo "🖼️ SeedEdit 图像编辑测试"
echo "=================================================="

# 显示可用图像
echo "📁 可用的输入图像:"
ls -la *.jpeg *.jpg *.png 2>/dev/null | head -5

echo ""
read -p "请输入图像文件名: " input_image

if [ ! -f "$input_image" ]; then
    echo "❌ 文件不存在: $input_image"
    exit 1
fi

echo ""
read -p "请输入编辑指令: " edit_prompt

echo ""
echo "📝 编辑指令: $edit_prompt"
echo "🖼️ 输入图像: $input_image"
echo "⏳ 正在编辑..."

# 方法1: 尝试标准的 images/edits 端点
echo ""
echo "🔄 方法1: 使用 /images/edits 端点"
curl -v -X POST "${BASE_URL}/images/edits" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "model=${SEEDEDIT_MODEL}" \
  -F "image=@${input_image}" \
  -F "prompt=${edit_prompt}" \
  -F "n=1" \
  -F "size=1024x1024" \
  -o seededit_response1.json

echo ""
echo "📄 方法1 响应:"
if [ -f "seededit_response1.json" ]; then
    cat seededit_response1.json
    echo ""
fi

# 方法2: 尝试不同的参数格式
echo ""
echo "🔄 方法2: 使用不同参数格式"
curl -v -X POST "${BASE_URL}/images/generations" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "model=${SEEDEDIT_MODEL}" \
  -F "image=@${input_image}" \
  -F "prompt=${edit_prompt}" \
  -F "response_format=url" \
  -o seededit_response2.json

echo ""
echo "📄 方法2 响应:"
if [ -f "seededit_response2.json" ]; then
    cat seededit_response2.json
    echo ""
fi

# 方法3: 尝试 JSON 格式 (如果支持base64)
echo ""
echo "🔄 方法3: 检查是否需要base64编码"
echo "将图像转换为base64..."
base64_image=$(base64 -i "$input_image")
echo "Base64长度: ${#base64_image} 字符"

curl -v -X POST "${BASE_URL}/images/edits" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d "{
    \"model\": \"${SEEDEDIT_MODEL}\",
    \"image\": \"data:image/jpeg;base64,${base64_image}\",
    \"prompt\": \"${edit_prompt}\",
    \"n\": 1,
    \"size\": \"1024x1024\"
  }" \
  -o seededit_response3.json

echo ""
echo "📄 方法3 响应:"
if [ -f "seededit_response3.json" ]; then
    cat seededit_response3.json
    echo ""
fi

# 检查哪个方法成功了
echo ""
echo "🔍 检查响应结果..."

for i in 1 2 3; do
    response_file="seededit_response${i}.json"
    if [ -f "$response_file" ]; then
        echo "--- 方法${i} ---"
        if command -v jq >/dev/null 2>&1; then
            if jq empty "$response_file" 2>/dev/null; then
                url=$(jq -r '.data[0].url // empty' "$response_file" 2>/dev/null)
                if [ -n "$url" ] && [ "$url" != "null" ]; then
                    echo "✅ 找到图像URL!"
                    timestamp=$(date +%s)
                    output_file="seededit_${timestamp}.jpeg"
                    echo "⬇️ 下载到: $output_file"
                    curl -s -o "$output_file" "$url"
                    echo "✅ 完成: $output_file"
                    ls -lah "$output_file"
                    break
                else
                    echo "⚠️ 未找到有效的图像URL"
                fi
            else
                echo "⚠️ 响应不是有效的JSON"
            fi
        else
            echo "⚠️ 需要安装jq来解析JSON"
        fi
    fi
done

# 清理临时文件
rm -f seededit_response*.json

echo ""
echo "🎯 SeedEdit 测试完成!"
