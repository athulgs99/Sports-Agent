# AI Sports Commentator

An intelligent sports commentary generator that creates personalized audio commentary for recent sports games using AI.

## 🎙️ Features

- **AI-Powered Commentary**: Uses Groq's LLM to generate engaging sports commentary
- **Multiple Commentators**: Choose from Ravi Shastri, Harsha Bhogle, or Tony Romo
- **Multi-Language Support**: English, Hindi, and Spanish commentary
- **Text-to-Speech**: Converts commentary to audio using gTTS
- **Real Sports Data**: Fetches recent game scores from TheSportsDB API
- **Modern UI**: Beautiful, responsive interface with Tailwind CSS
- **Audio Management**: Automatic cleanup of old audio files

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Groq API key
- TheSportsDB API key (free)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/athulgs99/Sports-Agent.git
   cd Sports-Agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env_config.txt .env
   ```
   
   Edit `.env` and add your API keys:
   ```env
   SPORTS_API_KEY=123
   GROQ_API_KEY=your_groq_api_key_here
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎯 Usage

1. **Select a Commentator**: Choose from Ravi Shastri, Harsha Bhogle, or Tony Romo
2. **Choose a Team**: Enter a team ID or select from the provided options
3. **Select Language**: English, Hindi, or Spanish
4. **Generate Commentary**: Click the button to create AI-powered commentary
5. **Listen**: The commentary will be converted to speech and played automatically

## 🏗️ Project Structure

```
Sports-Agent/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── utils.py              # Core utility functions
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html       # Web interface
├── static/              # Generated audio files
├── README.md           # This file
└── .env                # Environment variables (not in repo)
```

## 🔧 Configuration

### Environment Variables

- `SPORTS_API_KEY`: TheSportsDB API key (get from [thesportsdb.com](https://www.thesportsdb.com/api.php))
- `GROQ_API_KEY`: Groq API key (get from [groq.com](https://console.groq.com/))
- `SECRET_KEY`: Flask secret key for sessions
- `FLASK_DEBUG`: Enable/disable debug mode

### API Keys

- **TheSportsDB**: Free API for sports data
- **Groq**: Fast LLM API for commentary generation

## 🛡️ Security

- API keys are stored in `.env` file (not committed to repository)
- Input validation on all user inputs
- Error handling for API failures
- Automatic cleanup of generated audio files

## 📝 Logging

The application logs all activities to `app.log`:
- API requests and responses
- Commentary generation
- Audio file creation
- Error messages

## 🐛 Troubleshooting

### Common Issues

1. **"No recent games found"**
   - Check if the team ID is valid
   - Verify your TheSportsDB API key

2. **"LLM error generating commentary"**
   - Verify your Groq API key
   - Check Groq service status

3. **Audio not playing**
   - Check browser audio settings
   - Verify gTTS installation

### Debug Mode

Enable debug mode in `.env`:
```env
FLASK_DEBUG=True
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for fast LLM API
- [TheSportsDB](https://www.thesportsdb.com/) for sports data
- [gTTS](https://gtts.readthedocs.io/) for text-to-speech
- [Flask](https://flask.palletsprojects.com/) for web framework
- [Tailwind CSS](https://tailwindcss.com/) for styling
