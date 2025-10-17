from vertexai.generative_models import GenerativeModel, SafetySetting
import vertexai
import os
import random

def clean_text(s: str) -> str:
    if not s:
        return ''
    result = s.strip()
    for a,b in [('\u00a0',' '), ('\xa0',' '), ('\u2013','-'), ('\u2014','-'), ('\u2019',"'"), ('\u201c','"'), ('\u201d','"')]:
        result = result.replace(a,b)
    while '  ' in result:
        result = result.replace('  ', ' ')
    return result

def _init_vertex():
    vertexai.init(
        project="quick-formula-414701",
        location="europe-west4"
    )

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

Generate the enhanced video prompt below:
"""

def generate_video_prompt(image_prompt: str, video_prompt: str, max_retries: int = 3) -> str:
    import re

    # extract flags like --cowgirl
    flags = re.findall(r'\s+(--\w+)', video_prompt or '')
    v_clean = re.sub(r'\s+(--\w+)', '', video_prompt or '').strip()

    _init_vertex()
    safety = [
        SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE),
        SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE),
        SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE),
        SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE),
    ]
    gen_config = {"max_output_tokens": 1024, "temperature": 0.7, "response_mime_type": "text/plain"}

    for _ in range(max_retries):
        try:
            model = GenerativeModel("gemini-2.5-flash")
            txt = model.generate_content(
                VIDEO_PROMPT_TEMPLATE.format(image_prompt=image_prompt, video_prompt=v_clean),
                safety_settings=safety,
                generation_config=gen_config
            ).text
            out = clean_text(txt or '')
            if out:
                if flags:
                    out = out + ' ' + ' '.join(flags)
                return out
        except Exception:
            continue
    # 退化：若生成失敗，僅返回原始視頻描述（不拼接圖片描述）
    fallback = (v_clean or (video_prompt or '')).strip()
    if flags:
        fallback = (fallback + ' ' + ' '.join(flags)).strip()
    return fallback

def generate_video_prompts_for_images(image_prompts: list[str], video_prompt: str, parallel: bool = True) -> list[str]:
    if not image_prompts:
        return []
    if not parallel:
        return [generate_video_prompt(ip, video_prompt) for ip in image_prompts]

    from concurrent.futures import ThreadPoolExecutor
    results = [""] * len(image_prompts)
    def run(idx, ip):
        results[idx] = generate_video_prompt(ip, video_prompt)
    with ThreadPoolExecutor(max_workers=len(image_prompts)) as ex:
        for i, ip in enumerate(image_prompts):
            ex.submit(run, i, ip)
    return results


