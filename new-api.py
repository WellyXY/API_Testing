import requests
import json
import time

# Global variables
token = "4NmMivD10QqvN9xGur86bLu4xY5FOn0r_QlH_zGZQOk"
# token = "pk_DNAWZiA_nU-BRvMGw-Hcn4upZHIg2H2zcpoYPm0WlaA"
# # token_limited = "Y0XJXmoXRbwU44brvdl0NY8FE9-agxXzz-zEs910HF8"
api_url = "https://devapi.pika.art"

# api_url = "https://089e99349ace.pikalabs.app"
# api_url = "https://cool-firefly-84db.saarang.workers.dev"
# token = "GcqHI4K2ACWuRQw-eWF4c4RyDcLoADeysiym4iBj76o"
# token = 'pk_3028gOKTkqetJEb6RhkYbZFA1yZuC9OWHwiVD6n-EWg'   # expired
# token = "pk_UgMM9o42Cy0DoaEPPY9e3xZrKm6jFvAP7o9ZmQ2kWhQ"

def get_video_status(video_id):
    url = f"{api_url}/videos/{video_id}"
    headers = {
        "X-API-KEY": f"{token}",
        "Accept": "application/json"
    }
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            status = data.get("status")
            if status == "finished":
                print("Video processing is complete.")
                return data
            else:
                print(f"Current status: {status}. Checking again in 15 seconds...")
                print(data)
                if status == "failed":
                    print("Job failed")
                    return None
        else:
            print(f"Failed to retrieve video status. HTTP Status Code: {response.status_code}")
            break

        time.sleep(15)  # Wait for 15 seconds before the next check

def generate_pikadditions(video_path, image_path, prompt_text, seed=None, negative_prompt=None):
    url = f"{api_url}/generate/pikadditions"
    payload = {
        "promptText": prompt_text,
        "negativePrompt": negative_prompt,
        "seed": seed
    }
    headers = {
        "X-API-KEY": f"{token}",
        "Accept": "application/json"
    }
    files = {
        "video": (video_path[0], open(video_path[0], "rb"), video_path[1]),
        "image": (image_path[0], open(image_path[0], "rb"), image_path[1])
    }
    response = requests.post(url, data=payload, headers=headers, files=files)
    return response.json()

