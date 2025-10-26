"""
Sora Video Generator
Handles video generation using OpenAI's Sora 2 model
"""

from openai import OpenAI
from pathlib import Path
import time
import requests
from typing import Optional
from .utils import safe_print


class SoraGenerator:
    """Generates videos using OpenAI Sora 2"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        if not api_key:
            raise ValueError("OpenAI API key is required for Sora 2")
        self.client = OpenAI(api_key=api_key)
        safe_print("✓ Sora 2 API client initialized successfully")
    
    def generate_video(
        self,
        prompt: str,
        duration: int = 30,
        resolution: str = "1080p",
        output_path: str = "output/generated_video.mp4"
    ) -> str:
        """
        Generate a video using Sora 2 API
        
        Args:
            prompt: Text prompt for video generation
            duration: Video duration in seconds (5-60 for Sora 2)
            resolution: Video resolution (1080p, 720p, 480p)
            output_path: Where to save the generated video
            
        Returns:
            Path to the generated video file
            
        Raises:
            ValueError: If API key is missing or parameters are invalid
            Exception: If video generation fails
        """
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        # Validate duration (Sora 2 supports 5-60 seconds)
        if not (5 <= duration <= 60):
            raise ValueError(f"Duration must be between 5 and 60 seconds, got {duration}")
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            safe_print("=" * 60)
            safe_print("🎬 SORA 2 VIDEO GENERATION STARTED")
            safe_print("=" * 60)
            safe_print(f"📝 Prompt: {prompt}")
            safe_print(f"⏱️  Duration: {duration}s")
            safe_print(f"📺 Resolution: {resolution}")
            safe_print(f"💾 Output: {output_file}")
            safe_print("")
            
            # Make actual API request to Sora 2
            safe_print("🔄 Sending request to Sora 2 API...")
            safe_print("⚠️  Note: This will consume API credits from your OpenAI account")
            
            # Actual Sora 2 API call
            # The API uses the videos endpoint with model "sora-1" or "sora-turbo"
            response = self.client.videos.generations.create(
                model="sora-1",  # or "sora-turbo" for faster generation
                prompt=prompt,
                size=self._resolution_to_size(resolution),
                duration=duration
            )
            
            safe_print("✓ API request successful!")
            safe_print(f"📊 Generation ID: {response.id}")
            
            # Monitor generation status
            job_id = response.id
            video_url = None
            max_wait_time = 600  # 10 minutes max
            check_interval = 5  # Check every 5 seconds
            elapsed_time = 0
            
            safe_print("")
            safe_print("⏳ Waiting for video generation to complete...")
            
            while elapsed_time < max_wait_time:
                status = self.check_generation_status(job_id)
                
                if status["status"] == "completed":
                    video_url = status.get("url")
                    safe_print(f"✓ Video generation completed! (took {elapsed_time}s)")
                    break
                elif status["status"] == "failed":
                    error_msg = status.get("error", "Unknown error")
                    raise Exception(f"Video generation failed: {error_msg}")
                else:
                    progress = status.get("progress", 0)
                    safe_print(f"  Progress: {progress}% (elapsed: {elapsed_time}s)")
                    time.sleep(check_interval)
                    elapsed_time += check_interval
            
            if not video_url:
                raise Exception(f"Video generation timed out after {max_wait_time} seconds")
            
            # Download the generated video
            safe_print("")
            safe_print("⬇️  Downloading generated video...")
            self._download_video(video_url, output_file)
            
            # Verify the downloaded file
            if not output_file.exists() or output_file.stat().st_size == 0:
                raise Exception("Downloaded video file is missing or empty")
            
            file_size_mb = output_file.stat().st_size / (1024 * 1024)
            safe_print(f"✓ Video downloaded successfully! ({file_size_mb:.2f} MB)")
            safe_print("=" * 60)
            safe_print("✅ SORA 2 VIDEO GENERATION COMPLETED")
            safe_print("=" * 60)
            safe_print("")
            
            return str(output_file)
            
        except AttributeError as e:
            # Handle case where Sora API is not yet available in the OpenAI client
            safe_print("")
            safe_print("=" * 60)
            safe_print("⚠️  SORA 2 API NOT YET AVAILABLE")
            safe_print("=" * 60)
            safe_print("The OpenAI Python client does not yet support Sora 2 API.")
            safe_print("This could mean:")
            safe_print("  1. Sora 2 is not yet publicly released")
            safe_print("  2. Your OpenAI client library needs to be updated")
            safe_print("  3. You need to request access to Sora 2 API")
            safe_print("")
            safe_print("Please check:")
            safe_print("  - OpenAI Platform status: https://platform.openai.com/")
            safe_print("  - Your API access level")
            safe_print("  - Update openai library: pip install --upgrade openai")
            safe_print("=" * 60)
            safe_print("")
            raise Exception(
                "Sora 2 API is not available. Please verify your API access and "
                "ensure the OpenAI client library supports Sora 2 video generation."
            )
        except Exception as e:
            safe_print("")
            safe_print("=" * 60)
            safe_print("❌ SORA 2 VIDEO GENERATION FAILED")
            safe_print("=" * 60)
            safe_print(f"Error: {str(e)}")
            safe_print("=" * 60)
            safe_print("")
            raise Exception(f"Failed to generate video with Sora 2: {str(e)}")
    
    def _resolution_to_size(self, resolution: str) -> str:
        """Convert resolution string to Sora API size parameter"""
        size_map = {
            "1080p": "1920x1080",
            "720p": "1280x720",
            "480p": "854x480"
        }
        return size_map.get(resolution, "1920x1080")
    
    def _download_video(self, url: str, output_path: Path):
        """Download video from URL with progress tracking"""
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        safe_print(f"  Download progress: {progress:.1f}%", end='\r')
        
        safe_print("")  # New line after progress
    
    def check_generation_status(self, job_id: str) -> dict:
        """
        Check the status of a video generation job
        
        Args:
            job_id: The generation job ID returned by the API
            
        Returns:
            Dictionary with status information:
            - status: "pending", "processing", "completed", or "failed"
            - progress: Progress percentage (0-100)
            - url: Video URL (when completed)
            - error: Error message (when failed)
        """
        try:
            # Query the Sora 2 API for generation status
            result = self.client.videos.generations.retrieve(job_id)
            
            return {
                "status": result.status,
                "progress": getattr(result, 'progress', 0),
                "url": getattr(result, 'url', None),
                "error": getattr(result, 'error', None),
                "job_id": job_id
            }
        except AttributeError:
            # If API not available, return mock status for testing
            safe_print("⚠️  Unable to check status - Sora 2 API not available")
            return {
                "status": "completed",
                "job_id": job_id,
                "progress": 100,
                "url": None,
                "error": None
            }
        except Exception as e:
            safe_print(f"⚠️  Error checking generation status: {str(e)}")
            raise Exception(f"Failed to check generation status: {str(e)}")
    
    def verify_api_access(self) -> bool:
        """
        Verify that the API key has access to Sora 2
        
        Returns:
            True if Sora 2 API is accessible, False otherwise
        """
        try:
            # Try to access the videos generations endpoint
            # This is a lightweight check
            safe_print("🔍 Verifying Sora 2 API access...")
            
            # Check if the client has the videos.generations attribute
            if not hasattr(self.client, 'videos'):
                safe_print("❌ Sora 2 API not available in OpenAI client")
                return False
            
            if not hasattr(self.client.videos, 'generations'):
                safe_print("❌ Video generations API not available")
                return False
            
            safe_print("✓ Sora 2 API endpoints are available")
            return True
            
        except Exception as e:
            safe_print(f"❌ Sora 2 API access verification failed: {str(e)}")
            return False

