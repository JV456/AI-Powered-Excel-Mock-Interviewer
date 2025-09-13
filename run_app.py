#!/usr/bin/env python3
"""
AI-Powered Excel Mock Interviewer Launcher

Simple launcher script for the Streamlit application.
"""

import os
import subprocess
import sys


def main():
    """Launch the Streamlit application."""
    try:
        # Change to the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Check which file to run
        if os.path.exists("app.py"):
            app_file = "app.py"
        elif os.path.exists("streamlit_app.py"):
            app_file = "streamlit_app.py"
        else:
            print("❌ Error: Could not find app.py or streamlit_app.py")
            sys.exit(1)
        
        print("🚀 Launching AI-Powered Excel Mock Interviewer...")
        print(f"📝 Running {app_file} - The application will open in your web browser")
        print("🔑 Make sure you have set your GROQ_API_KEY in the .env file")
        print("─" * 60)
        
        # Try to use the virtual environment streamlit
        venv_streamlit = os.path.join(script_dir, "venv", "Scripts", "streamlit.exe")
        if os.path.exists(venv_streamlit):
            print(f"Using virtual environment streamlit: {venv_streamlit}")
            subprocess.run([venv_streamlit, "run", app_file], check=True)
        else:
            # Fallback to system streamlit
            subprocess.run([sys.executable, "-m", "streamlit", "run", app_file], check=True)
        
    except KeyboardInterrupt:
        print("\n\n👋 Interview session ended. Good luck with your Excel skills!")
    except FileNotFoundError:
        print("❌ Error: Streamlit not found. Please install requirements:")
        print("   pip install -r requirements.txt")
        print("   Or try running directly: streamlit run app.py")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        print("💡 Try running directly: streamlit run app.py")
        sys.exit(1)


if __name__ == "__main__":
    main()