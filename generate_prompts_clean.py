#!/usr/bin/env python3
"""
简洁版本 - 只输出 Image & Video Prompts

用法：
    python3 generate_prompts_clean.py <image_file> <video_prompt>
"""

import sys
from PIL import Image
from image_prompt_generator import generate_variant_prompts, generate_video_prompts_for_images

def main():
    if len(sys.argv) < 3:
        print("用法: python3 generate_prompts_clean.py <image_file> <video_prompt>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    video_prompt = sys.argv[2]
    
    # 加载图片
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"❌ 无法加载图片: {e}")
        sys.exit(1)
    
    # 生成图片 prompts
    print("⏳ 正在生成图片 prompts...")
    image_prompts = generate_variant_prompts(
        user_prompt="Generate prompts",
        image=image,
        max_retries=3
    )
    
    if not image_prompts:
        print("❌ 图片 prompts 生成失败")
        sys.exit(1)
    
    # 并行生成视频 prompts
    print("⏳ 正在并行生成视频 prompts...")
    video_prompts = generate_video_prompts_for_images(
        image_prompts=image_prompts,
        video_prompt=video_prompt,
        parallel=True  # 并行模式
    )
    
    # 输出结果 - 只输出 prompts
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80 + "\n")
    
    for i, (img_p, vid_p) in enumerate(zip(image_prompts, video_prompts), 1):
        print(f"[PAIR {i}]")
        print()
        print(f"IMAGE_PROMPT_{i}:")
        print(img_p)
        print()
        print(f"VIDEO_PROMPT_{i}:")
        print(vid_p if vid_p else "❌ FAILED")
        print()
        print("-" * 80)
        print()


if __name__ == "__main__":
    main()

