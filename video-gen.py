import os
import sys
import time
import random
import requests
import pathlib
from google import genai
from google.genai import types

# --- CONFIGURATION ---
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
STORY_MODEL = "gemini-3.1-flash-lite-preview"
VIDEO_MODEL = "veo-3.1-fast-generate-preview" 
IMAGE_MODEL = "imagen-4.0-fast-generate-001" 

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# --- 1. CONTENT GENERATION STEP ---
def generate_script(category):
    print(f"Step 1: Generating script for {category}...")
    template = os.getenv("VIDEO_STORY_PROMPT", "Write a story about {category}")
    prompt = template.format(category=category)
    
    response = client.models.generate_content(model=STORY_MODEL, contents=prompt)
    text = response.text.replace("*", "").strip()
    headline = text.split('\n')[0].strip()
    return text, headline

# --- 2. VIDEO GENERATION STEP ---
def generate_video(headline, output_path):
    print(f"Step 2: Rendering video via {VIDEO_MODEL}...")
    operation = client.models.generate_videos(
        model=VIDEO_MODEL,
        prompt=f"Cinematic vertical 9:16 video: {headline}. Realistic, 4k, no text.",
        config=types.GenerateVideosConfig(aspect_ratio="9:16", duration_seconds=8.0)
    )
    
    while not operation.done:
        print("   ...processing video...")
        time.sleep(20)
        operation = client.operations.get(operation)

    generated_video = operation.response.generated_videos[0]
    client.files.download(file=generated_video.video)
    generated_video.video.save(str(output_path))
    return output_path

# --- 3. IMAGE GENERATION STEP ---
def generate_image(headline, output_path):
    print(f"Step 3: Creating teaser image via {IMAGE_MODEL}...")
    img_response = client.models.generate_images(
        model=IMAGE_MODEL,
        prompt=f"Cinematic 9:16 vertical poster: {headline}. No text.",
        config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio="9:16")
    )
    img_response.generated_images[0].image.save(str(output_path))
    return output_path

# --- 4. PUBLISHING STEP ---
def publish_to_facebook(content, headline, video_path, image_path=None):
    print("Step 4: Uploading to Facebook Graph API...")
    
    # Upload Reel
    init_url = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/video_reels"
    init_res = requests.post(init_url, params={"access_token": FB_ACCESS_TOKEN}, data={"upload_phase": "start"}).json()
    video_id = init_res.get("video_id")

    headers = {"Authorization": f"OAuth {FB_ACCESS_TOKEN}", "Content-Type": "application/octet-stream"}
    with open(video_path, "rb") as f:
        requests.post(f"https://rupload.facebook.com/video-upload/v20.0/{video_id}", data=f, headers=headers)

    requests.post(init_url, params={"access_token": FB_ACCESS_TOKEN}, data={
        "upload_phase": "finish", "video_id": video_id, "video_state": "PUBLISHED", "description": content
    })
    
    # Upload Story (Teaser)
    if image_path:
        story_url = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/photos"
        with open(image_path, "rb") as img_file:
            requests.post(story_url, data={
                "message": f"NEW REEL: {headline} 🚀",
                "access_token": FB_ACCESS_TOKEN,
                "is_published": "true"
            }, files={"source": img_file})

# --- MAIN ORCHESTRATOR ---
def main():
    # Setup
    tmp_dir = pathlib.Path("./fb_tmp")
    tmp_dir.mkdir(exist_ok=True)
    
    cats = os.getenv("CATEGORIES", "Space,Tech").split(",")
    category = random.choice(cats).strip()

    try:
        # Execute Steps
        full_text, headline = generate_script(category)
        
        video_file = generate_video(headline, tmp_dir / "reel.mp4")
        
        # Optional Image (Wrapped in its own try/except so it doesn't kill the Reel)
        try:
            image_file = generate_image(headline, tmp_dir / "teaser.jpg")
        except Exception as e:
            print(f"Image Step Failed: {e}")
            image_file = None

        publish_to_facebook(full_text, headline, video_file, image_file)
        print("✅ SUCCESSFULLY POSTED!")

    except Exception as e:
        print(f"PIPELINE CRITICAL ERROR: {e}")

if __name__ == "__main__":
    main()
