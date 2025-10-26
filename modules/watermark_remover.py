"""
Watermark Remover
Integrates KLing watermark removal tool from the codebase
"""

import sys
from pathlib import Path
import shutil
import subprocess
from .utils import safe_print


class WatermarkRemover:
    """Removes watermarks from videos using KLing tool"""
    
    def __init__(self):
        # Path to KLing watermark remover in the codebase
        self.kling_path = self.find_kling_path()
        self.setup_environment()
        self.has_nvidia_gpu = self.check_nvidia_gpu()
        self.ffmpeg_encoder = self.get_best_encoder()
    
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
        safe_print("KLing tool not found in expected locations")
        return None
    
    def setup_environment(self):
        """Setup the environment for KLing tool"""
        if self.kling_path and self.kling_path.exists():
            # Add KLing path to sys.path
            sys.path.insert(0, str(self.kling_path))
    
    def check_nvidia_gpu(self) -> bool:
        """Check if NVIDIA GPU with NVENC is available"""
        try:
            # Check for nvidia-smi
            result = subprocess.run(
                ['nvidia-smi'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                safe_print("NVIDIA GPU detected")
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        safe_print("No NVIDIA GPU detected, using CPU encoding")
        return False
    
    def get_best_encoder(self) -> dict:
        """
        Get the best available encoder configuration
        Prioritizes NVIDIA GPU hardware acceleration
        """
        if self.has_nvidia_gpu:
            # Try NVENC (NVIDIA hardware encoder)
            if self._test_encoder('h264_nvenc'):
                safe_print("Using NVIDIA NVENC hardware encoder")
                return {
                    'vcodec': 'h264_nvenc',
                    'preset': 'p7',  # Best quality preset for NVENC
                    'rc': 'vbr',  # Variable bitrate
                    'cq': '19',  # Quality level (0-51, lower is better)
                    'b:v': '5M',  # Bitrate
                    'profile': 'high',
                    'gpu': '0'
                }
        
        # Fallback to CPU encoder
        if self._test_encoder('libx264'):
            safe_print("Using CPU libx264 encoder")
            return {
                'vcodec': 'libx264',
                'preset': 'medium',
                'crf': '23',  # Quality level
                'profile': 'high'
            }
        
        # Last resort: copy codec (fastest but no re-encoding)
        safe_print("Using codec copy (no re-encoding)")
        return {
            'vcodec': 'copy'
        }
    
    def _test_encoder(self, encoder: str) -> bool:
        """Test if an encoder is available in FFmpeg"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-hide_banner', '-encoders'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return encoder in result.stdout
        except:
            return False
    
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
                safe_print("KLing tool not available, using fallback method")
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
            
            safe_print(f"Removing watermark using KLing tool...")
            
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
            
            safe_print(f"Watermark removed: {output_video}")
            return output_video
            
        except ImportError as e:
            safe_print(f"KLing modules not available: {e}")
            safe_print("Falling back to simple method...")
            return self._fallback_method(input_video, output_video)
        except Exception as e:
            safe_print(f"Error using KLing tool: {e}")
            safe_print("Falling back to simple method...")
            return self._fallback_method(input_video, output_video)
    
    def _fallback_method(self, input_video: str, output_video: str) -> str:
        """
        Fallback method: Use FFmpeg to crop video (removes edge watermarks)
        This is a simple fallback when KLing tool is not available
        Optimized for NVIDIA GPU when available
        """
        try:
            safe_print("Using FFmpeg fallback for watermark removal...")
            
            # Build FFmpeg command with optimal encoder
            cmd = ['ffmpeg', '-i', input_video]
            
            # Add hardware acceleration if available
            if self.has_nvidia_gpu and self.ffmpeg_encoder['vcodec'] == 'h264_nvenc':
                cmd.extend([
                    '-hwaccel', 'cuda',
                    '-hwaccel_output_format', 'cuda'
                ])
            
            # Video filter: crop the bottom-right corner where watermarks usually are
            cmd.extend(['-vf', 'crop=iw*0.9:ih*0.9:0:0'])
            
            # Add encoder settings
            cmd.extend(['-c:v', self.ffmpeg_encoder['vcodec']])
            
            # Add encoder-specific options
            if self.ffmpeg_encoder['vcodec'] == 'h264_nvenc':
                cmd.extend([
                    '-preset', self.ffmpeg_encoder['preset'],
                    '-rc', self.ffmpeg_encoder['rc'],
                    '-cq', self.ffmpeg_encoder['cq'],
                    '-b:v', self.ffmpeg_encoder['b:v'],
                    '-profile:v', self.ffmpeg_encoder['profile']
                ])
            elif self.ffmpeg_encoder['vcodec'] == 'libx264':
                cmd.extend([
                    '-preset', self.ffmpeg_encoder['preset'],
                    '-crf', self.ffmpeg_encoder['crf'],
                    '-profile:v', self.ffmpeg_encoder['profile']
                ])
            
            # Audio settings
            cmd.extend([
                '-c:a', 'copy',  # Copy audio without re-encoding
                '-y',  # Overwrite output
                output_video
            ])
            
            safe_print(f"FFmpeg command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode == 0:
                safe_print(f"Video processed with FFmpeg: {output_video}")
                return output_video
            else:
                # If FFmpeg fails, just copy the file
                safe_print(f"FFmpeg failed with error: {result.stderr[:500]}")
                safe_print("Copying original video...")
                shutil.copy2(input_video, output_video)
                return output_video
                
        except Exception as e:
            # Last resort: just copy the file
            safe_print(f"Fallback method failed: {e}")
            safe_print("Copying original video...")
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

