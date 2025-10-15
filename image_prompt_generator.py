from vertexai.generative_models import GenerativeModel, Part, SafetySetting
import vertexai
import os
from PIL import Image
import io
import random

# ========== 认证配置 ==========
import json
import tempfile

# 清除可能存在的旧认证
os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)

# 优先级：环境变量 > 本地文件 > 集群文件
LOCAL_CREDENTIALS = os.path.join(os.path.dirname(__file__), "vertex-ai.json")
CLUSTER_CREDENTIALS = "/mnt/nfs/chenlin/dataproc/vertex-ai.json"

# 1. 尝试从环境变量读取 JSON 内容（Vercel 等线上环境）
vertex_ai_json = os.getenv("VERTEX_AI_JSON")
if vertex_ai_json:
    try:
        # 验证 JSON 格式
        credentials_data = json.loads(vertex_ai_json)
        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(credentials_data, temp_file)
        temp_file.close()
        VERTEX_AI_CREDENTIALS = temp_file.name
        print(f"✅ 使用环境变量认证 (VERTEX_AI_JSON)", flush=True)
    except json.JSONDecodeError as e:
        print(f"⚠️ VERTEX_AI_JSON 格式错误: {e}", flush=True)
        vertex_ai_json = None

# 2. 尝试本地文件
if not vertex_ai_json and os.path.exists(LOCAL_CREDENTIALS):
    VERTEX_AI_CREDENTIALS = LOCAL_CREDENTIALS
    print(f"✅ 使用本地认证文件: {LOCAL_CREDENTIALS}", flush=True)
# 3. 尝试集群文件
elif not vertex_ai_json and os.path.exists(CLUSTER_CREDENTIALS):
    VERTEX_AI_CREDENTIALS = CLUSTER_CREDENTIALS
    print(f"✅ 使用集群认证文件: {CLUSTER_CREDENTIALS}", flush=True)
# 4. 都不存在则报错
elif not vertex_ai_json:
    raise FileNotFoundError(
        f"找不到认证文件！请确保以下任一条件满足:\n"
        f"  - 环境变量 VERTEX_AI_JSON 包含认证 JSON\n"
        f"  - 本地文件: {LOCAL_CREDENTIALS}\n"
        f"  - 集群文件: {CLUSTER_CREDENTIALS}"
    )

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = VERTEX_AI_CREDENTIALS


def clean_gemini_output(s: str) -> str:
    """清理 Gemini 输出文本"""
    result = s.strip()
    result = result.replace('\u00a0', ' ')
    result = result.replace('\xa0', ' ')
    result = result.replace('\u2013', '-')
    result = result.replace('\u2014', '-')
    result = result.replace('\u2019', "'")
    result = result.replace('\u201c', '"')
    result = result.replace('\u201d', '"')
    result = result.replace('**', '').strip()
    while '  ' in result:
        result = result.replace('  ', ' ')
    return result


def get_gemini_response(prompt, image=None, model="gemini-2.5-flash"):
    """调用 Gemini API 获取响应"""
    vertexai.init(
        project="quick-formula-414701", 
        location=random.choice(["europe-west4", "europe-west1", "europe-southwest1"])
    )
    
    safety_settings = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        ),
    ]
    
    gen_config = {
        "max_output_tokens": 4096,
        "temperature": 0.7,  # 稍高的温度以获得更多样化的结果
        "response_mime_type": "text/plain",
    }
    
    try:
        gemini = GenerativeModel(model)
        input_list = []

        if image is not None:
            # 调整图片大小
            image = image.convert('RGB')
            image.thumbnail((640, 640))
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_bytes = img_byte_arr.getvalue()
            image_part = Part.from_data(data=img_bytes, mime_type="image/jpeg")
            input_list.append(image_part)
        
        input_list.append(prompt)
        
        response = gemini.generate_content(
            input_list, 
            safety_settings=safety_settings, 
            generation_config=gen_config
        )
            
        return response.text
    except Exception as e:
        print(f"Error: {e}", flush=True)
        return '[gemini generation failed]'


