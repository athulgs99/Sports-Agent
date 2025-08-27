import os
import time
import logging
import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import requests
from groq import Groq
from gtts import gTTS
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def validate_team_id(team_id: str) -> bool:
    """
    Validate team ID format.
    
    Args:
        team_id: The team ID to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not team_id:
        return False
    
    # Check if it's a numeric string (most sports APIs use numeric IDs)
    if not re.match(r'^\d+$', team_id):
        return False
    
    return True

def validate_commentator(commentator: str) -> bool:
    """
    Validate commentator name.
    
    Args:
        commentator: The commentator name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return commentator in Config.COMMENTATORS

def validate_language(language: str) -> bool:
    """
    Validate language selection.
    
    Args:
        language: The language to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return language in Config.VOICE_SETTINGS

def get_recent_scores(team_id: str) -> List[str]:
    """
    Fetches recent game scores for a given team ID from TheSportsDB API.
    
    Args:
        team_id: The team ID to fetch scores for
        
    Returns:
        List[str]: List of game summaries
    """
    if not validate_team_id(team_id):
        logger.error(f"Invalid team ID: {team_id}")
        return []
    
    url = f"{Config.SPORTS_API_BASE_URL}/{Config.SPORTS_API_KEY}/eventslast.php?id={team_id}"
    
    try:
        logger.info(f"Fetching scores for team ID: {team_id}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        events = data.get('results', [])
        
        if not events:
            logger.warning(f"No events found for team ID: {team_id}")
            return []
        
        summary = []
        for event in events[:5]:  # Limit to 5 most recent games
            try:
                event_str = f"{event['strEvent']} on {event['dateEvent']} - Score: {event['intHomeScore']}:{event['intAwayScore']}"
                summary.append(event_str)
            except KeyError as e:
                logger.warning(f"Missing key in event data: {e}")
                continue
        
        logger.info(f"Successfully fetched {len(summary)} games for team ID: {team_id}")
        return summary
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error fetching scores for team {team_id}: {e}")
        return []
    except ValueError as e:
        logger.error(f"JSON parsing error for team {team_id}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching scores for team {team_id}: {e}")
        return []

def generate_commentary(team_id: str, commentator: str, language: str) -> str:
    """
    Generates sports commentary based on a team's recent games.
    
    Args:
        team_id: The team ID
        commentator: The commentator personality
        language: The language for commentary
        
    Returns:
        str: Generated commentary text
    """
    # Validate inputs
    if not validate_team_id(team_id):
        raise ValidationError("Invalid team ID")
    
    if not validate_commentator(commentator):
        raise ValidationError("Invalid commentator")
    
    if not validate_language(language):
        raise ValidationError("Invalid language")
    
    games = get_recent_scores(team_id)
    if not games:
        return "No recent games found for this team."

    prompt = f"""
You are {commentator}, {Config.COMMENTATORS[commentator]}.
Here are the recent games:
{chr(10).join(games)}

Please generate a unique, lively, and engaging commentary for each game in {language}.
Avoid starting with "You are {commentator}".
End each game commentary naturally, make it exciting.
"""
    
    try:
        logger.info(f"Generating commentary for team {team_id} with {commentator} in {language}")
        client = Groq(api_key=Config.GROQ_API_KEY)
        
        response = client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        
        commentary_text = response.choices[0].message.content.strip()
        logger.info(f"Successfully generated commentary for team {team_id}")
        return commentary_text
        
    except Exception as e:
        logger.error(f"LLM error generating commentary: {e}")
        # Fallback simple static commentary
        return "\n".join([f"{game}. What a thrilling match!" for game in games])

def text_to_speech(text: str, language: str = "English") -> Optional[str]:
    """
    Converts text to speech and saves as MP3 file.
    
    Args:
        text: The text to convert
        language: The language for speech synthesis
        
    Returns:
        Optional[str]: Path to the audio file, or None if failed
    """
    if not validate_language(language):
        logger.error(f"Invalid language: {language}")
        return None
    
    try:
        timestamp = int(time.time() * 1000)
        filename = f"{Config.STATIC_FOLDER}/commentary_{timestamp}.mp3"
        
        logger.info(f"Converting text to speech in {language}")
        
        tts = gTTS(text=text, **Config.VOICE_SETTINGS[language])
        tts.save(filename)
        
        logger.info(f"Audio file saved: {filename}")
        return filename
        
    except Exception as e:
        logger.error(f"Text-to-speech error: {e}")
        return None

def cleanup_old_audio_files():
    """
    Clean up old audio files to prevent disk space issues.
    """
    try:
        if not os.path.exists(Config.STATIC_FOLDER):
            return
        
        current_time = time.time()
        audio_files = []
        
        for filename in os.listdir(Config.STATIC_FOLDER):
            if filename.endswith('.mp3'):
                filepath = os.path.join(Config.STATIC_FOLDER, filename)
                file_age = current_time - os.path.getmtime(filepath)
                
                if file_age > Config.AUDIO_CACHE_DURATION:
                    try:
                        os.remove(filepath)
                        logger.info(f"Removed old audio file: {filename}")
                    except OSError as e:
                        logger.error(f"Error removing file {filename}: {e}")
                else:
                    audio_files.append((filepath, file_age))
        
        # If we have too many files, remove the oldest ones
        if len(audio_files) > Config.MAX_AUDIO_FILES:
            audio_files.sort(key=lambda x: x[1], reverse=True)
            for filepath, _ in audio_files[Config.MAX_AUDIO_FILES:]:
                try:
                    os.remove(filepath)
                    logger.info(f"Removed excess audio file: {os.path.basename(filepath)}")
                except OSError as e:
                    logger.error(f"Error removing excess file {filepath}: {e}")
                    
    except Exception as e:
        logger.error(f"Error during audio cleanup: {e}")

def get_team_name(team_id: str) -> str:
    """
    Get team name from team ID.
    
    Args:
        team_id: The team ID
        
    Returns:
        str: Team name or "Unknown Team"
    """
    return Config.SAMPLE_TEAMS.get(team_id, "Unknown Team")
