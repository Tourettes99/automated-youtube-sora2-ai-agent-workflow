"""
Watermark Remover
Integrates KLing watermark removal tool from the codebase
"""

import sys
from pathlib import Path
import shutil
import subprocess


class WatermarkRemover:
    """Removes watermarks from videos using KLing tool"""
    
    def __init__(self):
        # Path to KLing watermark remover in the codebase
        self.kling_path = self.find_kling_path()
        self.setup_environment()
    
    def find_kling_path(self) -> Path:
        """Find the KLing watermark remover in the codebase"""
        # Look for the KLing directory
        possible_paths = [
            Path(__file__).parent.parent.parent / "KLing-Video-WatermarkRemover-Enhancer-master" / "KLing-Video-WatermarkRemover-Enhancer-master",
            Path(__file__).parent.parent.parent / "KLing-Video-WatermarkRemover-Enhancer-master",
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        # If not found, create a simplified version
        print("⚠️ KLing tool not found in expected locations")
        return None
    
    def setup_environment(self):
        """Setup the environment for KLing tool"""
        if self.kling_path and self.kling_path.exists():
            # Add KLing path to sys.path
            sys.path.insert(0, str(self.kling_path))
    
    def remove_watermark(
        self,
        input_video: str,
        output_video: str,
        watermark_region: tuple = None
    ) -> str:
        """
        Remove watermark from video
        
        Args:
            input_video: Path to input video with watermark
            output_video: Path to save processed video
            watermark_region: Optional (x, y, width, height) of watermark location
            
        Returns:
            Path to the processed video
        """
        input_path = Path(input_video)
        output_path = Path(output_video)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input video not found: {input_video}")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if self.kling_path and self.kling_path.exists():
                # Use the actual KLing tool
                return self._use_kling_tool(str(input_path), str(output_path), watermark_region)
            else:
                # Fallback: Simple copy if KLing not available
                print("⚠️ KLing tool not available, using fallback method")
                return self._fallback_method(str(input_path), str(output_path))
                
        except Exception as e:
            raise Exception(f"Failed to remove watermark: {str(e)}")
    
    def _use_kling_tool(
        self,
        input_video: str,
        output_video: str,
        watermark_region: tuple
    ) -> str:
        """Use the actual KLing tool for watermark removal"""
        try:
            # Import KLing modules
            from modules.erase import watermark_erase
            from modules.enhance import video_enhance
            
            print(f"Removing watermark using KLing tool...")
            
            # Create temporary directory for processing
            temp_dir = Path(output_video).parent / "temp_kling"
            temp_dir.mkdir(exist_ok=True)
            
            # Step 1: Erase watermark
            temp_erased = str(temp_dir / "erased.mp4")
            
            # If watermark region is not specified, try to detect it
            # or use default bottom-right corner (common for Sora videos)
            if watermark_region is None:
                # Default: bottom-right corner (last 20% width and height)
                watermark_region = (0.8, 0.8, 0.2, 0.2)  # Relative coordinates
            
            watermark_erase(
                video_path=input_video,
                output_path=temp_erased,
                region=watermark_region
            )
            
            # Step 2: Enhance video quality
            video_enhance(
                video_path=temp_erased,
                output_path=output_video,
                scale=2  # Upscale factor
            )
            
            # Cleanup temp files
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            print(f"✓ Watermark removed: {output_video}")
            return output_video
            
        except ImportError as e:
            print(f"KLing modules not available: {e}")
            print("Falling back to simple method...")
            return self._fallback_method(input_video, output_video)
        except Exception as e:
            print(f"Error using KLing tool: {e}")
            print("Falling back to simple method...")
            return self._fallback_method(input_video, output_video)
    
    def _fallback_method(self, input_video: str, output_video: str) -> str:
        """
        Fallback method: Use FFmpeg to crop video (removes edge watermarks)
        This is a simple fallback when KLing tool is not available
        """
        try:
            print("Using FFmpeg fallback for watermark removal...")
            
            # Use FFmpeg to crop the bottom-right corner where watermarks usually are
            # This removes roughly 10% from the right and bottom edges
            cmd = [
                'ffmpeg',
                '-i', input_video,
                '-vf', 'crop=iw*0.9:ih*0.9:0:0',  # Crop 90% of width and height from top-left
                '-c:a', 'copy',  # Copy audio without re-encoding
                '-y',  # Overwrite output
                output_video
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                print(f"✓ Video processed with FFmpeg: {output_video}")
                return output_video
            else:
                # If FFmpeg fails, just copy the file
                print("FFmpeg not available, copying original video...")
                shutil.copy2(input_video, output_video)
                return output_video
                
        except Exception as e:
            # Last resort: just copy the file
            print(f"Fallback method failed: {e}")
            print("Copying original video...")
            shutil.copy2(input_video, output_video)
            return output_video
    
    def auto_detect_watermark(self, video_path: str) -> tuple:
        """
        Attempt to automatically detect watermark location
        Returns (x, y, width, height) in relative coordinates (0-1)
        """
        # This is a placeholder for auto-detection
        # In production, you could use computer vision to detect watermarks
        
        # Default: bottom-right corner (common location)
        return (0.8, 0.8, 0.2, 0.2)

