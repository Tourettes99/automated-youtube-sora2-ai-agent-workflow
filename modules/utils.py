"""
Utility functions for the AI agent workflow
"""

import sys


def safe_print(message: str):
    """
    Safely print messages with proper encoding handling
    Prevents 'charmap' codec errors on Windows
    """
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback: encode to ASCII with replacement
        safe_message = message.encode('ascii', errors='replace').decode('ascii')
        print(safe_message)
    except Exception as e:
        # Last resort: print without problematic characters
        print(f"[Message contained unprintable characters: {type(e).__name__}]")


def setup_console_encoding():
    """
    Setup UTF-8 encoding for console output on Windows
    Call this at application startup
    """
    if sys.platform == 'win32':
        try:
            import io
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer, 
                encoding='utf-8', 
                errors='replace',
                line_buffering=True
            )
            sys.stderr = io.TextIOWrapper(
                sys.stderr.buffer, 
                encoding='utf-8', 
                errors='replace',
                line_buffering=True
            )
        except Exception as e:
            print(f"Warning: Could not set UTF-8 encoding: {e}")


def sanitize_text(text: str) -> str:
    """
    Sanitize text to remove problematic Unicode characters
    while preserving readability
    """
    try:
        # Try UTF-8 encoding first
        text.encode('utf-8')
        return text
    except UnicodeEncodeError:
        # Replace emojis and other problematic characters
        import re
        # Remove emojis and special unicode characters
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

