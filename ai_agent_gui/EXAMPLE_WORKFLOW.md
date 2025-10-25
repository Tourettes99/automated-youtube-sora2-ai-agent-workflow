# Example Workflow

This document shows you what to expect when running the AI Agent GUI workflow.

---

## Sample Workflow Execution

### Initial Configuration

**Settings Applied:**
```
- OpenAI API Key: sk-proj-***
- Gemini API Key: AIza***
- YouTube Client Secrets: client_secrets.json
- Video Duration: 30 seconds
- Video Resolution: 1080p
- Agent Instructions: "Generate educational tech videos"
```

**Schedule:**
```
Monday    09:00
Wednesday 14:00
Friday    18:00
```

---

## Workflow Step-by-Step

### Monday, 9:00 AM - Scheduled Run

#### Step 1: AI Agent Planning (Gemini 2.5 Flash)
```
Status: Running...
Progress: 50%

[LOG] AI Agent analyzing custom instructions
[LOG] Generating video prompt with Gemini 2.5 Flash
[LOG] Video prompt generated:
      "A sleek, modern laboratory where a robotic arm 
       assembles a futuristic smartphone. Camera slowly 
       orbits around the scene, highlighting the precision 
       and innovation of technology."

[LOG] Generating YouTube metadata
[LOG] Title: "The Future of Tech Manufacturing | AI Assembly"
[LOG] Description: "Watch as cutting-edge robotics demonstrate 
                    the future of smartphone manufacturing..."
[LOG] Tags: ["Technology", "Robotics", "AI", "Manufacturing", 
             "Future Tech"]

Status: Completed ✓
```

#### Step 2: Sora 2 Video Generation
```
Status: Running...
Progress: 30%

[LOG] Connecting to OpenAI Sora API
[LOG] Sending video generation request
[LOG] Duration: 30 seconds, Resolution: 1080p
[LOG] Waiting for video generation...

Progress: 60%
[LOG] Video generation in progress...

Progress: 90%
[LOG] Downloading generated video...

Progress: 100%
[LOG] Video saved: temp/generated_video.mp4
[LOG] File size: 48.2 MB
[LOG] Duration: 30.0 seconds

Status: Completed ✓
```

#### Step 3: Watermark Removal (KLing)
```
Status: Running...
Progress: 20%

[LOG] Loading KLing watermark removal tool
[LOG] Analyzing video for watermarks
[LOG] Detected watermark region: bottom-right (80%, 80%, 20%, 20%)

Progress: 40%
[LOG] Removing watermark from 900 frames...
[LOG] Processing frame 300/900...

Progress: 70%
[LOG] Processing frame 600/900...

Progress: 90%
[LOG] Processing frame 900/900...
[LOG] Watermark removal complete

Status: Completed ✓
```

#### Step 4: Video Enhancement
```
Status: Running...
Progress: 50%

[LOG] Enhancing video quality
[LOG] Upscaling resolution
[LOG] Applying filters
[LOG] Optimizing for YouTube

Progress: 100%
[LOG] Enhanced video saved: output/cleaned_video_1729850400.mp4
[LOG] File size: 52.1 MB

Status: Completed ✓
```

#### Step 5: YouTube Upload
```
Status: Running...
Progress: 0%

[LOG] Authenticating with YouTube
[LOG] Using saved credentials (token.pickle)

Progress: 10%
[LOG] Starting upload...
[LOG] Title: "The Future of Tech Manufacturing | AI Assembly"

Progress: 30%
[LOG] Upload progress: 30%

Progress: 60%
[LOG] Upload progress: 60%

Progress: 90%
[LOG] Upload progress: 90%

Progress: 100%
[LOG] Upload complete!
[LOG] Video ID: dQw4w9WgXcQ
[LOG] URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
[LOG] Privacy Status: Public

Status: Completed ✓
```

---

## Final Status

```
================================================
✓ Workflow completed successfully!
Video ID: dQw4w9WgXcQ
Video Title: The Future of Tech Manufacturing | AI Assembly
Upload Date: 2025-10-25 09:03:21
Next Scheduled Run: Wednesday (2 days) at 14:00
================================================
```

---

## Dashboard View

After successful completion, the dashboard shows:

```
┌─────────────────────────────────────────────────────┐
│ AI Agent Workflow Dashboard                         │
├─────────────────────────────────────────────────────┤
│                                                      │
│ 1. AI Agent Planning             [████████] ✓       │
│ 2. Sora 2 Video Generation      [████████] ✓       │
│ 3. Watermark Removal (KLing)    [████████] ✓       │
│ 4. Video Enhancement             [████████] ✓       │
│ 5. YouTube Upload                [████████] ✓       │
│                                                      │
│ Overall Status: Workflow Completed Successfully! ✓  │
│                                                      │
│ Next Scheduled Run: Wednesday (2 days) at 14:00     │
│                                                      │
│ [Run Workflow Now]  [Stop Workflow]                 │
└─────────────────────────────────────────────────────┘
```

---

## Logs View

The Logs tab shows detailed execution history:

