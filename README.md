# AI-Powered Social Media Automation (2026 Edition) 🚀

An advanced, production-ready Python automation engine that researches, writes, renders, and publishes high-fidelity **Facebook Stories** and **Posts** using the **Gemini 3** ecosystem and Facebook Graph API v20.0.

![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![AI Models](https://img.shields.io/badge/AI-Gemini%203%20%7C%20Imagen%204-orange.svg)

## ✨ Features
* **Multimodal AI Pipeline**:
    * **Scripting**: Powered by `gemini-3-flash` for high-retention engagement hooks and long-form storytelling.
    * **Visuals**: High-resolution cinematic images via `imagen-4.0-generate-001`.
* **Dynamic Content Injection**: Decoupled prompt and category variables for instant strategy adjustments without code commits.
* **GitHub Actions Integration**: Fully automated 3x daily posting schedule (00:00, 08:00, 16:00 UTC).
* **Fail-Fast Architecture**: Pre-execution validation of API keys, environment secrets, and prompt placeholders to ensure 100% pipeline reliability.
* **No-Code Strategy**: Manage your entire content calendar (topics and AI instructions) directly through GitHub Secrets.

## 🛠️ Tech Stack
* **Language**: Python 3.14+
* **AI SDK**: `google-genai` (Official 2026 Release)
* **API**: Facebook Graph API v20.0
* **Automation**: GitHub Actions

## 🚀 Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/EmanuelBurgess/demo-AI-social-media-automation.git](https://github.com/EmanuelBurgess/demo-AI-social-media-automation.git)
    cd demo-AI-social-media-automation
    ```

2.  **Configure GitHub Secrets**:
    To enable the automated pipeline, navigate to **Settings > Secrets and variables > Actions** and add:

    | Secret Name | Description |
    | :--- | :--- |
    | `FB_PAGE_ID` | Your Facebook Page unique ID. |
    | `FB_ACCESS_TOKEN` | Long-lived Page Access Token. |
    | `GOOGLE_API_KEY` | Gemini API Key from Google AI Studio. |
    | `CATEGORIES` | Comma-separated topics (e.g., `Space exploration, Deep sea, Future Tech`). |
    | `STORY_PROMPT` | The AI instruction (Must include `{category}` placeholder). |

## 📋 Usage

### Automated (Scheduled)
The system is pre-configured to run three times daily via the `.github/workflows/facebook_poster.yml` file.

### Manual Trigger
You can force a post immediately via the GitHub UI:
1.  Navigate to the **Actions** tab.
2.  Select **Scheduled Facebook Post**.
3.  Click **Run workflow**.

### Local Development
If running locally, ensure your environment variables are exported in your shell, then run:
```bash
python3 main.py
