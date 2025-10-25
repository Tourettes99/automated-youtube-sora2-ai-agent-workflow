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
        Step 2: Generate video with Sora 2
        
        Args:
            prompt: Video generation prompt
            
        Returns:
            Path to generated video
        """
        self.logger.log("Step 2: Generating video with Sora 2")
        
        openai_key = self.settings.get("openai_api_key")
        if not openai_key:
            raise ValueError("OpenAI API key not configured")
        
        duration = self.settings.get("video_duration", 30)
        resolution = self.settings.get("video_resolution", "1080p")
        
        generator = SoraGenerator(openai_key)
        
        output_path = self.temp_dir / "generated_video.mp4"
        
        self.logger.log(f"Generating {duration}s video at {resolution}...")
        video_path = generator.generate_video(
            prompt=prompt,
            duration=duration,
            resolution=resolution,
            output_path=str(output_path)
        )
        
        self.logger.log(f"Video generated: {video_path}")
        return video_path
    
    def step_watermark_removal(self, video_path: str) -> str:
        """
        Step 3: Remove watermark using KLing tool
        
        Args:
            video_path: Path to video with watermark
            
        Returns:
            Path to cleaned video
        """
        self.logger.log("Step 3: Removing watermark with KLing tool")
        
        remover = WatermarkRemover()
        
        output_path = self.output_dir / f"cleaned_video_{int(time.time())}.mp4"
        
        self.logger.log("Processing video to remove watermark...")
        cleaned_path = remover.remove_watermark(
            input_video=video_path,
            output_video=str(output_path)
        )
        
        self.logger.log(f"Watermark removed: {cleaned_path}")
        return cleaned_path
    
    def step_youtube_upload(self, video_path: str, metadata: dict) -> str:
        """
        Step 5: Upload video to YouTube
        
        Args:
            video_path: Path to video file
            metadata: Video metadata (title, description, tags)
            
        Returns:
            YouTube video ID
        """
        self.logger.log("Step 5: Uploading video to YouTube")
        
        client_secrets = self.settings.get("youtube_client_secrets", "client_secrets.json")
        
        uploader = YouTubeUploader(client_secrets)
        
        self.logger.log(f"Uploading: {metadata['title']}")
        video_id = uploader.upload_video(
            video_file=video_path,
            title=metadata['title'],
            description=metadata['description'],
            tags=metadata.get('tags', []),
            privacy_status="public"
        )
        
        if not video_id:
            raise Exception("Failed to upload video to YouTube")
        
        self.logger.log(f"Video uploaded successfully! ID: {video_id}")
        return video_id
    
    def stop_workflow(self):
        """Stop the current workflow"""
        self.should_stop = True
        self.logger.log("Workflow stop requested")
    
    def update_progress(self, step: str, progress: int, status: str):
        """Update progress callback"""
        if self.progress_callback:
            self.progress_callback(step, progress, status)

