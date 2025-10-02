import os
import time
import uuid
import json
import aiohttp
import asyncio
from fastapi import HTTPException

# Environment variables (replace with actual values or set via os.environ)
MINIMAX_GROUPID = os.getenv("MINIMAX_GROUPID", "your_group_id_here")
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "your_api_key_here")

AUDIO_OUTPUT_DIR = "./output_audio"
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

async def minimax_text_to_speech(voice_id: str, text: str) -> str:
    url = f"https://api.minimax.io/v1/t2a_v2?GroupId={MINIMAX_GROUPID}"
    payload = {
        "model": "speech-02-turbo",
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": 1,
            "vol": 1,
            "pitch": 0,
            "english_normalization": True
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1
        },
        "language_boost": "auto",
    }
    headers = {
        'Authorization': f'Bearer {MINIMAX_API_KEY}',
        'Content-Type': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status != 200:
                raise HTTPException(status_code=500, detail=f"TTS failed: {await response.text()}")
            parsed_json = await response.json()
    audio_value = bytes.fromhex(parsed_json['data']['audio'])
    filename = f"{voice_id}-{uuid.uuid4().hex}.mp3"
    output_path = os.path.join(AUDIO_OUTPUT_DIR, filename)
    with open(output_path, "wb") as f:
        f.write(audio_value)
    return output_path

async def minimax_clone_voice(userId: str, cnt: int, audio_path: str) -> tuple[str, str]:
    upload_url = f'https://api.minimax.io/v1/files/upload?GroupId={MINIMAX_GROUPID}'
    headers1 = {
        'Authorization': f'Bearer {MINIMAX_API_KEY}'
    }
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    form_data = aiohttp.FormData()
    form_data.add_field('purpose', 'voice_clone')
    form_data.add_field('file', audio_bytes, filename='audio.mp3', content_type='audio/mpeg')
    async with aiohttp.ClientSession() as session:
        async with session.post(upload_url, headers=headers1, data=form_data) as response:
            if response.status != 200:
                raise HTTPException(status_code=500, detail=f"Upload failed: {await response.text()}")
            upload_response = await response.json()
            file_id = upload_response["file"]["file_id"]
        clone_url = f'https://api.minimax.io/v1/voice_clone?GroupId={MINIMAX_GROUPID}'
        voice_id = f"nova-{userId}-{cnt}"
        payload = {
            "file_id": file_id,
            "voice_id": voice_id
        }
        headers2 = {
            'authorization': f'Bearer {MINIMAX_API_KEY}',
            'content-type': 'application/json'
        }
        async with session.post(clone_url, headers=headers2, json=payload) as response:
            if response.status != 200:
                raise HTTPException(status_code=500, detail=f"Clone failed: {await response.text()}")
    previewUrl = await minimax_text_to_speech(voice_id, "Hi, this is a preview of your cloned voice.")
    return voice_id, previewUrl

async def main():
    folder = "./voice_presets"
    userId = "7beafbcf-0174-451c-9f38-0d84e43a3c9c"
    files = sorted([f for f in os.listdir(folder) if f.endswith(".mp3")])
    voices = []
    for i, file in enumerate(files):
        try:
            audio_path = os.path.join(folder, file)
            voice_id, previewUrl = await minimax_clone_voice(userId, i, audio_path)
            voice = {
                "id": voice_id,
                "userId": userId,
                "name": os.path.splitext(file)[0],
                "previewUrl": previewUrl,
                "type": 1,
                "platform": "minimax",
                "createdAt": int(time.time() * 1000),
            }
            voices.append(voice)
        except Exception as e:
            print(f"Failed to clone voice for {file}: {e}")
    with open("cloned_voices_output.json", "w") as f:
        json.dump(voices, f, indent=2)
    return voices

if __name__ == "__main__":
    asyncio.run(main())
