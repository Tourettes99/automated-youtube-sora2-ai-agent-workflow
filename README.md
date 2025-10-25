# AI Agent GUI - Automated Sora Video to YouTube Workflow

A comprehensive Python GUI application that automates the complete workflow of generating videos with OpenAI's Sora 2, removing watermarks, and uploading to YouTube on a custom schedule.

## Features

### 🤖 AI-Powered Workflow
- **Gemini 2.5 Flash Integration**: Uses Google's Gemini AI as an intelligent agent to plan and optimize the workflow
- **Sora 2 Video Generation**: Automatically generates high-quality videos using OpenAI's Sora model
- **Intelligent Metadata**: AI generates SEO-optimized titles, descriptions, and tags for YouTube

### 🎥 Video Processing
- **KLing Watermark Removal**: Integrates the KLing watermark remover from your codebase
- **Video Enhancement**: Automatically enhances video quality after watermark removal
- **Multiple Fallback Options**: FFmpeg fallback if KLing tool is unavailable

### 📅 Smart Scheduling
- **Custom Weekly Schedule**: Set specific days and times for automatic uploads
- **Date Tracking**: Prevents duplicate uploads on the same day
- **Background Execution**: Runs silently in the background, checking schedule automatically

### 📊 User Interface
- **Intuitive GUI**: Clean, modern interface built with tkinter
- **Visual Progress Tracking**: Real-time visualization of workflow progress
- **Settings Management**: Easy configuration of all API keys and preferences
- **Comprehensive Logs**: Detailed logging with viewing interface

### ⚙️ Configuration
- **API Management**: Securely store OpenAI, Gemini, and YouTube API credentials
- **Custom AI Instructions**: Define custom guidelines for video generation
- **Video Settings**: Configure resolution, duration, and quality preferences
- **Privacy Controls**: Set video privacy status (public, unlisted, private)

### 🚀 Automation
- **Windows Startup**: Batch script for automatic launch at system startup
- **Hands-Free Operation**: Fully automated workflow once configured
- **Error Handling**: Robust error handling with detailed logging

---

## Installation

### Prerequisites

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Ensure "Add to PATH" is checked during installation

2. **FFmpeg** (recommended for video processing)
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Add to system PATH

### Setup Steps

1. **Clone or Download** this repository to your computer

2. **Install Dependencies**
   ```batch
   cd ai_agent_gui
   pip install -r requirements.txt
   ```

3. **Configure API Keys** (see Configuration section below)

4. **Run the Application**
   ```batch
   python main.py
   ```
   Or double-click `start_ai_agent.bat`

---

## Configuration

### 1. OpenAI API Key (for Sora 2)