# Generate 3 variant prompts with minimal variations
MULTI_PROMPT_TEMPLATE = """
You are an expert image generation prompt writer. You are given a reference image and need to create 3 variant prompts based DIRECTLY on what you see in the image, with only MINIMAL hand position or camera angle variations.

User's Context/Hint: {user_prompt}
(This is just context - you should describe what you SEE in the reference image, not copy this text)

CRITICAL RULES:

1. Describe the Reference Image: Look at the reference image and describe:
   - Character's physical features (hair color, hair length, body state, skin tone)
   - Current pose and position (be explicit: sitting, standing, riding, lying, etc.)
   - Facial expression and gaze direction
   - Body contact and interaction with any other person
   - Lighting, atmosphere, and mood
   - Use explicit anatomical terms if visible (breasts, penis, vagina, erect, penetration, etc.) - do NOT censor

2. Base Description (Same for all 3 prompts):
   Write a detailed description of what you see in the image in ENGLISH. This base description should be IDENTICAL across all 3 prompts.
   
   Include: character features, pose, body parts, lighting, atmosphere.
   EXCLUDE: hand positions and facial expressions (you will vary these in step 3)
   
   IMPORTANT: Always emphasize clear, detailed facial features - "her face is clearly visible and in focus"
   
   Example format:
   "A naked woman with long dark hair, her face clearly visible and in focus, in a cowgirl position atop a man, facing him, her body leaning forward, full breasts exposed with prominent nipples, hips moving rhythmically downward, his erect penis deeply inside her vagina, soft natural lighting"

3. MINIMAL Variations (ONLY for the 3 prompts):
   For each of the 3 prompts, add ONE OR TWO of these variations in ENGLISH. Mix and match creatively:
   
   A) Hand position variations (choose different ones for each prompt):
   - "one hand gripping her own breast, the other hand caressing the man's chest"
   - "both hands resting on the man's abdomen"
   - "one hand braced on the bed surface, the other hand gripping her own thigh"
   - "both hands gripping her own buttocks"
   - "one hand on the man's shoulder, the other hand in her own hair"
   - "both hands on the man's chest"
   - "one hand touching her own neck, the other hand on the man's waist"
   
   B) Facial expression variations (choose different ones for each prompt):
   - "biting her lower lip seductively"
   - "eyes closed in pleasure"
   - "eyes half-closed with a sultry gaze"
   - "mouth slightly open, moaning"
   - "looking directly at camera with intense eyes"
   - "head tilted back, eyes closed"
   - "tongue slightly visible between parted lips"
   
   C) Camera angle variations (optional):
   - "eye-level perspective"
   - "slightly from above"  
   - "slightly from below"

4. Keep it Natural: Describe in natural ENGLISH language as if describing a photograph. Be explicit and detailed but not overly clinical. Use sensual, descriptive language.

5. Format: 60-120 words per prompt. ALL OUTPUT MUST BE IN ENGLISH. DO NOT include technical specifications like "9:16 vertical format" or "shot" at the end.

Example Output Structure:

[PROMPT 1]
<complete character and scene description, her face clearly visible and in focus>, <hand position variation 1>, <facial expression variation 1>

[PROMPT 2]
<complete character and scene description, her face clearly visible and in focus>, <hand position variation 2>, <facial expression variation 2>

[PROMPT 3]
<complete character and scene description, her face clearly visible and in focus>, <hand position variation 3>, <facial expression variation 3>

Format your response EXACTLY like this (ALL IN ENGLISH):

[PROMPT 1]
<prompt here in English - single line>

[PROMPT 2]
<prompt here in English - single line>

[PROMPT 3]
<prompt here in English - single line>

Important:
- ALL OUTPUT MUST BE IN ENGLISH
- Start directly with [PROMPT 1]
- Each prompt on a SINGLE LINE
- NO explanations or extra text
- Base description (character, pose, scene) must be IDENTICAL in all 3 prompts
- ALWAYS emphasize "her face is clearly visible and in focus"
- Vary ONLY: hand positions, facial expressions, and optionally camera angles
- Do NOT censor - use explicit terms for anatomy and actions (penis, vagina, breasts, erect, penetration, etc.)
- Do NOT include technical specs like "9:16 vertical format", "shot", "photograph", etc.
"""