```
2025-10-25 09:00:01 - INFO - ==================================================
2025-10-25 09:00:01 - INFO - Starting AI Agent Workflow
2025-10-25 09:00:01 - INFO - ==================================================
2025-10-25 09:00:02 - INFO - Step 1: AI Agent Planning with Gemini 2.5 Flash
2025-10-25 09:00:02 - INFO - Generating video prompt...
2025-10-25 09:00:05 - INFO - Video prompt: A sleek, modern laboratory...
2025-10-25 09:00:05 - INFO - Generating video metadata...
2025-10-25 09:00:07 - INFO - Metadata: Title='The Future of Tech Manufacturing | AI Assembly'
2025-10-25 09:00:07 - INFO - Step 2: Generating video with Sora 2
2025-10-25 09:00:08 - INFO - Generating 30s video at 1080p...
2025-10-25 09:01:45 - INFO - Video generated: temp/generated_video.mp4
2025-10-25 09:01:45 - INFO - Step 3: Removing watermark with KLing tool
2025-10-25 09:01:46 - INFO - Processing video to remove watermark...
2025-10-25 09:02:30 - INFO - Watermark removed: output/cleaned_video_1729850400.mp4
2025-10-25 09:02:30 - INFO - Step 5: Uploading video to YouTube
2025-10-25 09:02:31 - INFO - Uploading: The Future of Tech Manufacturing | AI Assembly
2025-10-25 09:03:15 - INFO - Upload progress: 50%
2025-10-25 09:03:20 - INFO - ✓ Video uploaded successfully!
2025-10-25 09:03:20 - INFO -   Video ID: dQw4w9WgXcQ
2025-10-25 09:03:20 - INFO -   URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
2025-10-25 09:03:21 - INFO - Marked upload complete for 2025-10-25: The Future of Tech Manufacturing | AI Assembly (ID: dQw4w9WgXcQ)
2025-10-25 09:03:21 - INFO - ==================================================
2025-10-25 09:03:21 - INFO - ✓ Workflow completed successfully!
2025-10-25 09:03:21 - INFO - Video ID: dQw4w9WgXcQ
2025-10-25 09:03:21 - INFO - ==================================================
```

---

## Upload Tracker

After upload, `logs/upload_tracker.json` is updated:

```json
{
    "2025-10-25": {
        "uploaded": true,
        "video_id": "dQw4w9WgXcQ",
        "video_title": "The Future of Tech Manufacturing | AI Assembly",
        "day_of_week": "Monday",
        "timestamp": "2025-10-25T09:03:21.123456"
    }
}
```

---

## What Happens Next

### Same Day (Monday, 9:00 AM again)
If you try to run the workflow again on Monday, the system will detect:
```
[LOG] Video already uploaded today (Monday), skipping
```

### Wednesday, 2:00 PM
The scheduler will automatically trigger the workflow again:
```
[LOG] Scheduled time reached: Wednesday at 14:00
[LOG] Starting scheduled workflow for Wednesday
[LOG] ==================================================
[LOG] Starting AI Agent Workflow
[LOG] ==================================================
```

---

## Manual Workflow Run

You can also run the workflow manually anytime by clicking "Run Workflow Now":

1. Click the button
2. Workflow starts immediately (ignores schedule)
3. Does NOT check if already uploaded today
4. Uploads will still be tracked in logs

---

## Error Handling Example

If an error occurs, you'll see:

### Example: API Key Error
```
2025-10-25 09:00:01 - INFO - Starting AI Agent Workflow
2025-10-25 09:00:02 - INFO - Step 1: AI Agent Planning
2025-10-25 09:00:02 - ERROR - Workflow failed: Gemini API key not configured
2025-10-25 09:00:02 - ERROR - Please check your settings

Dashboard shows:
Overall Status: Workflow Error - Check Logs ✗
```

### Example: YouTube Quota Exceeded
```
2025-10-25 09:03:15 - INFO - Step 5: Uploading video to YouTube
2025-10-25 09:03:16 - ERROR - YouTube API error: Quota exceeded
2025-10-25 09:03:16 - INFO - Quota resets at midnight Pacific Time
2025-10-25 09:03:16 - ERROR - Workflow failed: Failed to upload video

Dashboard shows:
5. YouTube Upload [████░░░░] ✗ Error
Overall Status: Workflow Error - Check Logs ✗
```

---

## Typical Execution Time

**Average workflow duration: 2-4 minutes**

- AI Agent Planning: 5-10 seconds
- Sora 2 Generation: 30-90 seconds (depends on video length)
- Watermark Removal: 30-60 seconds
- Video Enhancement: 10-20 seconds
- YouTube Upload: 30-60 seconds (depends on file size)

**Factors affecting speed:**
- Internet connection speed
- API response times
- Video length and resolution
- Server load

---

## Tips for Smooth Operation

1. **Test first**: Run a manual workflow before setting up automation
2. **Monitor logs**: Check logs regularly for any issues
3. **Watch quotas**: Keep an eye on API usage limits
4. **Backup settings**: Save a copy of `settings.json` and `client_secrets.json`
5. **Update schedule**: Adjust schedule based on your content strategy

---

**Happy automating! Let the AI Agent handle your video workflow while you focus on strategy! 🚀**

