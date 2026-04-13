# AI Social Media Automation 🚀

An automated pipeline for generating and publishing high-quality multi-modal AI content to Facebook. This repository uses the latest Google Generative AI models to handle everything from scripting to media creation and posting.

![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![AI Models](https://img.shields.io/badge/AI-Gemini%203%20%7C%20Imagen%204-orange.svg)

## 🤖 AI Stack (2026 Models)
- **Gemini 3.1 Flash Lite:** Handles story scripting, headline generation, and hashtag optimization.
- **Veo 3.1 Fast:** Generates 8-second cinematic 4K vertical videos for Facebook Reels.
- **Imagen 4.0 Fast:** Creates high-fidelity 9:16 vertical images for Facebook Stories and Feed posts.

## 🔄 Automated Workflows

The project features two distinct automation pipelines located in `.github/workflows/`:

### 1. Video Reel Pipeline (`actions-video-gen.yml`)
- **Schedule:** Mondays at 10:00 AM UTC.
- **Output:** A generated 4K Reel and a companion Story teaser.
- **Logic:** Uses Gemini to write a story based on a random category, Veo to render video, and Imagen for the teaser.

### 2. Image Post Pipeline (`actions-image-gen.yml`)
- **Schedule:** 3x a week starting at 11:00 AM UTC.
- **Output:** A high-quality image post with an AI-written caption.
- **Logic:** Optimized for faster daily engagement using Imagen 4.0.

## 🔑 Setup & Configuration

To run these workflows, you must configure the following **GitHub Secrets** in `Settings > Secrets and variables > Actions`:

| Secret Name | Description |
| :--- | :--- |
| `GOOGLE_API_KEY` | Your API key from Google AI Studio. |
| `FB_PAGE_ID` | The numeric ID of your Facebook Business Page. |
| `FB_ACCESS_TOKEN` | A Long-Lived Page Access Token with `page_video_reels` and `publish_video` permissions. |
| `CATEGORIES` | A comma-separated list of topics (e.g., `Space Exploration, Dog Rescues, Deep Sea`). |
| `VIDEO_STORY_PROMPT` | Your prompt template for Gemini (Must include the `{category}` placeholder). |

## 🛠 Project Structure
- `.github/workflows/`: Contains the YAML files that handle the cron scheduling.
- `video-gen.py`: The main Python orchestrator for the Video/Reel pipeline.
- `image-gen.py`: The script dedicated to the daily Image/Feed pipeline.
- `fb_tmp/`: Temporary directory created during runtime to store generated media before upload.

## 🚀 Manual Triggers
Both workflows support `workflow_dispatch`. You can manually trigger a post at any time by going to the **Actions** tab, selecting a workflow, and clicking **Run workflow**.

---
*Maintained by [Emanuel Burgess](https://github.com/EmanuelBurgess)*
