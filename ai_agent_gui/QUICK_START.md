# Quick Start Guide

Get up and running with the AI Agent GUI in 5 minutes!

## Step 1: Install Python (if not already installed)

1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. During installation, **check "Add to PATH"**
3. Verify installation: Open Command Prompt and type `python --version`

## Step 2: Install Dependencies

1. Open Command Prompt
2. Navigate to the `ai_agent_gui` folder:
   ```batch
   cd path\to\ai_agent_gui
   ```
3. Install required packages:
   ```batch
   pip install -r requirements.txt
   ```

## Step 3: Get Your API Keys

### OpenAI API Key (for Sora 2)
1. Go to [platform.openai.com](https://platform.openai.com/)
2. Create account or log in
3. Go to API Keys → Create new key
4. Copy the key

### Google Gemini API Key
1. Go to [ai.google.dev](https://ai.google.dev/)
2. Click "Get API Key"
3. Copy the key

### YouTube API Setup
1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Create new project
3. Enable "YouTube Data API v3"
4. Create OAuth 2.0 credentials (Desktop app)
5. Download JSON file
6. Rename to `client_secrets.json`
7. Place in `ai_agent_gui` folder

## Step 4: Launch the Application

Double-click `start_ai_agent.bat` or run:
```batch
python main.py
```

## Step 5: Configure Settings

1. Go to the **Settings** tab
2. Paste your API keys
3. Add custom instructions for video generation
4. Click **Save Settings**

## Step 6: Set Your Schedule

1. Go to the **Schedule** tab
2. Check the days you want to upload
3. Set the time for each day
4. Click **Save Schedule**

## Step 7: Test the Workflow

1. Go to the **Dashboard** tab
2. Click **Run Workflow Now**
3. Watch the progress!

## Optional: Enable Auto-Startup

1. Right-click `setup_startup.bat`
2. Select "Run as Administrator"
3. Follow the prompts

---

## Troubleshooting

**Application won't start?**
- Check Python version (must be 3.8+)
- Run: `pip install -r requirements.txt --upgrade`

**API errors?**
- Verify all API keys are correct
- Check internet connection
- Review quota limits for each API

**YouTube upload fails?**
- Delete `token.pickle` and re-authenticate
- Check `client_secrets.json` is valid
- Verify YouTube API is enabled in Google Cloud Console

---

## Need Help?

See the full [README.md](README.md) for detailed documentation.

---

**You're all set! The AI Agent will now automate your video workflow! 🎉**

