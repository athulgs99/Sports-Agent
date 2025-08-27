"""
Advanced Voice Generation Utilities
Supports different voices for different commentators
"""

import requests
import time
import os
from typing import Optional
from config import Config

class VoiceGenerator:
    """Handles voice generation with different commentator personalities."""
    
    def __init__(self):
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY', '')
        self.use_elevenlabs = bool(self.elevenlabs_api_key)
    
    def get_commentator_voice_settings(self, commentator: str, language: str) -> dict:
        """Get voice settings for specific commentator and language."""
        
        # ElevenLabs Voice IDs (you'd need to create these voices)
        elevenlabs_voices = {
            "Ravi Shastri": {
                "English": "voice_id_ravi_english",
                "Hindi": "voice_id_ravi_hindi",
                "Spanish": "voice_id_ravi_spanish"
            },
            "Harsha Bhogle": {
                "English": "voice_id_harsha_english", 
                "Hindi": "voice_id_harsha_hindi",
                "Spanish": "voice_id_harsha_spanish"
            },
            "Tony Romo": {
                "English": "voice_id_tony_english",
                "Hindi": "voice_id_tony_hindi", 
                "Spanish": "voice_id_tony_spanish"
            }
        }
        
        # Azure Speech Services voices
        azure_voices = {
            "Ravi Shastri": {
                "English": "en-IN-NeerjaNeural",
                "Hindi": "hi-IN-SwaraNeural", 
                "Spanish": "es-MX-JorgeNeural"
            },
            "Harsha Bhogle": {
                "English": "en-IN-PrabhatNeural",
                "Hindi": "hi-IN-MadhurNeural",
                "Spanish": "es-MX-YagoNeural"
            },
            "Tony Romo": {
                "English": "en-US-JennyNeural",
                "Hindi": "hi-IN-SwaraNeural",
                "Spanish": "es-MX-JorgeNeural"
            }
        }
        
        return {
            "elevenlabs": elevenlabs_voices.get(commentator, {}).get(language),
            "azure": azure_voices.get(commentator, {}).get(language)
        }
    
    def generate_voice_elevenlabs(self, text: str, commentator: str, language: str) -> Optional[str]:
        """Generate voice using ElevenLabs API."""
        if not self.elevenlabs_api_key:
            return None
            
        voice_settings = self.get_commentator_voice_settings(commentator, language)
        voice_id = voice_settings.get("elevenlabs")
        
        if not voice_id:
            return None
            
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.elevenlabs_api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                timestamp = int(time.time() * 1000)
                filename = f"static/commentary_{timestamp}.mp3"
                
                with open(filename, "wb") as f:
                    f.write(response.content)
                
                return filename
        except Exception as e:
            print(f"ElevenLabs error: {e}")
            
        return None
    
    def generate_voice_azure(self, text: str, commentator: str, language: str) -> Optional[str]:
        """Generate voice using Azure Speech Services."""
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            voice_settings = self.get_commentator_voice_settings(commentator, language)
            voice_name = voice_settings.get("azure")
            
            if not voice_name:
                return None
                
            speech_config = speechsdk.SpeechConfig(
                subscription=os.getenv('AZURE_SPEECH_KEY'),
                region=os.getenv('AZURE_SPEECH_REGION')
            )
            speech_config.speech_synthesis_voice_name = voice_name
            
            timestamp = int(time.time() * 1000)
            filename = f"static/commentary_{timestamp}.mp3"
            
            audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config, 
                audio_config=audio_config
            )
            
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return filename
                
        except Exception as e:
            print(f"Azure Speech error: {e}")
            
        return None
    
    def generate_voice_fallback(self, text: str, language: str) -> Optional[str]:
        """Fallback to gTTS if advanced voice generation fails."""
        try:
            from gtts import gTTS
            
            voice_settings = {
                "English": {"lang": "en", "tld": "com"},
                "Hindi": {"lang": "hi", "tld": "co.in"},
                "Spanish": {"lang": "es", "tld": "com"}
            }
            
            settings = voice_settings.get(language, {"lang": "en", "tld": "com"})
            tts = gTTS(text=text, lang=settings["lang"], tld=settings["tld"])
            
            timestamp = int(time.time() * 1000)
            filename = f"static/commentary_{timestamp}.mp3"
            tts.save(filename)
            
            return filename
            
        except Exception as e:
            print(f"gTTS fallback error: {e}")
            return None
    
    def generate_commentator_voice(self, text: str, commentator: str, language: str) -> Optional[str]:
        """Main method to generate voice with commentator personality."""
        
        # Try ElevenLabs first (best quality, different voices)
        if self.use_elevenlabs:
            result = self.generate_voice_elevenlabs(text, commentator, language)
            if result:
                return result
        
        # Try Azure Speech Services
        azure_key = os.getenv('AZURE_SPEECH_KEY')
        if azure_key:
            result = self.generate_voice_azure(text, commentator, language)
            if result:
                return result
        
        # Fallback to gTTS (current implementation)
        return self.generate_voice_fallback(text, language)