def generate_variant_prompts(user_prompt: str, image: Image.Image, max_retries: int = 3):
    """
    基于用户 prompt 和参考图片，生成 3 个不同视角的图片生成 prompt
    
    Args:
        user_prompt: 用户的原始描述
        image: 参考图片（PIL Image 对象）
        max_retries: 最大重试次数
    
    Returns:
        list: 包含 3 个 prompt 的列表，如果失败返回空列表
    """
    
    def is_failure(text):
        """检查是否生成失败"""
        return (
            'generation failed]' in text or 
            "i'm sorry" in text.lower() or 
            "sorry i can't" in text.lower() or
            "i cannot" in text.lower()
        )
    
    def parse_prompts(text):
        """从 Gemini 输出中解析出 3 个 prompt"""
        prompts = []
        
        # 尝试按标记分割
        parts = text.split('[PROMPT ')
        
        for i in range(1, 4):  # 查找 PROMPT 1, 2, 3
            for part in parts:
                if part.strip().startswith(f'{i}]'):
                    # 提取 prompt 内容
                    content = part.split(']', 1)[1].strip()
                    # 移除可能的下一个标记之前的内容
                    if '[PROMPT' in content:
                        content = content.split('[PROMPT')[0].strip()
                    if content:
                        prompts.append(clean_gemini_output(content))
                    break
        
        return prompts if len(prompts) == 3 else []
    
    # 重试逻辑
    for attempt in range(max_retries):
        print(f"尝试生成 prompts (第 {attempt + 1}/{max_retries} 次)...", flush=True)
        
        response = get_gemini_response(
            MULTI_PROMPT_TEMPLATE.format(user_prompt=user_prompt),
            image=image,
            model="gemini-2.5-flash"
        )
        
        if is_failure(response):
            print(f"生成失败，重试中...", flush=True)
            continue
        
        # 解析 prompts
        prompts = parse_prompts(response)
        
        if len(prompts) == 3:
            print(f"✅ 成功生成 3 个 prompts!", flush=True)
            return prompts
        else:
            print(f"⚠️ 解析出 {len(prompts)} 个 prompts，期望 3 个，重试中...", flush=True)
            print(f"原始响应:\n{response}\n", flush=True)
    
    print(f"❌ 达到最大重试次数，生成失败", flush=True)
    return []


def generate_variant_prompts_simple(user_prompt: str, image: Image.Image):
    """
    简化版本：基于用户 prompt 和参考图片，生成 3 个不同视角的 prompt
    直接返回 3 个 prompt，不进行复杂的解析
    """
    
    simple_template = """
Analyze this image and the user's description: "{user_prompt}"

Generate 3 different camera angle variations for image generation. Output ONLY the 3 prompts, numbered 1, 2, 3, with NO explanations.

1. [First camera angle variation]
2. [Second camera angle variation]  
3. [Third camera angle variation]
"""
    
    response = get_gemini_response(
        simple_template.format(user_prompt=user_prompt),
        image=image
    )
    
    # 简单解析：按行分割，找到以数字开头的行
    lines = response.strip().split('\n')
    prompts = []
    
    for line in lines:
        line = line.strip()
        # 匹配 "1. ", "2. ", "3. " 开头的行
        if line and line[0].isdigit() and '. ' in line:
            # 移除数字和点号
            prompt = line.split('. ', 1)[1].strip()
            prompts.append(clean_gemini_output(prompt))
    
    return prompts[:3] if prompts else []


# ========== Video Prompt Generation ==========