1. Go to [platform.openai.com](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and paste it in the **Settings** tab of the application

**Note**: Sora API access may require waitlist approval from OpenAI.

### 2. Google Gemini API Key

1. Go to [ai.google.dev](https://ai.google.dev/)
2. Sign in with your Google account
3. Click "Get API Key"
4. Create a new API key
5. Copy the key and paste it in the **Settings** tab

### 3. YouTube API Setup

This is a multi-step process:

#### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the **YouTube Data API v3**

#### Step 2: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. Choose **Desktop app** as application type
4. Download the JSON file
5. Rename it to `client_secrets.json`
6. Place it in the `ai_agent_gui` directory

#### Step 3: Configure OAuth Consent Screen

1. Go to **OAuth consent screen**
2. Add your email as a test user
3. Add the following scope: `https://www.googleapis.com/auth/youtube.upload`

#### Step 4: First Time Authentication

1. When you first run the workflow, a browser window will open
2. Sign in with your YouTube account
3. Grant permissions
4. The credentials will be saved for future use

### 4. Weekly Schedule Setup

1. Open the **Schedule** tab in the application
2. Check the days you want to upload videos
3. Set the time for each day (HH:MM format)
4. Click **Save Schedule**

Example:
- Monday: 09:00
- Wednesday: 14:00
- Friday: 18:00

### 5. Custom AI Instructions

In the **Settings** tab, you can customize the AI agent's behavior:

```text
Generate engaging, high-quality videos suitable for YouTube.
Focus on educational content about technology and science.
Keep videos between 45-60 seconds.
Use vibrant colors and dynamic camera movements.
Avoid controversial topics.
```

---

## Usage

### Manual Workflow Execution

1. Open the application
2. Go to the **Dashboard** tab
3. Click **Run Workflow Now**
4. Watch the progress in real-time

### Scheduled Automation

1. Configure your weekly schedule in the **Schedule** tab
2. The application will automatically run at scheduled times
3. Check the **Logs** tab to see execution history

### Viewing Logs

1. Go to the **Logs** tab
2. Click **Refresh Logs** to see the latest entries
3. Logs include:
   - Workflow execution status
   - Video generation details
   - Upload confirmation
   - Error messages (if any)

---

## Workflow Steps

The application executes the following automated workflow:

### 1. AI Agent Planning (Gemini 2.5 Flash)
- Analyzes custom instructions
- Generates creative video prompt
- Creates SEO-optimized metadata

### 2. Sora 2 Video Generation
- Sends prompt to OpenAI's Sora API
- Generates video based on specifications
- Downloads and saves locally

### 3. Watermark Removal (KLing)
- Processes video with KLing tool
- Removes Sora watermarks
- Falls back to FFmpeg if needed

### 4. Video Enhancement
- Upscales video quality
- Applies enhancement filters
- Optimizes for YouTube

### 5. YouTube Upload
- Uploads video with metadata
- Sets privacy status
- Logs video ID and URL

---

## Windows Startup Automation

### Setup Automatic Startup

1. **Right-click** `setup_startup.bat`
2. Select **Run as Administrator**
3. Follow the prompts
4. The application will now start automatically when Windows boots

### Manual Task Scheduler Setup

Alternatively, you can manually create a task:

1. Open **Task Scheduler** (search in Start menu)
2. Click **Create Task**
3. Name: "AIAgentGUI"
4. Trigger: **At log on**
5. Action: Run `start_ai_agent.bat`
6. Check **Run with highest privileges**

### Disable Startup

Run this command as Administrator:
```batch
schtasks /delete /tn "AIAgentGUI" /f
```

---

## Directory Structure

```
ai_agent_gui/
├── main.py                      # Main application entry point
├── requirements.txt             # Python dependencies
├── start_ai_agent.bat          # Startup script
├── setup_startup.bat           # Startup automation setup
├── README.md                   # This file
├── settings.json               # Auto-generated settings file
├── client_secrets.json         # YouTube OAuth credentials (you provide)
├── token.pickle                # Auto-generated YouTube auth token
│
├── modules/                    # Application modules
│   ├── __init__.py
│   ├── settings_manager.py     # Settings persistence
│   ├── logger.py               # Logging system
│   ├── gemini_agent.py         # Gemini AI integration
│   ├── sora_generator.py       # Sora video generation
│   ├── watermark_remover.py    # KLing watermark removal
│   ├── youtube_uploader.py     # YouTube upload functionality
│   ├── scheduler.py            # Scheduling system
│   └── workflow_manager.py     # Workflow orchestration
│
├── output/                     # Generated videos (auto-created)
├── temp/                       # Temporary files (auto-created)
└── logs/                       # Log files (auto-created)
    ├── workflow_YYYYMM.log     # Monthly log files
    └── upload_tracker.json     # Upload history
```

---

## Troubleshooting

### Issue: "Gemini API Key Invalid"
**Solution**: Verify your API key at [ai.google.dev](https://ai.google.dev/)

### Issue: "OpenAI API Error"
**Solution**: 
- Check if you have Sora API access
- Verify your API key
- Check API usage limits

### Issue: "YouTube Upload Failed"
**Solution**:
- Delete `token.pickle` and re-authenticate
- Verify `client_secrets.json` is in the correct location
- Check YouTube API quota limits

### Issue: "KLing Tool Not Found"
**Solution**: The application will automatically fall back to FFmpeg. Ensure FFmpeg is installed and in PATH.

### Issue: "Video Already Uploaded Today"
**Solution**: The system prevents duplicate uploads. Check logs or manually edit `logs/upload_tracker.json` if needed.

### Issue: "Application Won't Start"
**Solution**:
- Check Python version: `python --version` (must be 3.8+)
- Reinstall dependencies: `pip install -r requirements.txt --upgrade`
- Check logs for error messages

---

## API Costs and Limits

### OpenAI (Sora 2)
- Video generation costs vary based on duration and resolution
- Check current pricing at [openai.com/pricing](https://openai.com/pricing)

### Google Gemini
- Gemini 2.5 Flash has a generous free tier
- Check limits at [ai.google.dev/pricing](https://ai.google.dev/pricing)

### YouTube API
- Free quota: 10,000 units/day
- Each upload costs ~1,600 units
- Allows ~6 uploads per day
- Quota resets at midnight Pacific Time

---

## Security Best Practices

1. **Never share your API keys**
2. **Never commit `settings.json` or `client_secrets.json` to version control**
3. **Keep `token.pickle` secure** (contains YouTube authentication)
4. **Use environment variables** for production deployments
5. **Regularly rotate API keys**
6. **Monitor API usage** to detect unauthorized access

---

## Advanced Configuration

### Custom Video Resolution

Edit in Settings tab or directly in `settings.json`:
```json
{
    "video_resolution": "1080p",  // Options: 1080p, 720p, 480p
    "video_duration": 30           // Duration in seconds
}
```

### Custom Output Directory

```json
{
    "output_directory": "output",
    "temp_directory": "temp"
}
```

### Privacy Status Options

In `youtube_uploader.py`, you can modify the default privacy status:
- `"public"` - Visible to everyone
- `"unlisted"` - Only people with link can view
- `"private"` - Only you can view

---

## Development

### Running in Development Mode

```batch
# Activate virtual environment
venv\Scripts\activate

# Run with debug logging
python main.py
```

### Testing Individual Components

```python
# Test Gemini Agent
from modules.gemini_agent import GeminiAgent
agent = GeminiAgent("your-api-key")
prompt = agent.generate_video_prompt()
print(prompt)

# Test YouTube Upload
from modules.youtube_uploader import YouTubeUploader
uploader = YouTubeUploader()
# Upload video...
```

---

## Contributing

This is a custom application for your workflow. Feel free to modify and extend it:

- Add new AI models
- Implement different video styles
- Add more YouTube automation features
- Improve error handling
- Add email notifications

---

## License

This application is provided as-is for your personal use.

External components:
- KLing Watermark Remover: See original repository license
- Google Gemini: Google's terms of service
- OpenAI Sora: OpenAI's terms of service
- YouTube API: Google's terms of service

---

## Support

### Resources
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Google Gemini AI Documentation](https://ai.google.dev/docs)
- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)

### Common Questions

**Q: Can I run multiple instances?**
A: Yes, but each needs its own directory and configuration.

**Q: Can I use this on Linux/Mac?**
A: The Python code is cross-platform, but the .bat files are Windows-only. Create equivalent .sh scripts for Linux/Mac.

**Q: How much does this cost to run?**
A: Costs depend on your API usage. Gemini Flash is mostly free, YouTube is free, but Sora has per-video generation costs.

**Q: Can I monetize the generated videos?**
A: Review OpenAI's usage policies regarding commercial use of Sora-generated content.

---

## Changelog

### Version 1.0.0 (Initial Release)
- Complete GUI application
- Gemini 2.5 Flash integration
- Sora 2 video generation
- KLing watermark removal
- YouTube upload automation
- Weekly scheduling
- Comprehensive logging
- Windows startup automation

---

## Acknowledgments

- OpenAI for Sora 2 video generation
- Google for Gemini AI and YouTube API
- KLing watermark remover contributors
- Python and tkinter communities

---

**Happy Automating! 🚀**

