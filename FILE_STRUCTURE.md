# File Structure Documentation

Complete overview of the AI Agent GUI project structure and file purposes.

---

## Root Directory

```
ai_agent_gui/
├── main.py                          # Main application entry point
├── requirements.txt                 # Python dependencies
├── settings.json                    # User settings (auto-generated)
├── client_secrets.json              # YouTube OAuth credentials (user provides)
├── token.pickle                     # YouTube auth token (auto-generated)
├── .gitignore                       # Git ignore rules
│
├── start_ai_agent.bat              # Quick launch script
├── install.bat                      # Installation script
├── setup_startup.bat               # Windows startup automation
│
├── README.md                        # Main documentation
├── QUICK_START.md                   # Quick start guide
├── API_SETUP_GUIDE.md              # Detailed API setup instructions
├── CONFIGURATION_TEMPLATE.md       # Configuration examples
├── EXAMPLE_WORKFLOW.md             # Example workflow execution
├── FILE_STRUCTURE.md               # This file
│
├── modules/                         # Core application modules
│   ├── __init__.py
│   ├── settings_manager.py         # Settings persistence
│   ├── logger.py                   # Logging system
│   ├── gemini_agent.py             # Gemini AI integration
│   ├── sora_generator.py           # Sora video generation
│   ├── watermark_remover.py        # Watermark removal
│   ├── youtube_uploader.py         # YouTube upload
│   ├── scheduler.py                # Workflow scheduler
│   └── workflow_manager.py         # Workflow orchestration
│
├── output/                          # Generated videos (auto-created)
├── temp/                            # Temporary files (auto-created)
├── logs/                            # Log files (auto-created)
└── venv/                            # Python virtual environment (auto-created)
```

---

## Core Files

### main.py
**Purpose**: Main GUI application  
**Key Components**:
- `AIAgentGUI` class - Main application window
- Dashboard tab with workflow visualization
- Settings configuration interface
- Schedule management
- Logs viewer
- Progress tracking callbacks

**When to modify**: To change UI layout, add new tabs, or modify GUI behavior

---

### requirements.txt
**Purpose**: Lists all Python package dependencies  
**Contents**:
- `google-generativeai` - Gemini AI
- `openai` - Sora 2 API
- `google-auth*` - YouTube authentication
- `google-api-python-client` - YouTube API
- `opencv-python` - Video processing
- `ffmpeg-python` - Video manipulation

**When to modify**: When adding new Python libraries

---

### settings.json
**Purpose**: Stores user configuration  
**Auto-generated**: Yes  
**Contains**:
- API keys (encrypted storage recommended)
- Custom instructions
- Video settings
- Weekly schedule
- Directory paths

**When to modify**: Directly edit for manual configuration changes

**⚠️ Security**: Never commit to version control (in .gitignore)

---

### client_secrets.json
**Purpose**: YouTube OAuth 2.0 credentials  
**User-provided**: Yes  
**Source**: Google Cloud Console

**How to get**: See API_SETUP_GUIDE.md

**⚠️ Security**: Keep private, never share

---

### token.pickle
**Purpose**: Cached YouTube authentication  
**Auto-generated**: Yes (after first YouTube auth)  
**Lifetime**: Until revoked or expired

**Troubleshooting**: Delete to re-authenticate

---

## Batch Scripts

### start_ai_agent.bat
**Purpose**: Quick launch script  
**Features**:
- Checks Python installation
- Creates/activates virtual environment
- Installs/updates dependencies
- Launches application

**Usage**: Double-click or run from command line

---

### install.bat
**Purpose**: First-time installation  
**Features**:
- Verifies Python version
- Creates virtual environment
- Installs all dependencies
- Creates necessary directories
- Checks for FFmpeg
- Optionally launches app

**Usage**: Run once during initial setup

---

### setup_startup.bat
**Purpose**: Windows startup automation  
**Requires**: Administrator privileges  
**Features**:
- Creates scheduled task
- Configures to run at logon
- Sets high priority

**Usage**: Right-click → Run as Administrator

---

## Module Files

