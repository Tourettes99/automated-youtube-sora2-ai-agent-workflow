"""
YouTube Uploader
Handles video uploads to YouTube using YouTube Data API v3
"""

import os
import pickle
from pathlib import Path
from typing import Dict, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError


class YouTubeUploader:
    """Uploads videos to YouTube using the Data API v3"""
    
    # OAuth 2.0 scopes
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self, client_secrets_file: str = "client_secrets.json"):
        self.client_secrets_file = Path(__file__).parent.parent / client_secrets_file
        self.credentials = None
        self.youtube = None
        self.authenticate()
    
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
                    print(f"⚠️ Client secrets file not found: {self.client_secrets_file}")
                    print("Please download OAuth 2.0 credentials from Google Cloud Console")
                    print("and save as 'client_secrets.json' in the application directory")
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
        privacy_status: str = "public"
    ) -> Optional[str]:
        """
        Upload a video to YouTube
        
        Args:
            video_file: Path to the video file
            title: Video title
            description: Video description
            tags: List of tags
            category_id: YouTube category ID (22 = People & Blogs)
            privacy_status: public, private, or unlisted
            
        Returns:
            Video ID if successful, None otherwise
        """
        if not self.youtube:
            raise Exception("YouTube API not authenticated. Please check client_secrets.json")
        
        video_path = Path(video_file)
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_file}")
        
        # Prepare video metadata
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
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
            print(f"Uploading video to YouTube: {title}")
            
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
                    print(f"Upload progress: {progress}%")
            
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            print(f"✓ Video uploaded successfully!")
            print(f"  Video ID: {video_id}")
            print(f"  URL: {video_url}")
            
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
            
            print(f"✓ Video updated: {video_id}")
            return True
            
        except HttpError as e:
            raise Exception(f"YouTube API error: {e}")
    
    def delete_video(self, video_id: str) -> bool:
        """Delete a video from YouTube"""
        if not self.youtube:
            raise Exception("YouTube API not authenticated")
        
        try:
            self.youtube.videos().delete(id=video_id).execute()
            print(f"✓ Video deleted: {video_id}")
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