def generate_turbo_t2v(prompt_text, seed=None, negative_prompt=None):
    url = f"{api_url}/generate/turbo/t2v"
    payload = {
        "promptText": prompt_text,
        "negativePrompt": negative_prompt,
        "seed": seed
    }
    headers = {
        "X-API-KEY": f"{token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    response = requests.post(url, data=payload, headers=headers)
    return response.json()

def generate_turbo_i2v(image_path, prompt_text=None, seed=None, negative_prompt=None):
    url = f"{api_url}/generate/turbo/i2v"
    payload = {
        "promptText": prompt_text,
        "negativePrompt": negative_prompt,
        "seed": seed
    }
    headers = {
        "X-API-KEY": f"{token}",
        "Accept": "application/json"
    }
    files = {
        "image": (image_path[0], open(image_path[0], "rb"), image_path[1])
    }
    response = requests.post(url, data=payload, headers=headers, files=files)
    print("Requests response:", response)
    return response.json()

def generate_turbo_c2v(image_paths, prompt_text=None, seed = None, ingredients_mode="precise", negative_prompt=None):
    url = f"{api_url}/generate/turbo/pikascenes"
    payload = {
        "ingredientsMode": ingredients_mode,
        "promptText": prompt_text,
        "negativePrompt": negative_prompt,
        "seed": seed
    }
    headers = {
        "X-API-KEY": f"{token}",
        "Accept": "application/json"
    }
    files = [("images", (image_path[0], open(image_path[0], "rb"), image_path[1])) for image_path in image_paths]
    response = requests.post(url, data=payload, headers=headers, files=files)
    print("Requests response:", response)
    return response.json()


def generate_t2v(prompt_text, seed=None, negative_prompt=None):
    url = f"{api_url}/generate/2.2/t2v"
    payload = {
        "promptText": prompt_text,
        "negativePrompt": negative_prompt,
        "seed": seed
    }
    headers = {
        "X-API-KEY": f"{token}",
        "Accept": "application/json"
    }
    response = requests.post(url, data=payload, headers=headers)
    print("query", response, url)
    return response.json()

def generate_i2v(image_path, prompt_text=None, seed=None, negative_prompt=None):
    url = f"{api_url}/generate/2.2/i2v"
    payload = {
        "promptText": prompt_text,
        "negativePrompt": negative_prompt,
        "seed": seed
    }
    headers = {
        "X-API-KEY": f"{token}",
        "Accept": "application/json"
    }
    files = {
        "image": (image_path[0], open(image_path[0], "rb"), image_path[1])
    }
    response = requests.post(url, data=payload, headers=headers, files=files)
    print("Requests response:", response)
    return response.json()

def generate_c2v(image_paths, prompt_text=None, seed = None, ingredients_mode="precise", negative_prompt=None):
    url = f"{api_url}/generate/2.2/pikascenes"
    payload = {
        "ingredientsMode": ingredients_mode,
        "promptText": prompt_text,
        "negativePrompt": negative_prompt,
        "seed": seed
    }
    headers = {
        "X-API-KEY": f"{token}",
        "Accept": "application/json"
    }
    files = [("images", (image_path[0], open(image_path[0], "rb"), image_path[1])) for image_path in image_paths]
    response = requests.post(url, data=payload, headers=headers, files=files)
    print("Requests response:", response)
    return response.json()

def test_t2v():
    image_path = ("man.jpg", 'image/jpg')
    prompt = "An old man flying in the sky with superpowers."
    seed = 245632

    response = generate_turbo_t2v(prompt, seed)
    # response = generate_t2v(prompt, seed)

    print(response)

    vidID = response["video_id"]

    data = get_video_status(vidID)

    print(data)

def test_c2v():
    image_paths = [("man.jpg", 'image/jpg'), ("tomato.jpeg", 'image/jpeg'), ("knife.jpeg", 'image/jpeg')]
    prompt = "The man in the image cuts a tomato with the knife in the image while his wife watches behind him."
    seed = 3

    response = generate_turbo_c2v(image_paths, prompt, seed)
    # response = generate_c2v(image_paths, prompt, seed)

    print(response)

    vidID = response["video_id"]

    data = get_video_status(vidID)

    print(data)

def test_i2v():
    image_path = ("lincoln.jpg", 'image/jpg')
    prompt = "The man in the image is dancing in a graceful way."
    seed = 245632

    response = generate_turbo_i2v(image_path, prompt, seed)
    # response = generate_i2v(image_path, prompt, seed)

    print(response)

    vidID = response["video_id"]

    data = get_video_status(vidID)

    print(data)

def generate_pikadditions(video_path, image_path=None, prompt_text=None, negative_prompt=None, seed=None):
    url = f"{api_url}/generate/pikatwists"
    payload = {
        "promptText": prompt_text,
        "negativePrompt": negative_prompt,
        "seed": seed,
        # "model": "Turbo"
    }
    headers = {
        "X-API-KEY": f"{token}",
        "Accept": "multipart/form-data"
    }
    
    files = [("video", (video_path[0], open(video_path[0], "rb"), video_path[1]))]
    if image_path:
        files.append(("image", (image_path[0], open(image_path[0], "rb"), image_path[1])))
    response = requests.post(url, data=payload, headers=headers, files=files)
    print(response.json())
    return response.json()

def test_pikadditions():
    video_path = ("vid.mp4", "video/mp4")
    image_path = ("man.jpg", "image/jpg")
    prompt = "the person dancing turns into lego"
    seed = 12345
    roi = "The person dancing in red clothes"

    response = generate_pikadditions(video_path, image_path=None, prompt_text=prompt, negative_prompt="blurry, low quality", seed=seed)
    print(response)

    vid_id = response["video_id"]
    data = get_video_status(vid_id)
    print(data)

def generate_pikaswaps(video_path, image_path=None, prompt_text=None, negative_prompt=None, seed=None, modify_region_roi=None):
    url = f"{api_url}/generate/pikaswaps"
    payload = {
        "promptText": prompt_text,
        "negativePrompt": negative_prompt,
        "seed": seed,
        "modifyRegionRoi": modify_region_roi,
        "model": "Pro"
    }
    headers = {
        "X-API-KEY": f"{token}",
        "Accept": "application/json"
    }
    
    files = [("video", (video_path[0], open(video_path[0], "rb"), video_path[1]))]
    if image_path:
        files.append(("image", (image_path[0], open(image_path[0], "rb"), image_path[1])))
    
    response = requests.post(url, data=payload, headers=headers, files=files)
    print("Request response:", response)
    return response.json()

def test_pikaswaps():
    video_path = ("vid.mp4", "video/mp4")
    image_path = ("man.jpg", "image/jpg")
    prompt = "Replace the person in the video with a monster dancing"
    seed = 12345
    roi = "The person dancing in red clothes"

    response = generate_pikaswaps(video_path, image_path, prompt, "blurry, low quality", seed, roi)
    print(response)

    vid_id = response["video_id"]
    data = get_video_status(vid_id)
    print(data)

def generate_pikaframes(keyframe_paths, prompt_text, duration=5, resolution="1080p", seed=None, negative_prompt=None):
    endpoint = f"{api_url}/generate/2.2/pikaframes"
    
    payload = {
        "promptText": prompt_text,
        "negativePrompt": negative_prompt,
        "seed": seed,
        "duration": duration,
        "resolution": resolution
    }
    
    headers = {
        "X-API-KEY": token,
        # "Accept": "application/json"
    }
    
    # Open files directly rather than using list comprehension
    files = []
    for frame_path in keyframe_paths:
        files.append(("keyFrames", (frame_path[0], open(frame_path[0], "rb"), frame_path[1])))
    
    try:
        response = requests.post(endpoint, data=payload, headers=headers, files=files)
        response.raise_for_status()  # This will raise an exception for 4XX/5XX responses
        print(response)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error in API call: {e}")
        print(f"Response content: {response.text}")
        return {"error": str(e)}
    finally:
        # Close file handles
        for _, file_tuple, *_ in files:
            file_tuple[1].close()

def test_pikaframes():
    keyframe_paths = [("man.jpg", "image/jpg"), ("lincoln.jpg", "image/jpg")]
    prompt = "" # "The tomato morphs into a sharp knife with dramatic lighting"
    duration = 3
    seed = 12345

    response = generate_pikaframes(keyframe_paths, prompt, duration, "1080p", seed, "blurry, low quality")
    print(response)

    vid_id = response["video_id"]
    data = get_video_status(vid_id)
    print(data)

def generate_multiframe(keyframe_paths: list[tuple[str, str]],
                        transition_prompts: list[str],
                        frame_durations: list[int],
                        resolution: str = "1080p",
                        loop: bool = False,
                        negative_prompt: str | None = None,
                        seed: int | None = None):
    """
    Generates a video using the /generate/2.2/multiframe endpoint.

    Args:
        keyframe_paths: List of tuples, each containing (filepath, content_type).
                        e.g., [("frame1.png", "image/png"), ("frame2.jpg", "image/jpeg")]
        transition_prompts: List of prompts for each transition.
        frame_durations: List of durations (seconds) for each transition.
        resolution: Output resolution ('720p' or '1080p').
        loop: Whether the video should loop.
        negative_prompt: Optional negative prompt.
        seed: Optional seed for generation.

    Returns:
        Dictionary with the API response or error details.
    """
    endpoint = f"{api_url}/generate/2.2/multiframe"

    # --- Prepare Payload (Data Fields) ---
    data_payload = {
        "resolution": resolution,
        "loop": str(loop).lower(), # API expects 'true'/'false'
        "transitionPrompts": transition_prompts,
        "frameDurations": frame_durations,
    }
    # Add optional fields if they are provided
    if negative_prompt:
        data_payload["negativePrompt"] = negative_prompt
    if seed is not None:
        data_payload["seed"] = seed

    # --- Prepare Headers ---
    headers = {
        "X-API-KEY": token, # Use the globally defined token
        "Accept": "application/json" # Expect JSON response
    }

    # --- Prepare Files ---
    files_to_upload = []
    file_handles = []
    try:
        for frame_path, content_type in keyframe_paths:
             if not os.path.exists(frame_path):
                 print(f"Error: Keyframe file not found at {frame_path}")
                 return {"error": f"File not found: {frame_path}"}

             file_handle = open(frame_path, "rb")
             file_handles.append(file_handle)
             # Structure for requests: ('form_field_name', (filename, file_object, content_type))
             files_to_upload.append(("keyFrames", (os.path.basename(frame_path), file_handle, content_type)))

        # --- Make API Call ---
        print(f"Calling: {endpoint}")
        print(f"Data: {data_payload}")
        # print(f"Files: {[f[1][0] for f in files_to_upload]}") # Uncomment to verify filenames

        response = requests.post(endpoint, data=data_payload, headers=headers, files=files_to_upload)

        # --- Process Response ---
        print(f"Status Code: {response.status_code}")
        # Always try to print the raw text for debugging, especially on errors
        print(f"Response Text: {response.text}")

        if response.ok: # Checks if status code is < 400
            return response.json()
        else:
            # Try to parse JSON error detail, otherwise use text
            error_details = response.text
            try:
                error_details = response.json()
            except requests.exceptions.JSONDecodeError:
                pass
            print(f"API Error: {response.status_code}")
            return {"error": f"API Error {response.status_code}", "details": error_details}

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        traceback.print_exc()
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return {"error": f"An unexpected error occurred: {str(e)}"}
    finally:
        # --- Cleanup: Close Files ---
        for handle in file_handles:
            if handle and not handle.closed:
                handle.close()

import os

def test_multiframe():
    """Tests the multiframe generation endpoint."""
    # Define inputs for the multiframe API
    keyframe_paths = [("man.jpg", "image/jpg")] #, ("lincoln.jpg", "image/jpg")] #,  
                      # ("man.jpg", "image/jpg"), ("lincoln.jpg", "image/jpg")]
    transition_prompts_input = [""] # , "", "", ""]
    frame_durations_input = [10] # 5 seconds for the transition
    seed_input = 54321
    negative_prompt_input = "ugly, deformed, blurry"
    resolution_input = "1080p"
    loop_input = True

    # Make sure the keyframe files exist before calling
    for path, _ in keyframe_paths:
        if not os.path.exists(path):
            print(f"ERROR: Test cannot run. Keyframe file missing: {path}")
            return

    print("--- Starting Multiframe Test ---")
    response = generate_multiframe(
        keyframe_paths=keyframe_paths,
        transition_prompts=transition_prompts_input,
        frame_durations=frame_durations_input,
        resolution=resolution_input,
        loop=loop_input,
        negative_prompt=negative_prompt_input,
        seed=seed_input
    )

    print("\n--- Generation Request Response ---")
    print(response)

    vid_id = response["video_id"]
    res = get_video_status(vid_id)
    print(res)


# test_t2v()
test_i2v()
# test_c2v()
# test_pikadditions()
# test_pikaframes()
# test_multiframe()
# test_pikaswaps()

i2v_2p2_ID = 'eb8e3970-d2bd-4a15-8a2e-c694d84776f9'
t2v_2p2_ID = '0f7ee4a2-e8c1-49d2-b7b2-d25cb150ab1d'
t2v_2p2_10s = '6f431226-104d-4a9f-b250-5cf0fa1b34b4'
c2v_2p2_10s = '08ce7ab3-097f-424c-938f-efbaec1eca4c'
keyframe_2p2_3s = '04fc5786-f526-49f7-8507-3147936224f4'

pikaffect_crumble = 'edea077d-52c1-4a84-94ce-cb5b10474647'
pikaffect_propose = 'e642670e-a903-4503-976b-38c9cdd5a6fa'

# pikaswaps = '4afbe5e4-7081-4825-ab00-eeb207d4c24b' 
pikaswaps_prod_img = '93124cec-a464-46c5-ad7f-e66d035efa0b'
pikaswaps = 'df1c4be1-1e1f-43f3-af7c-7cf5662ae1e4'

pikaframes = 'b321315e-47be-45ad-b67b-594116b8ed1f'
pikatwists = 'ceb6954f-fa50-4c51-88a9-c75dd0d93196'

ID = pikatwists
# print(get_video_status(ID))

# test_pikaframes()

# print(generate_turbo_t2v("video of two monkeys dancing in new york city"))

#print(get_video_status(ID))

