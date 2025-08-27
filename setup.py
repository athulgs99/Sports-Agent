#!/usr/bin/env python3
"""
Setup script for AI Sports Commentator
Run with: python setup.py
"""

import os
import sys

def create_env_file():
    """Create a .env file with template values."""
    env_content = """# AI Sports Commentator Environment Variables
# Copy this file to .env and fill in your actual values

# API Keys (Required)
SPORTS_API_KEY=your_sports_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-to-something-secure
FLASK_ENV=development
FLASK_DEBUG=True

# Optional: Custom port (default is 5000)
# PORT=5000
"""
    
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Skipping creation.")
        return
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file template")
    print("📝 Please edit .env file with your actual API keys")

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask',
        'requests', 
        'groq',
        'gtts',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'python-dotenv':
                import dotenv
            else:
                __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Install missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def create_directories():
    """Create necessary directories."""
    directories = ['static', 'templates']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created {directory}/ directory")
        else:
            print(f"✅ {directory}/ directory already exists")

def main():
    """Main setup function."""
    print("🚀 AI Sports Commentator Setup\n")
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    print("\n📋 Next Steps:")
    print("1. Edit .env file with your API keys")
    print("2. Get API keys from:")
    print("   - TheSportsDB: https://www.thesportsdb.com/api.php")
    print("   - Groq: https://console.groq.com/")
    print("3. Run: python app.py")
    print("4. Open: http://localhost:5000")
    
    if not deps_ok:
        print("\n⚠️  Please install missing dependencies before running the app")
        sys.exit(1)
    
    print("\n🎉 Setup complete! You're ready to start commentating!")

if __name__ == "__main__":
    main()
