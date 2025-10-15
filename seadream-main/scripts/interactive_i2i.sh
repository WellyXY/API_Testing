#!/bin/bash

# 交互式图像到图像生成脚本
# 支持自定义prompt和高质量输出

API_KEY="70f23192-0f0c-47d2-9bbf-961f70a17a92"
BASE_URL="https://ark.ap-southeast.bytepluses.com/api/v3"

# 模型配置
SEEDREAM_4_MODEL="ep-20250921042133-t769x"
SEEDEDIT_MODEL="ep-20250806055507-zhskr"

echo "🎨 交互式图像生成工具"
echo "=================================================="

# 显示可用的输入图像
echo "📁 可用的输入图像:"
ls -la *.jpeg *.jpg *.png 2>/dev/null | grep -E "\.(jpeg|jpg|png)$" || echo "未找到图像文件"

echo ""
echo "请选择生成方式:"
echo "1) 使用 Seedream 4.0 (文本到图像，高质量)"
echo "2) 使用 SeedEdit (图像编辑)"
echo "3) 退出"

read -p "请选择 (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🎨 使用 Seedream 4.0 进行高质量图像生成"
        read -p "请输入您的 prompt: " user_prompt
        
        # 添加高质量关键词
        enhanced_prompt="$user_prompt, high quality, 8K resolution, ultra detailed, professional photography, sharp focus, vivid colors, masterpiece"
        
        echo "📝 增强后的 prompt: $enhanced_prompt"
        echo "⏳ 正在生成图像..."
        
        curl -X POST "${BASE_URL}/images/generations" \
          -H "Content-Type: application/json" \
          -H "Authorization: Bearer ${API_KEY}" \
          -d "{
            \"model\": \"${SEEDREAM_4_MODEL}\",
            \"prompt\": \"${enhanced_prompt}\",
            \"n\": 1,
            \"size\": \"1024x1024\",
            \"response_format\": \"url\"
          }" > response.json
        
        echo ""
        echo "📄 API 响应:"
        cat response.json | jq '.'
        
        # 提取URL并下载
        url=$(cat response.json | jq -r '.data[0].url' 2>/dev/null)
        if [ "$url" != "null" ] && [ "$url" != "" ]; then
            timestamp=$(date +%s)
            filename="generated_${timestamp}.jpeg"
            echo "⬇️ 下载图像到: $filename"
            curl -o "$filename" "$url"
            echo "✅ 图像已保存: $filename"
        else
            echo "❌ 未能获取图像URL"
        fi
        ;;
        
    2)
        echo ""
        echo "🖼️ 使用 SeedEdit 进行图像编辑"
        read -p "请输入输入图像文件名: " input_image
        
        if [ ! -f "$input_image" ]; then
            echo "❌ 文件不存在: $input_image"
            exit 1
        fi
        
        read -p "请输入您的编辑 prompt: " user_prompt
        
        # 添加高质量关键词
        enhanced_prompt="$user_prompt, high quality, detailed, sharp, professional"
        
        echo "📝 增强后的 prompt: $enhanced_prompt"
        echo "⏳ 正在编辑图像..."
        
        curl -X POST "${BASE_URL}/images/edits" \
          -H "Authorization: Bearer ${API_KEY}" \
          -F "model=${SEEDEDIT_MODEL}" \
          -F "image=@${input_image}" \
          -F "prompt=${enhanced_prompt}" \
          -F "n=1" \
          -F "size=1024x1024" > edit_response.json
        
        echo ""
        echo "📄 API 响应:"
        cat edit_response.json
        
        # 如果响应是JSON格式，尝试提取URL
        if command -v jq >/dev/null 2>&1; then
            url=$(cat edit_response.json | jq -r '.data[0].url' 2>/dev/null)
            if [ "$url" != "null" ] && [ "$url" != "" ]; then
                timestamp=$(date +%s)
                filename="edited_${timestamp}.jpeg"
                echo "⬇️ 下载编辑后的图像到: $filename"
                curl -o "$filename" "$url"
                echo "✅ 图像已保存: $filename"
            fi
        fi
        ;;
        
    3)
        echo "👋 再见!"
        exit 0
        ;;
        
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "🎯 完成!"
