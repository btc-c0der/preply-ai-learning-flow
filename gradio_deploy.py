#!/usr/bin/env python3
"""
Gradio Deploy Script for AI Engineering Learning Roadmap
Deploys to: https://huggingface.co/spaces/fartec0/ai-learning-path-audio-sentiment
"""

import os
import subprocess
import sys
from pathlib import Path

def check_gradio_cli():
    """Check if Gradio CLI is installed and working."""
    try:
        result = subprocess.run(["gradio", "--version"], capture_output=True, text=True, check=True)
        print(f"✅ Gradio CLI installed: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Gradio CLI not found")
        print("Install it with: pip install gradio[deploy]")
        return False

def check_hf_token():
    """Check if Hugging Face token is configured."""
    # Check environment variable
    hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")
    if hf_token:
        print("✅ Hugging Face token found in environment")
        return True
    
    # Check HF CLI
    try:
        subprocess.run(["huggingface-cli", "whoami"], capture_output=True, check=True)
        print("✅ Hugging Face CLI configured")
        return True
    except subprocess.CalledProcessError:
        print("❌ Hugging Face token not configured")
        print("Configure it with: huggingface-cli login")
        return False

def prepare_deployment():
    """Prepare files for deployment."""
    print("📁 Preparing deployment files...")
    
    # Check required files
    required_files = [
        "app.py",
        "requirements.txt",
        "README.md",
        "src/app.py",
        "src/repositories/roadmap_repository.py",
        "src/services/roadmap_service.py",
        "src/ui/gradio_ui_service.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def test_app_locally():
    """Test the application locally before deployment."""
    print("\n🧪 Testing application locally...")
    
    try:
        # Import and test the app
        from app import create_app
        app = create_app()
        print("✅ Application created successfully")
        return True
    except Exception as e:
        print(f"❌ Application test failed: {e}")
        return False

def deploy_to_hf():
    """Deploy to Hugging Face Spaces using gradio deploy."""
    print("\n🚀 Deploying to Hugging Face Spaces...")
    
    space_name = "fartec0/ai-learning-path-audio-sentiment"
    
    try:
        # Deploy using gradio deploy
        cmd = ["gradio", "deploy", "--space-id", space_name, "--hf-token", os.getenv("HUGGINGFACE_API_KEY", "")]
        
        print(f"🔄 Running: {' '.join(cmd[:-1])} [token]")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✅ Deployment successful!")
        print(f"🔗 Your Space is available at: https://huggingface.co/spaces/{space_name}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        print("Error output:", e.stderr)
        
        # Fallback instructions
        print("\n📋 Manual deployment alternative:")
        print("1. Run: gradio deploy")
        print("2. Follow the prompts to create/update your Space")
        print(f"3. Space URL: https://huggingface.co/spaces/{space_name}")
        
        return False

def main():
    """Main deployment function."""
    print("🚀 AI Engineering Learning Roadmap - Gradio Deploy")
    print("=" * 60)
    print(f"🎯 Target Space: https://huggingface.co/spaces/fartec0/ai-learning-path-audio-sentiment")
    print()
    
    # Check prerequisites
    if not check_gradio_cli():
        print("💡 Install with: pip install gradio[deploy]")
        return False
    
    if not check_hf_token():
        print("💡 Configure with: huggingface-cli login")
        print("   Or set HF_TOKEN environment variable")
        return False
    
    # Prepare deployment
    if not prepare_deployment():
        return False
    
    # Test locally
    if not test_app_locally():
        print("⚠️  Local test failed, but continuing with deployment...")
    
    # Deploy
    success = deploy_to_hf()
    
    if success:
        print("\n🎉 Deployment completed successfully!")
        print("📝 Next steps:")
        print("1. Visit your Space and test the audio recording feature")
        print("2. Add OpenAI API key to Space secrets if not already done")
        print("3. Share your Space with the community!")
        
        print("\n🔧 Space Configuration:")
        print("- OpenAI API Key: Add to Space secrets as 'OPENAI_API_KEY'")
        print("- Hardware: CPU Basic (free tier)")
        print("- Visibility: Public")
        
    else:
        print("\n❌ Deployment failed")
        print("Check the error messages above and try again")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
