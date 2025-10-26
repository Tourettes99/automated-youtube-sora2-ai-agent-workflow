"""
Workflow Manager
Orchestrates the complete AI agent workflow:
1. AI Agent Planning (Gemini)
2. Sora 2 Video Generation
3. Watermark Removal (KLing)
4. Video Enhancement
5. YouTube Upload
"""

import time
import threading
from pathlib import Path
from typing import Callable, Optional

from .settings_manager import SettingsManager
from .logger import WorkflowLogger
from .gemini_agent import GeminiAgent
from .sora_generator import SoraGenerator
from .watermark_remover import WatermarkRemover
from .youtube_uploader import YouTubeUploader
from .scheduler import WorkflowScheduler


class WorkflowManager:
    """Manages the complete AI agent workflow"""
    
    def __init__(
        self,
        settings_manager: SettingsManager,
        logger: WorkflowLogger,
        progress_callback: Optional[Callable] = None
    ):
        self.settings = settings_manager
        self.logger = logger
        self.progress_callback = progress_callback
        self.should_stop = False
        self.scheduler = None
        
        # Initialize output directories
        self.setup_directories()
    
    def setup_directories(self):
        """Create necessary output directories"""
        output_dir = Path(__file__).parent.parent / self.settings.get("output_directory", "output")
        temp_dir = Path(__file__).parent.parent / self.settings.get("temp_directory", "temp")
        
        output_dir.mkdir(exist_ok=True)
        temp_dir.mkdir(exist_ok=True)
        
        self.output_dir = output_dir
        self.temp_dir = temp_dir
    
    def start_scheduler(self):
        """Start the background scheduler"""
        schedule = self.settings.get("weekly_schedule", {})
        
        if not schedule:
            self.logger.log("No schedule configured, scheduler not started")
            return
        
        self.scheduler = WorkflowScheduler(
            schedule=schedule,
            workflow_callback=self.scheduled_workflow_execution
        )
        
        self.logger.log(f"Scheduler started with schedule: {schedule}")
        self.scheduler.start()
    
    def scheduled_workflow_execution(self, day_of_week: str):
        """Execute workflow when scheduled (called by scheduler)"""
        # Check if already uploaded today
        if self.logger.has_uploaded_today(day_of_week):
            self.logger.log(f"Video already uploaded today ({day_of_week}), skipping")
            return
        
        self.logger.log(f"Starting scheduled workflow for {day_of_week}")
        self.run_workflow()
    
    def get_next_scheduled_run(self) -> str:
        """Get next scheduled run time"""
        if self.scheduler:
            return self.scheduler.get_next_scheduled_run()
        else:
            schedule = self.settings.get("weekly_schedule", {})
            if schedule:
                temp_scheduler = WorkflowScheduler(schedule, lambda x: None)
                return temp_scheduler.get_next_scheduled_run()
        return "No schedule configured"
    
    def run_workflow(self) -> bool:
        """
        Execute the complete workflow
        
        Returns:
            True if successful, False otherwise
        """
        self.should_stop = False
        self.logger.log("=" * 50)
        self.logger.log("Starting AI Agent Workflow")
        self.logger.log("=" * 50)
        
        try:
            # Step 1: AI Agent Planning
            self.update_progress("AI Agent Planning", 0, "Running")
            video_prompt, metadata = self.step_ai_planning()
            self.update_progress("AI Agent Planning", 100, "Completed")
            
            if self.should_stop:
                return False
            
            # Step 2: Sora 2 Video Generation
            self.update_progress("Sora 2 Video Generation", 0, "Running")
            generated_video = self.step_video_generation(video_prompt)
            self.update_progress("Sora 2 Video Generation", 100, "Completed")
            
            if self.should_stop:
                return False
            
            # Step 3: Watermark Removal
            self.update_progress("Watermark Removal (KLing)", 0, "Running")
            cleaned_video = self.step_watermark_removal(generated_video)
            self.update_progress("Watermark Removal (KLing)", 100, "Completed")
            
            if self.should_stop:
                return False
            
            # Step 4: Video Enhancement (included in watermark removal)
            self.update_progress("Video Enhancement", 0, "Running")
            time.sleep(1)  # Placeholder
            enhanced_video = cleaned_video  # Already enhanced in step 3
            self.update_progress("Video Enhancement", 100, "Completed")
            
            if self.should_stop:
                return False
            
            # Step 5: YouTube Upload
            self.update_progress("YouTube Upload", 0, "Running")
            video_id = self.step_youtube_upload(enhanced_video, metadata)
            self.update_progress("YouTube Upload", 100, "Completed")
            
            # Mark as uploaded
            self.logger.mark_uploaded(video_id, metadata['title'])
            
            self.logger.log("=" * 50)
            self.logger.log("✓ Workflow completed successfully!")
            self.logger.log(f"Video ID: {video_id}")
            self.logger.log("=" * 50)
            
            return True
            
        except Exception as e:
            error_msg = f"Workflow failed: {str(e)}"
            self.logger.log(error_msg, level="ERROR")
            self.update_progress("Error", 0, "Error")
            return False
    
    def step_ai_planning(self) -> tuple:
        """
        Step 1: AI Agent Planning with Gemini
        
        Returns:
            Tuple of (video_prompt, metadata)
        """
        self.logger.log("Step 1: AI Agent Planning with Gemini 2.5 Flash")
        
        gemini_key = self.settings.get("gemini_api_key")
        if not gemini_key:
            raise ValueError("Gemini API key not configured")
        
        custom_instructions = self.settings.get("agent_instructions", "")
        
        agent = GeminiAgent(gemini_key, custom_instructions)
        
        # Generate video prompt
        self.logger.log("Generating video prompt...")
        video_prompt = agent.generate_video_prompt()
        self.logger.log(f"Video prompt: {video_prompt}")
        
        # Generate metadata
        self.logger.log("Generating video metadata...")
        metadata = agent.generate_video_metadata(video_prompt)
        self.logger.log(f"Metadata: Title='{metadata['title']}'")
        
        return video_prompt, metadata
    
    def step_video_generation(self, prompt: str) -> str:
        """
        Step 2: Generate video with Sora 2 API
        
        Args:
            prompt: Video generation prompt
            
        Returns:
            Path to generated video
            
        Raises:
            ValueError: If API key is not configured
            Exception: If video generation fails or verification fails
        """
        self.logger.log("=" * 60)
        self.logger.log("Step 2: Generating video with Sora 2 API")
        self.logger.log("=" * 60)
        
        openai_key = self.settings.get("openai_api_key")
        if not openai_key:
            raise ValueError("OpenAI API key not configured. Please add your API key in Settings.")
        
        duration = self.settings.get("video_duration", 30)
        resolution = self.settings.get("video_resolution", "1080p")
        
        # Initialize Sora generator
        generator = SoraGenerator(openai_key)
        
        # Verify API access before attempting generation
        self.logger.log("Verifying Sora 2 API access...")
        if not generator.verify_api_access():
            raise Exception(
                "Cannot access Sora 2 API. Please verify:\n"
                "1. Your OpenAI API key is valid\n"
                "2. You have access to Sora 2 API\n"
                "3. Your OpenAI client library is updated (pip install --upgrade openai)"
            )
        
        output_path = self.temp_dir / "generated_video.mp4"
        
        self.logger.log(f"Generating {duration}s video at {resolution}...")
        self.logger.log("⚠️  This will consume API credits from your OpenAI account")
        
        # Generate the video using Sora 2 API
        video_path = generator.generate_video(
            prompt=prompt,
            duration=duration,
            resolution=resolution,
            output_path=str(output_path)
        )
        
        # CRITICAL: Verify that video was actually generated
        self.logger.log("")
        self.logger.log("Verifying video generation...")
        if not self._verify_video_file(video_path):
            raise Exception(
                "Video verification failed. The generated file is missing or invalid. "
                "No watermark removal or upload will be performed."
            )
        
        self.logger.log("✓ Video generation verified successfully")
        self.logger.log(f"✓ Video file: {video_path}")
        self.logger.log("=" * 60)
        return video_path
    
    def _verify_video_file(self, video_path: str) -> bool:
        """
        Verify that the video file was actually generated and is valid
        
        Args:
            video_path: Path to the video file
            
        Returns:
            True if video is valid, False otherwise
        """
        from pathlib import Path
        
        video_file = Path(video_path)
        
        # Check if file exists
        if not video_file.exists():
            self.logger.log("❌ Video file does not exist", level="ERROR")
            return False
        
        # Check if file has content (not empty)
        file_size = video_file.stat().st_size
        if file_size == 0:
            self.logger.log("❌ Video file is empty (0 bytes)", level="ERROR")
            return False
        
        # Check if file is reasonably large (at least 100 KB for a valid video)
        min_size = 100 * 1024  # 100 KB
        if file_size < min_size:
            self.logger.log(
                f"⚠️  Warning: Video file is very small ({file_size} bytes). "
                f"Expected at least {min_size} bytes for a valid video.",
                level="WARNING"
            )
            # Still return True but log warning
        
        # Log file size
        file_size_mb = file_size / (1024 * 1024)
        self.logger.log(f"✓ Video file size: {file_size_mb:.2f} MB")
        
        return True
    
    def step_watermark_removal(self, video_path: str) -> str:
        """
        Step 3: Remove watermark using KLing tool
        (Only proceeds if video was successfully generated and verified)
        
        Args:
            video_path: Path to video with watermark
            
        Returns:
            Path to cleaned video
            
        Raises:
            Exception: If watermark removal fails
        """
        self.logger.log("=" * 60)
        self.logger.log("Step 3: Removing watermark with KLing tool")
        self.logger.log("=" * 60)
        
        # Verify input video exists before processing
        if not self._verify_video_file(video_path):
            raise Exception(
                "Cannot proceed with watermark removal: Input video is invalid. "
                "Video must be generated successfully before watermark removal."
            )
        
        remover = WatermarkRemover()
        
        output_path = self.output_dir / f"cleaned_video_{int(time.time())}.mp4"
        
        self.logger.log("Processing video to remove watermark...")
        cleaned_path = remover.remove_watermark(
            input_video=video_path,
            output_video=str(output_path)
        )
        
        # Verify output video
        if not self._verify_video_file(cleaned_path):
            raise Exception("Watermark removal failed: Output video is invalid")
        
        self.logger.log(f"✓ Watermark removed: {cleaned_path}")
        self.logger.log("=" * 60)
        return cleaned_path
    
    def step_youtube_upload(self, video_path: str, metadata: dict) -> str:
        """
        Step 5: Upload video to YouTube (Main Channel or YouTube Shorts)
        (Only proceeds if video was successfully generated and processed)
        
        Args:
            video_path: Path to video file
            metadata: Video metadata (title, description, tags)
            
        Returns:
            YouTube video ID
            
        Raises:
            Exception: If upload fails
        """
        self.logger.log("=" * 60)
        self.logger.log("Step 5: Uploading video to YouTube")
        self.logger.log("=" * 60)
        
        # Verify video exists before uploading
        if not self._verify_video_file(video_path):
            raise Exception(
                "Cannot proceed with upload: Video file is invalid. "
                "Video must be successfully generated and processed before upload."
            )
        
        client_secrets = self.settings.get("youtube_client_secrets", "client_secrets.json")
        upload_destination = self.settings.get("upload_destination", "main_channel")
        
        # Determine if uploading to YouTube Shorts
        upload_as_shorts = (upload_destination == "youtube_shorts")
        
        uploader = YouTubeUploader(client_secrets)
        
        self.logger.log(f"Upload destination: {'YouTube Shorts' if upload_as_shorts else 'Main Channel'}")
        self.logger.log(f"Uploading: {metadata['title']}")
        
        video_id = uploader.upload_video(
            video_file=video_path,
            title=metadata['title'],
            description=metadata['description'],
            tags=metadata.get('tags', []),
            privacy_status="public",
            upload_as_shorts=upload_as_shorts
        )
        
        if not video_id:
            raise Exception("Failed to upload video to YouTube")
        
        self.logger.log(f"✓ Video uploaded successfully! ID: {video_id}")
        self.logger.log("=" * 60)
        return video_id
    
    def stop_workflow(self):
        """Stop the current workflow"""
        self.should_stop = True
        self.logger.log("Workflow stop requested")
    
    def update_progress(self, step: str, progress: int, status: str):
        """Update progress callback"""
        if self.progress_callback:
            self.progress_callback(step, progress, status)