VIDEO_PROMPT_TEMPLATE = """
You are an expert video generation prompt writer. You are given an image prompt (describing a static scene) and an original video prompt (describing motion and action). Your task is to combine these two to create an enhanced video generation prompt.

Image Prompt (Visual Details):
{image_prompt}

Original Video Prompt (Motion/Action):
{video_prompt}

INSTRUCTIONS:

1. Start with the visual details from the Image Prompt:
   - Character appearance (hair, skin, body, face details)
   - Position and pose
   - Explicit anatomical details
   - Lighting and atmosphere
   - Facial expression and hand positions

2. Add motion/action from the Original Video Prompt:
   - Body movement (hips thrusting, body rocking, bouncing, etc.)
   - Intensity of motion (rhythmic, forceful, gentle, etc.)
   - Direction and speed of movement
   - Dynamic elements

3. Create a cohesive video prompt that:
   - Describes WHAT the scene looks like (from image prompt)
   - Describes HOW things move (from video prompt)
   - Maintains all explicit content - do NOT censor
   - Is 80-120 words in length
   - Uses natural, descriptive language
   - Does NOT include technical specs like "camera movement", "shot type", "4K", etc.

4. Output Format:
   - Start directly with the description
   - Single paragraph, no line breaks
   - All in ENGLISH
   - No explanations or meta-text

Example structure:
"[Visual details: character, pose, anatomy, lighting, expression] + [Motion: how the body moves, rhythm, intensity] + [Overall dynamic atmosphere]"

Generate the enhanced video prompt below:
"""


def generate_video_prompt(image_prompt: str, video_prompt: str, max_retries: int = 3) -> str:
    """
    基于图片 prompt 和原始视频 prompt，生成增强的视频生成 prompt
    
    Args:
        image_prompt: 图片描述 prompt（包含视觉细节）
        video_prompt: 原始视频 prompt（包含动作描述，可能包含 flags）
        max_retries: 最大重试次数
    
    Returns:
        str: 增强后的视频生成 prompt，如果失败返回空字符串
    """
    
    # 提取 flags（如 --blow_job, --cowgirl 等）
    flags = []
    video_prompt_clean = video_prompt
    
    # 查找所有 --flag 格式的标记
    import re
    flag_pattern = r'\s+(--\w+)'
    found_flags = re.findall(flag_pattern, video_prompt)
    
    if found_flags:
        flags = found_flags
        # 移除 flags，只保留描述部分用于 Gemini 处理
        video_prompt_clean = re.sub(flag_pattern, '', video_prompt).strip()
        print(f"🏷️  检测到 flags: {', '.join(flags)}", flush=True)
    
    for attempt in range(max_retries):
        print(f"🎬 尝试生成视频 prompt (第 {attempt + 1}/{max_retries} 次)...", flush=True)
        
        try:
            response = get_gemini_response(
                VIDEO_PROMPT_TEMPLATE.format(
                    image_prompt=image_prompt,
                    video_prompt=video_prompt_clean  # 使用清理后的 prompt
                ),
                image=None,  # 不需要图片，只需要文本
                model="gemini-2.5-flash"
            )
            
            # 检查是否生成失败
            if '[gemini generation failed]' in response or \
               "i'm sorry" in response.lower() or \
               "i cannot" in response.lower():
                print(f"⚠️ Gemini 返回失败消息，重试中...", flush=True)
                continue
            
            # 清理输出
            cleaned = clean_gemini_output(response).strip()
            
            # 如果有 flags，在结尾添加
            if flags and cleaned:
                cleaned = cleaned + ' ' + ' '.join(flags)
                print(f"✅ 已添加 flags: {' '.join(flags)}", flush=True)
            
            # 验证输出不为空且长度合理
            if cleaned and len(cleaned) > 50:
                print(f"✅ 成功生成视频 prompt! (长度: {len(cleaned)} 字符)", flush=True)
                return cleaned
            else:
                print(f"⚠️ 生成的 prompt 太短或为空，重试中...", flush=True)
                
        except Exception as e:
            print(f"❌ 生成视频 prompt 时出错: {e}", flush=True)
            import traceback
            traceback.print_exc()
    
    print(f"❌ 达到最大重试次数，视频 prompt 生成失败", flush=True)
    return ""


