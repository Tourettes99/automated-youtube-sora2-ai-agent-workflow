# Configuration Template

Use this as a reference for configuring your AI Agent GUI.

## settings.json

The application auto-generates this file, but here's what it looks like:

```json
{
    "openai_api_key": "sk-...",
    "gemini_api_key": "AIza...",
    "youtube_api_key": "",
    "youtube_client_secrets": "client_secrets.json",
    "agent_instructions": "Generate engaging, high-quality videos suitable for YouTube. Focus on trending topics, educational content, or entertainment. Keep videos between 30-60 seconds.",
    "video_duration": 30,
    "video_resolution": "1080p",
    "weekly_schedule": {
        "Monday": "09:00",
        "Wednesday": "14:00",
        "Friday": "18:00"
    },
    "output_directory": "output",
    "temp_directory": "temp"
}
```

## client_secrets.json

Download this from Google Cloud Console. Format:

```json
{
    "installed": {
        "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
        "project_id": "your-project-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "YOUR_CLIENT_SECRET",
        "redirect_uris": ["http://localhost"]
    }
}
```

## Custom AI Instructions Examples

### Educational Content
```
Generate educational videos about science and technology.
Use clear explanations and visual demonstrations.
Target audience: ages 18-35.
Keep videos 45-60 seconds.
Use professional tone.
```

### Entertainment
```
Create entertaining, viral-worthy content.
Focus on trending topics and memes.
Use dynamic camera movements and transitions.
Target audience: ages 13-25.
Keep videos 30-45 seconds.
High energy and fast-paced.
```

### Product Showcases
```
Generate product demonstration videos.
Highlight key features and benefits.
Use clean, minimalist aesthetics.
Target audience: potential customers.
Keep videos 30-60 seconds.
Professional and polished.
```

### Nature/Travel
```
Create beautiful nature and travel videos.
Use cinematic camera movements.
Focus on stunning landscapes and wildlife.
Peaceful and inspiring tone.
Keep videos 45-60 seconds.
```

## Weekly Schedule Examples

### Daily Uploads
```json
{
    "Monday": "10:00",
    "Tuesday": "10:00",
    "Wednesday": "10:00",
    "Thursday": "10:00",
    "Friday": "10:00",
    "Saturday": "12:00",
    "Sunday": "12:00"
}
```

### Weekday Only
```json
{
    "Monday": "09:00",
    "Tuesday": "09:00",
    "Wednesday": "09:00",
    "Thursday": "09:00",
    "Friday": "09:00"
}
```

### Twice Weekly
```json
{
    "Tuesday": "14:00",
    "Friday": "14:00"
}
```

### Weekend Only
```json
{
    "Saturday": "11:00",
    "Sunday": "11:00"
}
```

## Video Settings

### High Quality (1080p)
```json
{
    "video_resolution": "1080p",
    "video_duration": 60
}
```

### Standard Quality (720p)
```json
{
    "video_resolution": "720p",
    "video_duration": 45
}
```

### Lower Quality (480p)
```json
{
    "video_resolution": "480p",
    "video_duration": 30
}
```

## Environment Variables (Optional)

For enhanced security, you can use environment variables instead of storing API keys in settings.json:

### Windows
```batch
setx OPENAI_API_KEY "sk-..."
setx GEMINI_API_KEY "AIza..."
```

### Modify code to use environment variables:
```python
import os

# In settings_manager.py or main.py
openai_key = os.getenv('OPENAI_API_KEY') or settings.get('openai_api_key')
gemini_key = os.getenv('GEMINI_API_KEY') or settings.get('gemini_api_key')
```

## Troubleshooting Configurations

### Reset All Settings
Delete `settings.json` and restart the application to restore defaults.

### Reset YouTube Authentication
Delete `token.pickle` and re-authenticate on next upload.

### Clear Upload History
Delete or edit `logs/upload_tracker.json`.

### Change Output Directories
```json
{
    "output_directory": "D:\\Videos\\Output",
    "temp_directory": "C:\\Temp\\AIAgent"
}
```

---

**Tip**: Always backup your `settings.json` and `client_secrets.json` files before making changes!

