import os
import sys
import time
import random
import requests
import pathlib
from google import genai
from google.genai import types

#CONFIGURATION
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
STORY_MODEL = "gemini-3.1-flash-lite-preview"
VIDEO_MODEL = "veo-3.1-fast-generate-preview" 
IMAGE_MODEL = "imagen-4.0-fast-generate-001" 

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# --- PROMPT & CATEGORY SETTINGS ---
# You can edit these directly here or keep using Env Vars
custom_categories = os.getenv("CATEGORIES")
STORY_PROMPT_TEMPLATE = os.getenv("VIDEO_STORY_PROMPT")

# 1. FAIL FAST: Process Categories
if not custom_categories or custom_categories.strip() == "":
    print("ERROR: No categories provided. Pipeline failing.")
    sys.exit(1)

CATEGORIES = [c.strip() for c in custom_categories.split(",") if c.strip()]

def main():
    # 1. Setup workspace
    tmp_dir = pathlib.Path("./fb_tmp")
    tmp_dir.mkdir(exist_ok=True)
    
    category = random.choice(CATEGORIES)
    print(f"Category: {category}")

    # 2. Generate Story
    print("Generating Story...")
    story_prompt = STORY_PROMPT_TEMPLATE.format(category=category)
    
    try:
        response = client.models.generate_content(model=STORY_MODEL, contents=story_prompt)
        content = response.text.replace("*", "").strip()
        headline = content.split('\n')[0].strip()
        print(f"Content Generated: {headline}")
    except Exception as e:
        print(f"Content failed: {e}")
        return

    # 2. Generate Reel Video
    print("🎬 Starting Video Generation (Veo 3.1)...")
    video_path = tmp_dir / "reel_video.mp4"
    try:
        operation = client.models.generate_videos(
            model=VIDEO_MODEL,
            prompt=f"Cinematic vertical 9:16 video of: {headline}. Realistic, 4k, dramatic lighting. text free.",
            config=types.GenerateVideosConfig(aspect_ratio="9:16", duration_seconds=8.0)
        )
        while not operation.done:
            print("   ...rendering video...")
            time.sleep(20)
            operation = client.operations.get(operation)

        generated_video = operation.response.generated_videos[0]
        client.files.download(file=generated_video.video)
        generated_video.video.save(str(video_path))
        print(f"Video Saved: {video_path.name}")
    except Exception as e:
        print(f"Video Generation failed: {e}")
        return

    # 3. Generate Story Image (Teaser)
    print("Generating Story Teaser Image (Imagen 4.0)...")
    image_path = tmp_dir / "story_teaser.jpg"
    try:
        img_response = client.models.generate_images(
            model=IMAGE_MODEL,
            prompt=f"Cinematic 9:16 vertical poster for a story about: {headline}. Hyper-realistic, dramatic, text-free.",
            config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio="9:16")
        )
        img_response.generated_images[0].image.save(str(image_path))
        print("Story Image Saved.")
    except Exception as e:
        print(f"Image failed: {e}")
        image_path = None

    # 4. Upload Reel
    print("📤 Uploading Reel...")
    try:
        init_url = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/video_reels"
        init_res = requests.post(init_url, params={"access_token": FB_ACCESS_TOKEN}, data={"upload_phase": "start"}).json()
        video_id = init_res.get("video_id")

        headers = {"Authorization": f"OAuth {FB_ACCESS_TOKEN}", "offset": "0", "file_size": str(video_path.stat().st_size), "Content-Type": "application/octet-stream"}
        with open(video_path, "rb") as f:
            requests.post(f"https://rupload.facebook.com/video-upload/v20.0/{video_id}", data=f, headers=headers)

        requests.post(init_url, params={"access_token": FB_ACCESS_TOKEN}, data={"upload_phase": "finish", "video_id": video_id, "video_state": "PUBLISHED", "description": content})
        print(f"SUCCESS! Reel is live (ID: {video_id}).")
    except Exception as e:
        print(f"Reel Upload failed: {e}")

    # 5. Upload Facebook Story
    if image_path:
        print("📸 Posting to Facebook Stories...")
        try:
            story_url = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/photos"
            with open(image_path, "rb") as img_file:
                # Posting to stories requires 'target_id' or 'is_story=true' depending on your API version
                # Usually, posting to /photos with is_published=false then attaching to stories works best
                files = {"source": img_file}
                payload = {
                    "message": f"NEW REEL: {headline} 🚀 Check it out on our feed!",
                    "access_token": FB_ACCESS_TOKEN,
                    "is_published": "true" # In v20.0, published photos on pages appear in the story tray if configured
                }
                requests.post(story_url, data=payload, files=files)
            print("SUCCESS! Related Story is live.")
        except Exception as e:
            print(f"Story Upload failed: {e}")

if __name__ == "__main__":
    main()