### modules/settings_manager.py
**Purpose**: Persistent settings storage  
**Key Functions**:
- `load_settings()` - Load from JSON
- `save_settings()` - Save to JSON
- `get(key, default)` - Get setting value
- `set(key, value)` - Update setting
- `update(dict)` - Batch update

**Storage Format**: JSON file
**Default Settings**: Defined in `get_default_settings()`

---

### modules/logger.py
**Purpose**: Logging and upload tracking  
**Key Functions**:
- `log(message, level)` - Write log entry
- `has_uploaded_today(day)` - Check upload status
- `mark_uploaded(id, title)` - Record upload
- `get_recent_logs(lines)` - Retrieve logs

**Log Files**:
- `logs/workflow_YYYYMM.log` - Monthly logs
- `logs/upload_tracker.json` - Upload history

**Log Levels**: INFO, WARNING, ERROR, DEBUG

---

### modules/gemini_agent.py
**Purpose**: Gemini AI integration  
**Model**: gemini-2.5-flash  
**Key Functions**:
- `generate_video_prompt()` - Create Sora prompt
- `generate_video_metadata()` - Create YouTube metadata
- `analyze_workflow_status()` - Status analysis

**API Key**: From settings (`gemini_api_key`)

---

### modules/sora_generator.py
**Purpose**: Sora 2 video generation  
**Key Functions**:
- `generate_video()` - Generate video from prompt
- `check_generation_status()` - Check async jobs

**Parameters**:
- `prompt` - Video description
- `duration` - Length in seconds
- `resolution` - Quality (1080p, 720p, 480p)
- `output_path` - Where to save

**Note**: Contains placeholder code until Sora API is public

---

### modules/watermark_remover.py
**Purpose**: Watermark removal using KLing tool  
**Key Functions**:
- `remove_watermark()` - Process video
- `auto_detect_watermark()` - Detect location
- `_use_kling_tool()` - Use KLing if available
- `_fallback_method()` - FFmpeg fallback

**Integration**: Links to KLing codebase
**Fallback**: FFmpeg cropping if KLing unavailable

---

### modules/youtube_uploader.py
**Purpose**: YouTube Data API v3 integration  
**Key Functions**:
- `authenticate()` - OAuth 2.0 flow
- `upload_video()` - Upload with metadata
- `update_video()` - Update metadata
- `delete_video()` - Remove video
- `get_video_info()` - Fetch details

**Authentication**: OAuth 2.0 with token caching
**Scopes**: `youtube.upload`

---

### modules/scheduler.py
**Purpose**: Weekly schedule management  
**Key Functions**:
- `check_and_execute()` - Check current time
- `is_time_match()` - Compare times
- `get_next_scheduled_run()` - Calculate next run

**Schedule Format**: `{"Monday": "09:00", "Wednesday": "14:00"}`
**Check Interval**: 60 seconds

---

### modules/workflow_manager.py
**Purpose**: Complete workflow orchestration  
**Key Functions**:
- `run_workflow()` - Execute full workflow
- `step_ai_planning()` - Gemini planning
- `step_video_generation()` - Sora generation
- `step_watermark_removal()` - Watermark removal
- `step_youtube_upload()` - Upload to YouTube
- `update_progress()` - Progress callbacks

**Workflow Steps**:
1. AI Agent Planning
2. Sora 2 Video Generation
3. Watermark Removal
4. Video Enhancement
5. YouTube Upload

---

## Documentation Files

### README.md
**Purpose**: Main project documentation  
**Sections**:
- Features overview
- Installation instructions
- Configuration guide
- Usage instructions
- Troubleshooting
- API costs

**Audience**: All users

---

### QUICK_START.md
**Purpose**: Fast setup guide  
**Length**: ~5 minutes to read  
**Sections**:
- Minimal installation steps
- Essential configuration
- Quick test

**Audience**: New users wanting to start quickly

---

### API_SETUP_GUIDE.md
**Purpose**: Detailed API configuration  
**Sections**:
- OpenAI setup
- Gemini setup
- YouTube setup
- Cost breakdown
- Security practices

**Audience**: Users setting up APIs for the first time

---

