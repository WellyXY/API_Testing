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


# Generate 3 variant prompts (concise constraints, no samples/lists)
MULTI_PROMPT_TEMPLATE = """
You are an expert image prompt writer. You will receive ONE reference image.

Objective:
- Produce EXACTLY 3 prompts in Chinese; EACH prompt must contain TWO sentences:
  1) Base visual description of the reference image (concise but detailed, ≈40–80 Chinese characters)
  2) Minimal modification instruction (保持构图不变 + 变更动作/手部/表情/镜头；结尾“同时确保构图一致”)
- Preserve base composition, subject pose, scene and background.
- Make only minimal, plausible changes: hand placement, subtle body posture, facial expression, or camera angle.
- At least ONE prompt MUST change the camera angle (but DO NOT raise the camera), and at least ONE prompt MUST add a clear hand action.

Variation and richness:
- Start EACH prompt by describing the reference image in detail (in Chinese):
  - Character's physical features (hair color, hair length, body state, skin tone)
  - Current pose and position (sitting/standing/riding/lying, etc.)
  - Facial expression and gaze direction
  - Body contact and interaction with any other person
  - Lighting, atmosphere, and mood
- Then add ONE minimal modification sentence (hand/pose/expression/camera) as instruction.
- Prefer dynamic hand actions when plausible and visible (e.g., 抓胸、拨头发、抚摸大腿、将手放在男子胸膛；握住阴茎仅在口交等物理可行情境下)。
- Keep each change minimal but noticeable; avoid introducing new objects or people.
// Camera change constraints (hard rule):
// - DO NOT move the camera upward/top-down/high-angle (禁止俯视/略微俯视/from above)
// - Prefer side view, eye-level, or slightly lower angle (侧面/平视/略微仰视) when changing camera

Physical feasibility:
- First infer the sexual position/activity depicted (e.g., cowgirl, blow job, missionary, doggy).
- Only propose actions that are physically possible for that position.
- If an element is not visible in the image, do not mention it.
- Keep explicitness consistent with the image; do not censor; do not add technical specs.

Style and output format:
- EACH prompt MUST contain TWO Chinese sentences:
  1) Base visual description of the current image (40–80 chars)
  2) Modification instruction in the structure: 「保持画面中人物的动作以及背景不变，……。同时确保构图一致」
- Output ONLY the following, with no explanations and no examples:

[PROMPT 1]
<Chinese base description sentence>
<Chinese modification instruction sentence>

[PROMPT 2]
<Chinese base description sentence>
<Chinese modification instruction sentence>

[PROMPT 3]
<Chinese base description sentence>
<Chinese modification instruction sentence>

Optional user hint (context only, do not copy): {user_prompt}
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
        """从 Gemini 输出中解析出 3 个 prompt（更强健）"""
        raw = (text or '').strip()
        if not raw:
            return []

        def normalize_and_pack(lines):
            # 规整化：去引号、合并“同时确保构图一致”孤行、补句尾
            quote_chars = '「」『』“”"\''
            suffix = '同时确保构图一致'
            result = []
            for token in lines:
                t = (token or '').strip()
                if not t:
                    continue
                # 去首尾引号
                t = t.strip(quote_chars).strip()
                if not t:
                    continue
                # 若是孤立的结尾提示，拼到上一句
                if t == suffix or t.startswith(suffix):
                    if result and suffix not in result[-1]:
                        result[-1] = result[-1].rstrip('。').rstrip('.') + '。' + suffix
                    continue
                # 缺少结尾则补齐
                if suffix not in t:
                    t = t.rstrip('。').rstrip('.') + '。' + suffix
                result.append(t)
            # 只取前三条
            return result[:3]

        # 0) 首選：按 [PROMPT x] 解析兩句式（基礎描述 + 修改指令）
        lines = [l.strip() for l in raw.splitlines()]
        merged = []
        for i in range(1, 4):
            try:
                # 找到 [PROMPT i]
                idx = next(k for k, l in enumerate(lines) if l.upper().startswith(f'[PROMPT {i}]'))
                # 取後續兩個非空行
                base_line = ''
                instr_line = ''
                p = idx + 1
                while p < len(lines) and not base_line:
                    if lines[p] and not lines[p].upper().startswith('[PROMPT'):
                        base_line = lines[p]
                    p += 1
                while p < len(lines) and not instr_line:
                    if lines[p] and not lines[p].upper().startswith('[PROMPT'):
                        instr_line = lines[p]
                    p += 1
                if base_line and instr_line:
                    # 清理並合併為同一條 prompt（兩句）
                    pair = clean_gemini_output(base_line) + ' ' + clean_gemini_output(instr_line)
                    merged.append(pair)
            except StopIteration:
                break
        if len(merged) == 3:
            return merged

        # 0.1) 退化：若沒有 [PROMPT x]，嘗試捕獲成對的兩行（非空連續兩行為一組），取前三組
        pairs = []
        buff = []
        for l in lines:
            if not l:
                continue
            if l.upper().startswith('[PROMPT'):
                continue
            buff.append(l)
            if len(buff) == 2:
                pairs.append(clean_gemini_output(buff[0]) + ' ' + clean_gemini_output(buff[1]))
                buff = []
        if len(pairs) >= 3:
            return pairs[:3]

        # 0.2) 仍不足：抓取“保持…同时确保构图一致”的指令句，作為最小退化方案
        import re
        pattern = r'保持[\s\S]*?同时确保构图一致'
        groups = re.findall(pattern, raw)
        if len(groups) >= 3:
            return normalize_and_pack(groups[:3])

        # 1) 优先解析 [PROMPT x] 结构
        parts = raw.split('[PROMPT ')
        tmp = []
        for i in range(1, 4):
            for part in parts:
                s = part.strip()
                if s.startswith(f'{i}]'):
                    content = s.split(']', 1)[1].strip()
                    if '[PROMPT' in content:
                        content = content.split('[PROMPT')[0].strip()
                    if content:
                        # 去除换行，避免被错误拆分
                        tmp.append(clean_gemini_output(content.replace('\n', ' ')))
                    break
        if len(tmp) == 3:
            return normalize_and_pack(tmp)

        # 2) 解析以数字编号的三行（1. / 2. / 3.）
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        tmp = []
        for line in lines:
            if line[:2].isdigit() or (len(line) > 2 and line[0].isdigit() and line[1] in ['.', '、', ')']):
                # 去掉前缀编号
                if '. ' in line:
                    line = line.split('. ', 1)[1].strip()
                elif '、' in line:
                    line = line.split('、', 1)[1].strip()
                elif ') ' in line:
                    line = line.split(') ', 1)[1].strip()
                tmp.append(clean_gemini_output(line))
        if len(tmp) >= 3:
            return normalize_and_pack(tmp)

        # 3) 如果只有纯文本，尝试按中文句号/换行切分，取前三句
        import re
        sentences = re.split(r'[\n。]+', raw)
        sentences = [s.strip() for s in sentences if s.strip()]
        if len(sentences) >= 3:
            return normalize_and_pack(sentences[:3])

        return []
    
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

