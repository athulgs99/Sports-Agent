from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from config import Config
from utils import (
    generate_commentary, 
    text_to_speech, 
    cleanup_old_audio_files,
    get_team_name,
    ValidationError,
    logger
)

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['STATIC_FOLDER'] = Config.STATIC_FOLDER

# Create static folder if it doesn't exist
os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

# ===== HELPER FUNCTIONS =====
def cleanup_audio_files():
    """Clean up old audio files periodically."""
    try:
        cleanup_old_audio_files()
    except Exception as e:
        logger.error(f"Error during audio cleanup: {e}")

# ===== ROUTES =====
@app.route("/")
def index():
    """Renders the HTML template for the user interface."""
    return render_template('index.html')

@app.route("/commentary", methods=["POST"])
def commentary():
    """
    Main API endpoint to generate commentary and audio.
    """
    try:
        req = request.get_json()
        if not req:
            return jsonify({"error": "Invalid JSON data"}), 400
        
        team_id = req.get("team_id")
        commentator = req.get("commentator", "Ravi Shastri")
        language = req.get("language", "English")

        # Validate inputs
        if not team_id:
            return jsonify({"error": "Team ID is required"}), 400

        logger.info(f"Generating commentary for team {team_id} with {commentator} in {language}")
        
        # Generate commentary
        text = generate_commentary(team_id, commentator, language)
        
        # Convert to speech
        audio_file = text_to_speech(text, language)
        
        if not audio_file:
            return jsonify({"error": "Failed to generate audio file"}), 500

        # Clean up old audio files periodically
        cleanup_audio_files()
        
        return jsonify({
            "text": text, 
            "audio": "/" + audio_file,
            "team_name": get_team_name(team_id)
        })
        
    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error generating commentary: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/static/<path:filename>")
def static_files(filename):
    """Serves static files like audio."""
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    logger.info("Starting AI Sports Commentator application...")
    app.run(debug=Config.FLASK_DEBUG, host='0.0.0.0', port=5000)
