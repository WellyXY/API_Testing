#!/bin/bash

# Seedream API 测试脚本 (使用 curl)
# 基于 BytePlus ModelArk 文档

API_KEY="70f23192-0f0c-47d2-9bbf-961f70a17a92"
BASE_URL="https://ark.ap-southeast.bytepluses.com/api/v3"

# 模型配置
SEEDREAM_3_MODEL="ep-20250806055257-l5f4r"
SEEDREAM_4_MODEL="ep-20250921042133-t769x"

echo "🚀 开始测试 Seedream API"
echo "=================================================="

# 测试 Seedream 3.0
echo ""
echo "🎨 测试 Seedream 3.0"
echo "📝 提示词: A beautiful sunset over mountains"

curl -X POST "${BASE_URL}/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "model": "'${SEEDREAM_3_MODEL}'",
    "prompt": "A beautiful sunset over mountains, digital art style",
    "n": 1,
    "size": "1024x1024",
    "response_format": "url"
  }' | jq '.'

echo ""
echo "=================================================="

# 测试 Seedream 4.0
echo ""
echo "🎨 测试 Seedream 4.0"
echo "📝 提示词: A cute cat playing in garden"

curl -X POST "${BASE_URL}/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "model": "'${SEEDREAM_4_MODEL}'",
    "prompt": "A cute cat playing in garden, cartoon style",
    "n": 1,
    "size": "1024x1024",
    "response_format": "url"
  }' | jq '.'

echo ""
echo "🎯 测试完成!"

