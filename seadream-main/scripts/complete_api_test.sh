#!/bin/bash

# BytePlus ModelArk API 完整测试脚本
# 包含所有您提供的模型端点

API_KEY="70f23192-0f0c-47d2-9bbf-961f70a17a92"
BASE_URL="https://ark.ap-southeast.bytepluses.com/api/v3"

echo "🚀 BytePlus ModelArk API 完整测试"
echo "=================================================="

# 创建输出目录
mkdir -p generated_images generated_videos

# 1. 测试 Seedream 3.0 (图像生成)
echo ""
echo "🎨 测试 Seedream 3.0 - 图像生成"
curl -X POST "${BASE_URL}/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "model": "ep-20250806055257-l5f4r",
    "prompt": "A serene Japanese garden with cherry blossoms, traditional art style",
    "n": 1,
    "size": "1024x1024",
    "response_format": "url"
  }' > seedream_3_response.json

echo "✅ Seedream 3.0 测试完成，结果保存到 seedream_3_response.json"

# 2. 测试 Seedream 4.0 (图像生成)
echo ""
echo "🎨 测试 Seedream 4.0 - 图像生成"
curl -X POST "${BASE_URL}/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "model": "ep-20250921042133-t769x",
    "prompt": "A futuristic robot in a cyberpunk city, neon lights, high detail",
    "n": 1,
    "size": "1024x1024",
    "response_format": "url"
  }' > seedream_4_response.json

echo "✅ Seedream 4.0 测试完成，结果保存到 seedream_4_response.json"

# 3. 测试 SeedEdit (图像编辑)
echo ""
echo "🖼️ 测试 SeedEdit - 图像编辑"
echo "注意: SeedEdit 需要输入图像，这里显示请求格式"
cat << 'EOF'
curl -X POST "${BASE_URL}/images/edits" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F model="ep-20250806055507-zhskr" \
  -F image="@input_image.png" \
  -F prompt="Add a rainbow in the sky" \
  -F n=1 \
  -F size="1024x1024"
EOF

# 4. 测试 Seedance Lite T2V (文本到视频)
echo ""
echo "🎬 测试 Seedance Lite T2V - 文本到视频"
curl -X POST "${BASE_URL}/video/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "model": "ep-20250806055653-7g92d",
    "prompt": "A butterfly flying over a flower field in slow motion",
    "duration": 3
  }' > seedance_lite_t2v_response.json

echo "✅ Seedance Lite T2V 测试完成，结果保存到 seedance_lite_t2v_response.json"

# 5. 测试 Seedance Lite I2V (图像到视频)
echo ""
echo "🎬 测试 Seedance Lite I2V - 图像到视频"
echo "注意: I2V 需要输入图像，这里显示请求格式"
cat << 'EOF'
curl -X POST "${BASE_URL}/video/generations" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F model="ep-20250806055841-6swck" \
  -F image="@input_image.jpg" \
  -F prompt="Make the scene come alive with gentle movement" \
  -F duration=3
EOF

# 6. 测试 Seedance Pro (视频生成)
echo ""
echo "🎬 测试 Seedance Pro - 专业视频生成"
curl -X POST "${BASE_URL}/video/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "model": "ep-20250806055935-b9mgj",
    "prompt": "A majestic eagle soaring through mountain peaks at sunset, cinematic quality",
    "duration": 5
  }' > seedance_pro_response.json

echo "✅ Seedance Pro 测试完成，结果保存到 seedance_pro_response.json"

echo ""
echo "🎯 所有API测试完成!"
echo "=================================================="
echo "📁 生成的响应文件:"
ls -la *_response.json
echo ""
echo "💡 提示: 检查响应文件中的URL来下载生成的内容"

