"""
Gemini AI Agent
Uses Google Gemini 2.5 Flash for intelligent workflow orchestration
"""

import google.generativeai as genai
from typing import Dict, Optional
from .utils import sanitize_text


class GeminiAgent:
    """AI Agent powered by Google Gemini 2.5 Flash"""
    
    def __init__(self, api_key: str, custom_instructions: str = ""):
        self.api_key = api_key
        self.custom_instructions = custom_instructions
        self.model = None
        self.initialize_model()
    
    def initialize_model(self):
        """Initialize the Gemini model"""
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        genai.configure(api_key=self.api_key)
        
        # Use Gemini 2.5 Flash
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate_video_prompt(self) -> str:
        """
        Generate a creative video prompt for Sora 2
        Returns a detailed prompt for video generation
        """
        system_prompt = f"""
        You are an AI agent responsible for generating creative video prompts for Sora 2 (OpenAI's video generation model).
        
        Custom Instructions: {self.custom_instructions}
        
        Generate a single, detailed video prompt that:
        1. Is engaging and suitable for YouTube
        2. Is visually interesting and cinematic
        3. Has clear narrative or visual progression
        4. Is appropriate for a 30-60 second video
        5. Avoids copyright issues or controversial content
        
        Return ONLY the video prompt, nothing else. Make it detailed and descriptive.
        """
        
        try:
            response = self.model.generate_content(system_prompt)
            prompt = response.text.strip()
            # Sanitize prompt to remove emojis and problematic characters
            prompt = sanitize_text(prompt)
            return prompt
        except Exception as e:
            raise Exception(f"Failed to generate video prompt: {str(e)}")
    
    def generate_video_metadata(self, video_description: str) -> Dict[str, str]:
        """
        Generate YouTube metadata (title, description, tags) based on video content
        """
        system_prompt = f"""
        You are an AI agent creating YouTube metadata for a video.
        
        Video Prompt: {video_description}
        
        Generate appropriate YouTube metadata in the following JSON format:
        {{
            "title": "An engaging, SEO-friendly title (max 100 characters)",
            "description": "A detailed description with relevant information and keywords",
            "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"]
        }}
        
        Make the title catchy and click-worthy while being accurate.
        Include relevant hashtags and keywords in the description.
        Choose 5-10 relevant tags.
        
        Return ONLY valid JSON, nothing else.
        """
        
        try:
            response = self.model.generate_content(system_prompt)
            import json
            response_text = sanitize_text(response.text.strip())
            metadata = json.loads(response_text)
            
            # Sanitize all metadata fields
            metadata['title'] = sanitize_text(metadata.get('title', 'AI Generated Video'))
            metadata['description'] = sanitize_text(metadata.get('description', ''))
            metadata['tags'] = [sanitize_text(tag) for tag in metadata.get('tags', [])]
            
            return metadata
        except Exception as e:
            # Fallback metadata
            return {
                "title": "AI Generated Video",
                "description": f"Video generated using AI: {sanitize_text(video_description)}",
                "tags": ["AI", "Generated", "Video", "Sora"]
            }
    
    def analyze_workflow_status(self, current_step: str, error: Optional[str] = None) -> str:
        """
        Analyze workflow status and provide recommendations
        """
        if error:
            prompt = f"""
            The AI workflow encountered an error at step: {current_step}
            Error: {error}
            
            Provide a brief analysis and suggestion for resolution.
            Keep response under 100 words.
            """
        else:
            prompt = f"""
            The AI workflow successfully completed step: {current_step}
            
            Provide a brief status update.
            Keep response under 50 words.
            """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Status: {current_step} {'- Error occurred' if error else '- Completed'}"

