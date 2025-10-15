#!/bin/bash

# 批量 i2i 脚本 - 处理所有 ref 图片
# 您可以自己输入 prompt

API_KEY="70f23192-0f0c-47d2-9bbf-961f70a17a92"
BASE_URL="https://ark.ap-southeast.bytepluses.com/api/v3"
SEEDREAM_4_MODEL="ep-20250921042133-t769x"

# 设置路径
REF_DIR="images/ref"
OUTPUT_DIR="images/generated"
cd "/Users/welly/Desktop/Character folder"

echo "🎨 批量 i2i 图像编辑"
echo "=================================================="

# 获取所有参考图片
existing_images=()
for ext in jpg jpeg png JPG JPEG PNG; do
    for img in $REF_DIR/*.$ext; do
        if [ -f "$img" ]; then
            existing_images+=("$img")
        fi
    done
done

if [ ${#existing_images[@]} -eq 0 ]; then
    echo "❌ 未找到参考图片"
    exit 1
fi

echo "📁 找到 ${#existing_images[@]} 张参考图片:"
for i in "${!existing_images[@]}"; do
    echo "  $((i+1)). ${existing_images[$i]}"
done

echo ""
read -p "📝 请输入您的 prompt: " user_prompt

if [ -z "$user_prompt" ]; then
    echo "❌ Prompt 不能为空"
    exit 1
fi

# 创建批次文件夹
batch_timestamp=$(date +%Y%m%d_%H%M%S)
batch_folder="${OUTPUT_DIR}/batch_${batch_timestamp}"
mkdir -p "$batch_folder"

echo ""
echo "📁 创建批次文件夹: $batch_folder"
echo "🎨 使用模型: ${SEEDREAM_4_MODEL}"
echo "📐 分辨率: 2K"
echo "📝 Prompt: $user_prompt"
echo "⏳ 开始批量处理..."
echo "=================================================="

# 处理每张图片
for i in "${!existing_images[@]}"; do
    img="${existing_images[$i]}"
    img_name=$(basename "$img")
    img_name_no_ext="${img_name%.*}"
    
    echo ""
    echo "🖼️  [$((i+1))/${#existing_images[@]}] 处理: $img_name"
    
    # 检查文件大小
    file_size=$(stat -f%z "$img" 2>/dev/null || stat -c%s "$img" 2>/dev/null)
    if [ "$file_size" -gt 5000000 ]; then
        echo "   ⚠️  文件太大 ($(echo "scale=1; $file_size/1024/1024" | bc)MB)，跳过"
        continue
    fi
    
    # 转换为 base64
    echo "   🔄 转换为 base64..."
    image_b64=$(base64 -i "$img" | tr -d '\n')
    
    # 创建临时JSON文件
    temp_json=$(mktemp)
    cat > "$temp_json" << EOF
{
  "model": "${SEEDREAM_4_MODEL}",
  "prompt": "${user_prompt}",
  "image": "data:image/jpeg;base64,${image_b64}",
  "sequential_image_generation": "disabled",
  "response_format": "url",
  "size": "2K",
  "stream": false,
  "watermark": true
}
EOF
    
    # 调用 API
    echo "   🚀 调用 API..."
    
    response=$(curl -s -X POST "${BASE_URL}/images/generations" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer ${API_KEY}" \
      -d @"$temp_json")
    
    # 删除临时文件
    rm -f "$temp_json"
    
    # 提取 URL
    if command -v jq >/dev/null 2>&1; then
        url=$(echo "$response" | jq -r '.data[0].url' 2>/dev/null)
    else
        url=$(echo "$response" | grep -o '"url":"[^"]*' | cut -d'"' -f4)
    fi
    
    # 检查响应中是否有错误
    error_code=$(echo "$response" | jq -r '.error.code // empty' 2>/dev/null)
    
    if [ ! -z "$error_code" ]; then
        echo "   ❌ API 错误: $error_code"
        error_msg=$(echo "$response" | jq -r '.error.message // empty' 2>/dev/null)
        echo "   📝 错误信息: $error_msg"
        
        if [ "$error_code" = "OutputImageSensitiveContentDetected" ]; then
            echo "   💡 提示: 输出内容被检测为敏感，请修改prompt或使用不同的参考图片"
        fi
    elif [ "$url" != "null" ] && [ ! -z "$url" ]; then
        # 生成输出文件名 (保存到批次文件夹)
        timestamp=$(date +%s)
        output_file="${batch_folder}/i2i_${img_name_no_ext}_${timestamp}.jpeg"
        
        echo "   ⬇️  下载到: $output_file"
        curl -s -o "$output_file" "$url"
        
        if [ -f "$output_file" ]; then
            file_size=$(ls -lah "$output_file" | awk '{print $5}')
            echo "   ✅ 完成: $output_file ($file_size)"
        else
            echo "   ❌ 下载失败"
        fi
    else
        echo "   ❌ API 调用失败"
        echo "   响应: $response"
    fi
    
    # 避免请求过快
    if [ $((i+1)) -lt ${#existing_images[@]} ]; then
        echo "   ⏱️  等待 2 秒..."
        sleep 2
    fi
done

echo ""
echo "=================================================="
echo "🎯 批量处理完成!"
echo "📁 批次文件夹: $batch_folder"
echo ""
echo "生成的文件:"
ls -lah "$batch_folder"