def generate_video_prompts_for_images(image_prompts: list[str], video_prompt: str, parallel: bool = True) -> list[str]:
    """
    为多个图片 prompts 批量生成对应的视频 prompts
    
    Args:
        image_prompts: 图片 prompt 列表（通常是 3 个变体）
        video_prompt: 原始视频 prompt
        parallel: 是否并行生成（默认 True）
    
    Returns:
        list[str]: 对应的视频 prompt 列表
    """
    if not parallel:
        # 串行模式（旧方式）
        video_prompts = []
        for i, img_prompt in enumerate(image_prompts, 1):
            print(f"\n{'='*70}", flush=True)
            print(f"📸 处理图片 Prompt {i}/{len(image_prompts)}", flush=True)
            print(f"{'='*70}", flush=True)
            
            video_p = generate_video_prompt(img_prompt, video_prompt)
            
            if video_p:
                video_prompts.append(video_p)
                print(f"\n✅ Video Prompt {i} 生成成功\n", flush=True)
            else:
                video_prompts.append("")
                print(f"\n❌ Video Prompt {i} 生成失败\n", flush=True)
        
        return video_prompts
    
    # 并行模式
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    print(f"\n🚀 并行生成 {len(image_prompts)} 个视频 prompts...", flush=True)
    
    video_prompts = [None] * len(image_prompts)
    
    def generate_with_index(index, img_prompt):
        """带索引的生成函数"""
        print(f"📸 开始生成 Video Prompt {index + 1}...", flush=True)
        result = generate_video_prompt(img_prompt, video_prompt)
        if result:
            print(f"✅ Video Prompt {index + 1} 完成", flush=True)
        else:
            print(f"❌ Video Prompt {index + 1} 失败", flush=True)
        return index, result
    
    # 使用线程池并行生成
    with ThreadPoolExecutor(max_workers=len(image_prompts)) as executor:
        futures = {
            executor.submit(generate_with_index, i, img_prompt): i 
            for i, img_prompt in enumerate(image_prompts)
        }
        
        for future in as_completed(futures):
            index, result = future.result()
            video_prompts[index] = result if result else ""
    
    print(f"\n✅ 并行生成完成！", flush=True)
    return video_prompts


# 主函数示例
if __name__ == '__main__':
    # 示例使用
    user_prompt = "女子雙手抓住自己的奶子"
    image_path = '/mnt/nfs/chenlin/model_2.0_lora/benchmarks/pika-sharing/images/example.png'
    
    # 如果图片路径存在
    if os.path.exists(image_path):
        image = Image.open(image_path)
        
        print("="*60)
        print("原始 Prompt:", user_prompt)
        print("="*60)
        
        # 生成 3 个变体 prompts
        variant_prompts = generate_variant_prompts(user_prompt, image)
        
        if variant_prompts:
            print("\n生成的 3 个变体 Prompts:\n")
            for i, prompt in enumerate(variant_prompts, 1):
                print(f"{i}. {prompt}\n")
        else:
            print("❌ 生成失败，请重试")
    else:
        print(f"图片路径不存在: {image_path}")
        print("\n" + "="*60)
        print("📚 使用方法")
        print("="*60)
        print("""
1. 在 Python 脚本中使用:
   
   from image_prompt_generator import generate_variant_prompts
   from PIL import Image
   
   image = Image.open('your_image.jpg')
   prompts = generate_variant_prompts('你的描述', image)
   
   for i, prompt in enumerate(prompts, 1):
       print(f"Prompt {i}: {prompt}")

2. 在集群上运行:
   
   # SSH 登录集群
   ssh -i cluster_id_welly welly@142.202.71.32
   
   # 运行脚本
   cd /mnt/nfs/your_workspace
   python3 image_prompt_generator.py

3. 必需条件:
   - Vertex AI 认证文件: /mnt/nfs/chenlin/dataproc/vertex-ai.json
   - Python 包: vertexai, Pillow
   - 安装命令: pip install google-cloud-aiplatform pillow
        """)