### CONFIGURATION_TEMPLATE.md
**Purpose**: Configuration examples  
**Contents**:
- settings.json examples
- Schedule templates
- Custom instructions samples
- Environment variable setup

**Audience**: Users customizing the application

---

### EXAMPLE_WORKFLOW.md
**Purpose**: Shows workflow execution  
**Contents**:
- Step-by-step workflow example
- Log output examples
- Dashboard views
- Error handling examples

**Audience**: Users wanting to understand what happens

---

### FILE_STRUCTURE.md
**Purpose**: Project structure documentation  
**Contents**: This document

**Audience**: Developers and advanced users

---

## Auto-Generated Directories

### output/
**Purpose**: Stores final processed videos  
**Created**: Automatically on first run  
**Contents**: Clean, watermark-free videos ready for upload  
**Filename Pattern**: `cleaned_video_{timestamp}.mp4`

**Cleanup**: Manually delete old files to save space

---

### temp/
**Purpose**: Temporary files during processing  
**Created**: Automatically on first run  
**Contents**: 
- Generated videos from Sora
- Intermediate processing files

**Cleanup**: Can be safely deleted when no workflow is running

---

### logs/
**Purpose**: Application logs and tracking  
**Created**: Automatically on first run  
**Contents**:
- `workflow_YYYYMM.log` - Monthly log files
- `upload_tracker.json` - Upload history

**Retention**: Logs accumulate; old logs can be archived/deleted

---

### venv/
**Purpose**: Python virtual environment  
**Created**: By install.bat or manually  
**Contents**: Isolated Python packages  
**Size**: ~500 MB - 1 GB

**Cleanup**: Delete to reset environment; reinstall with install.bat

---

## File Sizes

Typical file sizes after installation:

```
ai_agent_gui/
├── Python code:          ~50 KB
├── Documentation:        ~100 KB
├── settings.json:        ~2 KB
├── client_secrets.json:  ~1 KB
├── token.pickle:         ~5 KB
├── venv/:                ~500 MB - 1 GB
├── output/ (per video):  ~50-200 MB
├── temp/ (per video):    ~50-200 MB
└── logs/:                ~1-10 MB

Total (fresh install):    ~500-600 MB
Total (with videos):      ~1-5 GB
```

---

## Important Notes

### Files to Backup
- ✅ settings.json
- ✅ client_secrets.json
- ✅ token.pickle
- ✅ logs/upload_tracker.json

### Files to Never Commit
- ❌ settings.json (contains API keys)
- ❌ client_secrets.json (OAuth secrets)
- ❌ token.pickle (auth token)
- ❌ venv/ (environment)
- ❌ output/ (videos)
- ❌ temp/ (temporary files)

### Files Safe to Share
- ✅ All .py files
- ✅ All .bat files
- ✅ All .md files
- ✅ requirements.txt
- ✅ .gitignore

---

## Customization Guide

### Adding a New Tab to the GUI
1. Edit `main.py`
2. Add `create_your_tab()` method to `AIAgentGUI` class
3. Call it in `setup_ui()`

### Adding a New Workflow Step
1. Create new module in `modules/`
2. Add method to `workflow_manager.py`
3. Update `workflow_steps` list in `main.py`
4. Add progress tracking

### Changing the Schedule Format
1. Modify `scheduler.py`
2. Update settings manager default
3. Update GUI in `main.py` schedule tab

### Adding Environment Variables
1. Add to settings_manager.py
2. Check environment before settings.json
3. Document in CONFIGURATION_TEMPLATE.md

---

## Troubleshooting File Issues

### "settings.json not found"
- Normal on first run
- Will be auto-generated with defaults

### "client_secrets.json not found"
- You need to provide this file
- See API_SETUP_GUIDE.md

### "Import Error" when running
- Run: `pip install -r requirements.txt`
- Check Python version (3.8+)

### "Permission Denied" errors
- Run as Administrator (for setup_startup.bat)
- Check file permissions

### Large disk usage
- Clean output/ and temp/ directories
- Archive old logs/
- Logs can grow to several GB over time

---

**This documentation covers the complete file structure. For usage instructions, see README.md and QUICK_START.md.**

