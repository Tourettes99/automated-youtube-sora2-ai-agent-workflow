"""
Workflow Logger
Manages logging with date tracking for workflow execution
"""

import logging
from pathlib import Path
from datetime import datetime
import json


class WorkflowLogger:
    """Handles logging for the AI agent workflow"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(__file__).parent.parent / log_dir
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup main log file
        self.log_file = self.log_dir / f"workflow_{datetime.now().strftime('%Y%m')}.log"
        
        # Setup upload tracking file
        self.upload_tracker_file = self.log_dir / "upload_tracker.json"
        self.upload_tracker = self.load_upload_tracker()
        
        # Configure logging
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_upload_tracker(self) -> dict:
        """Load upload tracker from file"""
        if self.upload_tracker_file.exists():
            try:
                with open(self.upload_tracker_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading upload tracker: {e}")
                return {}
        return {}
    
    def save_upload_tracker(self):
        """Save upload tracker to file"""
        try:
            with open(self.upload_tracker_file, 'w', encoding='utf-8') as f:
                json.dump(self.upload_tracker, f, indent=4)
        except Exception as e:
            print(f"Error saving upload tracker: {e}")
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message"""
        if level == "INFO":
            self.logger.info(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "ERROR":
            self.logger.error(message)
        elif level == "DEBUG":
            self.logger.debug(message)
    
    def has_uploaded_today(self, day_of_week: str) -> bool:
        """Check if a video has been uploaded today for the given day of week"""
        today = datetime.now().strftime('%Y-%m-%d')
        current_day = datetime.now().strftime('%A')
        
        # Check if current day matches the scheduled day
        if current_day != day_of_week:
            return False
        
        # Check if already uploaded today
        if today in self.upload_tracker:
            return self.upload_tracker[today].get('uploaded', False)
        
        return False
    
    def mark_uploaded(self, video_id: str, video_title: str):
        """Mark today as uploaded with video details"""
        today = datetime.now().strftime('%Y-%m-%d')
        day_of_week = datetime.now().strftime('%A')
        
        self.upload_tracker[today] = {
            'uploaded': True,
            'video_id': video_id,
            'video_title': video_title,
            'day_of_week': day_of_week,
            'timestamp': datetime.now().isoformat()
        }
        
        self.save_upload_tracker()
        self.log(f"Marked upload complete for {today}: {video_title} (ID: {video_id})")
    
    def get_recent_logs(self, lines: int = 100) -> str:
        """Get recent log entries"""
        try:
            if self.log_file.exists():
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    all_lines = f.readlines()
                    return ''.join(all_lines[-lines:])
            return "No logs available"
        except Exception as e:
            return f"Error reading logs: {str(e)}"
    
    def get_upload_history(self, days: int = 30) -> dict:
        """Get upload history for the last N days"""
        return self.upload_tracker

