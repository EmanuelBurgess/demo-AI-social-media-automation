import os
import sys
import random
import requests
import pathlib
from google import genai
from google.genai import types

# --- CONFIGURATION ---
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
MODEL_ID = "gemini-2.5-flash-lite"
IMAGE_MODEL_ID = "imagen-4.0-generate-001"

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# --- PROMPT & CATEGORY SETTINGS ---
# You can edit these directly here or keep using Env Vars
custom_categories = os.getenv("CATEGORIES", "Technology, AI, Future, Space")
STORY_PROMPT_TEMPLATE = os.getenv("STORY_PROMPT", "Write an engaging short story about {category}. Use a compelling headline on the first line.")

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
        response = client.models.generate_content(model=MODEL_ID, contents=story_prompt)
        content = response.text
        if not content:
            raise ValueError("Empty response from model.")
    except Exception as e:
        print(f"Story failed: {e}")
        return

    # Extract headline (first line)
    headline = content.split('\n')[0].strip('#* ')
    print(f"Story Generated. Headline used for image: {headline}")

    # 3. Generate Image
    print("Generating Image...")
    image_path = tmp_dir / "post_image.jpg"
    image_generated = False
    
    try:
        img_response = client.models.generate_images(
            model=IMAGE_MODEL_ID,
            prompt=f"Cinematic realistic photo for: {headline}. No words in generated image.",
            config=types.GenerateImagesConfig(number_of_images=1)
        )
        
        if img_response.generated_images:
            # Saving via the image object's save method as per your original logic
            img_response.generated_images[0].image.save(str(image_path))
            image_generated = True
            print("Image generated and verified.")
    except Exception as e:
        print(f"Image generation failed: {e}")
        print("Falling back to text-only mode.")

    # 4. Upload to Facebook
    print("Uploading...")
    
    if image_generated:
        url = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/photos"
        payload = {"caption": content, "access_token": FB_ACCESS_TOKEN}
        with open(image_path, "rb") as img_file:
            files = {"source": img_file}
            fb_res = requests.post(url, data=payload, files=files)
    else:
        url = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/feed"
        payload = {"message": content, "access_token": FB_ACCESS_TOKEN}
        fb_res = requests.post(url, data=payload)

    # 5. Verify
    result = fb_res.json()
    if "id" in result:
        print("SUCCESS! Post is live.")
        print(f"Post ID: {result['id']}")
    else:
        print(f"FB Error: {result}")

if __name__ == "__main__":
    main()
