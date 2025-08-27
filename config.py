import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for the AI Sports Commentator application."""
    
    # API Keys
    SPORTS_API_KEY = os.getenv('SPORTS_API_KEY', '123')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', 'your_groq_api_key_here')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
    STATIC_FOLDER = 'static'
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # API Configuration
    SPORTS_API_BASE_URL = "https://www.thesportsdb.com/api/v1/json"
    GROQ_MODEL = "llama3-8b-8192"
    
    # Audio Configuration
    AUDIO_CACHE_DURATION = 3600  # 1 hour in seconds
    MAX_AUDIO_FILES = 10
    
    # Voice Settings for gTTS
    VOICE_SETTINGS = {
        "English": {"lang": "en", "tld": "com"},
        "Hindi": {"lang": "hi", "tld": "co.in"},
        "Spanish": {"lang": "es", "tld": "com"}
    }
    
    # Available Commentators
    COMMENTATORS = [
        "Ravi Shastri",
        "Harsha Bhogle", 
        "Tony Romo"
    ]
    
    # Sample Teams (Team ID: Team Name)
    SAMPLE_TEAMS = {
        "134860": "Boston Celtics",
        "133602": "Liverpool", 
        "133604": "Arsenal"
    }
