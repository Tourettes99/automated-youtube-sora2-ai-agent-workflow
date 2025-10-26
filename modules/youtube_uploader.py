"""
YouTube Uploader
Handles video uploads to YouTube using YouTube Data API v3
"""

import os
import pickle
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from .utils import safe_print


class YouTubeUploader:
    """Uploads videos to YouTube using the Data API v3"""
    
    # OAuth 2.0 scopes
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    # YouTube API Quota limits (daily quota is 10,000 units)
    # Upload costs approximately 1600 quota units
    MAX_DAILY_UPLOADS = 6  # Conservative limit to stay within free tier
    MAX_WEEKLY_UPLOADS = 30  # Weekly limit for safety
    
    def __init__(self, client_secrets_file: str = "client_secrets.json"):
        self.client_secrets_file = Path(__file__).parent.parent / client_secrets_file
        self.credentials = None
        self.youtube = None
        self.quota_tracker_file = Path(__file__).parent.parent / "youtube_quota_tracker.json"
        self.quota_data = self.load_quota_tracker()
        self.authenticate()
    
    def load_quota_tracker(self) -> dict:
        """Load quota tracking data"""
        if self.quota_tracker_file.exists():
            try:
                with open(self.quota_tracker_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                safe_print(f"Error loading quota tracker: {e}")
                return self.init_quota_data()
        return self.init_quota_data()
    
    def init_quota_data(self) -> dict:
        """Initialize quota data structure"""
        return {
            'daily_uploads': {},
            'weekly_uploads': {},
            'last_reset': datetime.now().isoformat()
        }
    
    def save_quota_tracker(self):
        """Save quota tracking data"""
        try:
            with open(self.quota_tracker_file, 'w', encoding='utf-8') as f:
                json.dump(self.quota_data, f, indent=4)
        except Exception as e:
            safe_print(f"Error saving quota tracker: {e}")
    
    def check_quota_limit(self) -> tuple[bool, str]:
        """
        Check if we're within quota limits
        
        Returns:
            (can_upload: bool, reason: str)
        """
        today = datetime.now().strftime('%Y-%m-%d')
        current_week = datetime.now().strftime('%Y-W%W')
        
        # Clean old data (older than 8 days for daily, 5 weeks for weekly)
        self.cleanup_old_quota_data()
        
        # Check daily limit
        daily_count = self.quota_data['daily_uploads'].get(today, 0)
        if daily_count >= self.MAX_DAILY_UPLOADS:
            return False, f"Daily upload limit reached ({daily_count}/{self.MAX_DAILY_UPLOADS})"
        
        # Check weekly limit
        weekly_count = self.quota_data['weekly_uploads'].get(current_week, 0)
        if weekly_count >= self.MAX_WEEKLY_UPLOADS:
            return False, f"Weekly upload limit reached ({weekly_count}/{self.MAX_WEEKLY_UPLOADS})"
        
        return True, f"OK - Daily: {daily_count}/{self.MAX_DAILY_UPLOADS}, Weekly: {weekly_count}/{self.MAX_WEEKLY_UPLOADS}"
    
    def increment_quota_counter(self):
        """Increment upload counters"""
        today = datetime.now().strftime('%Y-%m-%d')
        current_week = datetime.now().strftime('%Y-W%W')
        
        # Increment daily counter
        self.quota_data['daily_uploads'][today] = self.quota_data['daily_uploads'].get(today, 0) + 1
        
        # Increment weekly counter
        self.quota_data['weekly_uploads'][current_week] = self.quota_data['weekly_uploads'].get(current_week, 0) + 1
        
        self.save_quota_tracker()
    
    def cleanup_old_quota_data(self):
        """Remove old quota data to keep file size manageable"""
        cutoff_date = datetime.now() - timedelta(days=8)
        cutoff_week = (datetime.now() - timedelta(weeks=5)).strftime('%Y-W%W')
        
        # Clean daily data
        to_remove = []
        for date_str in self.quota_data['daily_uploads'].keys():
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                if date_obj < cutoff_date:
                    to_remove.append(date_str)
            except:
                pass
        
        for date_str in to_remove:
            del self.quota_data['daily_uploads'][date_str]
        
        # Clean weekly data
        to_remove = []
        for week_str in self.quota_data['weekly_uploads'].keys():
            if week_str < cutoff_week:
                to_remove.append(week_str)
        
        for week_str in to_remove:
            del self.quota_data['weekly_uploads'][week_str]
    
    def authenticate(self):
        """Authenticate with YouTube API using OAuth 2.0"""
        creds = None
        token_file = Path(__file__).parent.parent / "token.pickle"
        
        # Load saved credentials
        if token_file.exists():
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If credentials are invalid or don't exist, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not self.client_secrets_file.exists():
                    safe_print(f"Client secrets file not found: {self.client_secrets_file}")
                    safe_print("Please download OAuth 2.0 credentials from Google Cloud Console")
                    safe_print("and save as 'client_secrets.json' in the application directory")
                    return
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.client_secrets_file),
                    self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next time
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.credentials = creds
        
        # Build YouTube API client
        if creds:
            self.youtube = build('youtube', 'v3', credentials=creds)
    
    def upload_video(
        self,
        video_file: str,
        title: str,
        description: str = "",
        tags: list = None,
        category_id: str = "22",  # People & Blogs
        privacy_status: str = "public",
        upload_as_shorts: bool = False
    ) -> Optional[str]:
        """
        Upload a video to YouTube (Main Channel or YouTube Shorts)
        
        Args:
            video_file: Path to the video file
            title: Video title
            description: Video description
            tags: List of tags
            category_id: YouTube category ID (22 = People & Blogs)
            privacy_status: public, private, or unlisted
            upload_as_shorts: If True, upload as YouTube Shorts with optimizations
            
        Returns:
            Video ID if successful, None otherwise
        """
        if not self.youtube:
            raise Exception("YouTube API not authenticated. Please check client_secrets.json")
        
        # Check quota limits
        can_upload, quota_msg = self.check_quota_limit()
        if not can_upload:
            raise Exception(f"Upload blocked: {quota_msg}. Please wait before uploading more videos.")
        
        safe_print(f"Quota check: {quota_msg}")
        
        video_path = Path(video_file)
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_file}")
        
        # Optimize metadata for YouTube Shorts if requested
        if upload_as_shorts:
            safe_print("📱 Uploading as YouTube Shorts")
            
            # Add #Shorts hashtag to description if not present
            shorts_hashtag = "#Shorts"
            if shorts_hashtag not in description:
                description = f"{description}\n\n{shorts_hashtag}" if description else shorts_hashtag
            
            # Add Shorts-specific tags
            shorts_tags = ["Shorts", "Short", "YouTubeShorts"]
            all_tags = list(set((tags or []) + shorts_tags))
        else:
            safe_print("📺 Uploading to main YouTube channel")
            all_tags = tags or []
        
        # Prepare video metadata
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': all_tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Create media upload
        media = MediaFileUpload(
            str(video_path),
            chunksize=-1,  # Upload in a single request
            resumable=True,
            mimetype='video/*'
        )
        
        try:
            safe_print(f"Uploading video to YouTube: {title}")
            
            # Execute upload
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    safe_print(f"Upload progress: {progress}%")
            
            video_id = response['id']
            
            # Generate appropriate URL based on upload type
            if upload_as_shorts:
                video_url = f"https://www.youtube.com/shorts/{video_id}"
            else:
                video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            # Increment quota counter after successful upload
            self.increment_quota_counter()
            
            safe_print(f"✅ Video uploaded successfully!")
            safe_print(f"  Video ID: {video_id}")
            safe_print(f"  URL: {video_url}")
            if upload_as_shorts:
                safe_print(f"  Format: YouTube Shorts")
            
            return video_id
            
        except HttpError as e:
            raise Exception(f"YouTube API error: {e}")
        except Exception as e:
            raise Exception(f"Failed to upload video: {str(e)}")
    
    def update_video(
        self,
        video_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[list] = None
    ) -> bool:
        """Update video metadata"""
        if not self.youtube:
            raise Exception("YouTube API not authenticated")
        
        try:
            # Get current video details
            video = self.youtube.videos().list(
                part='snippet',
                id=video_id
            ).execute()
            
            if not video['items']:
                raise Exception(f"Video not found: {video_id}")
            
            snippet = video['items'][0]['snippet']
            
            # Update fields
            if title:
                snippet['title'] = title
            if description:
                snippet['description'] = description
            if tags:
                snippet['tags'] = tags
            
            # Update video
            self.youtube.videos().update(
                part='snippet',
                body={
                    'id': video_id,
                    'snippet': snippet
                }
            ).execute()
            
            safe_print(f"Video updated: {video_id}")
            return True
            
        except HttpError as e:
            raise Exception(f"YouTube API error: {e}")
    
    def delete_video(self, video_id: str) -> bool:
        """Delete a video from YouTube"""
        if not self.youtube:
            raise Exception("YouTube API not authenticated")
        
        try:
            self.youtube.videos().delete(id=video_id).execute()
            safe_print(f"Video deleted: {video_id}")
            return True
        except HttpError as e:
            raise Exception(f"YouTube API error: {e}")
    
    def get_video_info(self, video_id: str) -> Dict:
        """Get video information"""
        if not self.youtube:
            raise Exception("YouTube API not authenticated")
        
        try:
            response = self.youtube.videos().list(
                part='snippet,status,statistics',
                id=video_id
            ).execute()
            
            if response['items']:
                return response['items'][0]
            return None
            
        except HttpError as e:
            raise Exception(f"YouTube API error: {e}")

