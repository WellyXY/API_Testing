#!/bin/bash

# 创建目标文件夹
mkdir -p download/Benchmark

# 定义下载函数
download_video() {
  video_name=$1
  video_url=$2
  echo "========================================================"
  echo "下载视频: $video_name"
  echo "页面URL: $video_url"
  
  # 使用curl获取页面内容
  echo "获取视频页面..."
  page_content=$(curl -s "$video_url")
  
  # 提取视频直链
  video_direct_url=$(echo "$page_content" | grep -o '"url":"[^"]*\.mp4"' | sed 's/"url":"//g' | sed 's/"//g' | sed 's/\\u002F/\//g')
  
  if [ -z "$video_direct_url" ]; then
    echo "❌ 未找到视频直链"
    return 1
  fi
  
  echo "找到视频直链: $video_direct_url"
  output_file="download/Benchmark/${video_name}.mp4"
  
  # 下载视频
  echo "正在下载到: $output_file"
  curl -L "$video_direct_url" -o "$output_file" --progress-bar
  
  if [ $? -eq 0 ]; then
    echo "✅ 下载成功!"
    return 0
  else
    echo "❌ 下载失败"
    return 1
  fi
}

# 计数器
success=0
failed=0

# 视频列表 - 使用简单数组

# 视频名称数组
names=(
  "Video-3_Brianne"
  "Video-4"
  "Video-5"
  "Video-7"
  "Video-8"
  "Video-9"
  "Video-10"
  "Video-11"
  "Video-12"
  "Video-13"
  "Video-14"
  "Video-15"
  "Video-16"
  "Video-17"
  "Video-18"
  "Video-19"
  "Video-20"
  "Video-21"
  "Video-22"
  "Video-23"
  "Video-24"
)

# 视频URL数组
urls=(
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/b655b0b8-3837-4e63-8053-341c4035a68f"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/55393631-da99-40c7-8c41-cffc0469aa2f"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/a0c7942a-bdb9-4687-a743-5dd54b9e41ed"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/d44a5a2b-7d9a-4e2c-9b45-2358bb505bcf"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/3c34515d-cd6a-44f5-b3f4-142738181b4a"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/94e676d4-6ca8-4784-b78b-b0726806ac69"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/1edc97df-23d5-4b4b-96df-ab2c6e3b3e43"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/a18c5da5-9580-43fc-a6d3-25464bc4eaf0"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/c7ac14c6-5242-4c14-97f3-eb108979aab7"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/afb323f3-e9d4-46c7-8b0a-54aa121102c2"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/0817f8b5-e43c-4672-b0cd-69483bb07f11"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/25023c0e-651f-46c5-bd7a-2b6089158372"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/fad77112-2af1-4863-9851-789d1affff70"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/19b002ee-5c25-4e9b-9039-70b77b0fd5c0"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/c93a0737-2af7-49bf-85e3-b01c1bfaf409"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/d5ada7b4-6394-4e2d-9e66-0fcdd6d60ad8"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/9588f8eb-b091-4592-9d48-c5b0b2a5bce8"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/c7ac14c6-5242-4c14-97f3-eb108979aab7"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/07b2da58-327d-42a4-b5ff-b46f8ffa588c"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/b9f39d28-75dd-4625-855c-effd9f29a5d2"
  "https://pika-git-feat-model-25-pika-labs.vercel.app/video/bd60ef28-f6bb-42ee-a772-621cab940b97"
)

total=${#names[@]}

# 遍历数组下载视频
for ((i=0; i<${#names[@]}; i++)); do
  name=${names[$i]}
  url=${urls[$i]}
  
  echo ""
  echo "[$(($i+1))/$total] 处理视频: $name"
  
  if download_video "$name" "$url"; then
    ((success++))
  else
    ((failed++))
  fi
done

# 打印总结
echo ""
echo "========================================================"
echo "下载完成! 总数: $total, 成功: $success, 失败: $failed"
echo "文件保存在: $(pwd)/download/Benchmark/"
echo "========================================================" 