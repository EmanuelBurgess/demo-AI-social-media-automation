# AI-Powered Facebook Content Automator 🚀

An automated pipeline that leverages **Gemini 2.5 Flash-lite** and **Imagen 4.0** to generate high-engagement stories and cinematic visuals, then automatically posts them to a Facebook Page three times a day.

## 🛠 Features
- **Dynamic Content:** Randomly selects from a curated list of categories.
- **AI-Driven Creative:** Uses Gemini for storytelling and Imagen for realistic, high-quality images.
- **Fail-Fast Architecture:** Validates all required secrets and prompt placeholders before execution to save API credits.
- **Fully Automated:** Runs via GitHub Actions on a 3x daily schedule (00:00, 08:00, 16:00 UTC).
- **No-Code Configuration:** Update prompts and categories directly via GitHub Secrets without touching code.

## 📋 Prerequisites
To run this automation, you will need:
1. **Google AI SDK Key:** From [Google AI Studio](https://aistudio.google.com/).
2. **Facebook Page ID & Access Token:** Generated via a Meta App with `page_manage_posts` and `pages_read_engagement` permissions.
3. **GitHub Repository:** To host the code and Actions.

## 🔐 GitHub Secrets Configuration
Navigate to **Settings > Secrets and variables > Actions** and add the following:

| Secret Name | Description | Example Format |
| :--- | :--- | :--- |
| `FB_PAGE_ID` | Your Facebook Page unique ID. | `1234567890` |
| `FB_ACCESS_TOKEN` | A Long-Lived Page Access Token. | `EAAB...` |
| `GOOGLE_API_KEY` | Your Gemini API Key. | `AIza...` |
| `CATEGORIES` | Comma-separated topics for the AI. | `Deep Sea, Space, Cold Cases` |
| `STORY_PROMPT` | The instruction for the AI (Must include `{category}`). | `Write a story about {category}...` |

> **Note:** Your `STORY_PROMPT` **must** include the placeholder `{category}` so the script can inject the randomly selected topic.

## 🚀 Deployment
1. Clone this repository.
2. Ensure your Python script is named `main.py`.
3. Push the `.github/workflows/facebook_poster.yml` file to your main branch.
4. Manually trigger the first run via the **Actions** tab to verify the connection.

## 📁 File Structure
- `main.py`: The Python execution engine.
- `.github/workflows/facebook_poster.yml`: The GitHub Actions schedule configuration.
- `requirements.txt`: (Optional) Lists `requests` and `google-genai`.

## ⚖️ License
MIT
