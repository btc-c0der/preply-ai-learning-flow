#!/usr/bin/env python3
"""
AI Engineering Learning Roadmap - Hugging Face Spaces Entry Point
Voice-powered learning with sentiment analysis and AI guidance.
Deployment: https://huggingface.co/spaces/fartec0/ai-learning-path-audio-sentiment
"""

import os
import sys
import gradio as gr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_app():
    """
    Create the main application for Hugging Face Spaces deployment.
    
    Returns:
        Gradio Interface object
    """
    try:
        # Try to import and create the enhanced app with audio features
        from src.app import create_gradio_app
        
        # Check for OpenAI API key
        openai_key = os.getenv("OPENAI_API_KEY", "")
        
        if openai_key:
            print("✅ OpenAI API Key found - Creating app with full AI features")
        else:
            print("⚠️ No OpenAI API Key - Some features will be limited")
            
        app = create_gradio_app()
        print("✅ Application created successfully")
        return app
        
    except Exception as e:
        print(f"❌ Error creating application: {e}")
        
        # Create a fallback error interface
        with gr.Blocks(title="AI Learning Roadmap - Error") as error_app:
            gr.Markdown("# ❌ Application Error")
            gr.Markdown(f"**Error:** {str(e)}")
            gr.Markdown("""
            ## 🔧 Possible Solutions:
            1. Check that all dependencies are installed
            2. Verify OpenAI API key is configured
            3. Ensure all source files are present
            4. Check the application logs for more details
            """)
            
            gr.Markdown("## 📞 Support")
            gr.Markdown("If this error persists, please check the repository or contact support.")
        
        return error_app

# Create the main application instance
app = create_app()

if __name__ == "__main__":
    # Launch configuration for Hugging Face Spaces
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # HF Spaces handles sharing
        debug=False,  # Disable debug in production
        show_error=True
    )
