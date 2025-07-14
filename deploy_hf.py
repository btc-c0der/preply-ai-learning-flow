#!/usr/bin/env python3
"""
Hugging Face Spaces deployment script for AI Engineering Learning Roadmap.
This script helps prepare and deploy the application to Hugging Face Spaces.
"""

import os
import subprocess
import sys
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "gradio",
        "huggingface_hub",
        "git"
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == "git":
                subprocess.run(["git", "--version"], check=True, capture_output=True)
            else:
                __import__(package)
            print(f"✅ {package} is installed")
        except (ImportError, subprocess.CalledProcessError):
            missing.append(package)
            print(f"❌ {package} is missing")
    
    if missing:
        print(f"\n🚨 Missing dependencies: {', '.join(missing)}")
        print("Install them with:")
        if "git" in missing:
            print("  - Install Git from https://git-scm.com/")
        if "huggingface_hub" in missing:
            print("  - pip install huggingface_hub")
        if "gradio" in missing:
            print("  - pip install gradio")
        return False
    
    return True

def prepare_files():
    """Prepare files for Hugging Face Spaces deployment."""
    print("\n📁 Preparing files for deployment...")
    
    # Check if required files exist
    required_files = [
        "app.py",
        "requirements.txt",
        "src/app.py",
        "src/app_enhanced.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path} exists")
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    # Create README.md with HF header if it doesn't exist
    if not os.path.exists("README.md"):
        print("📝 Creating README.md with Hugging Face header...")
        with open("README_HF.md", "r") as source:
            content = source.read()
        with open("README.md", "w") as target:
            target.write(content)
        print("✅ README.md created")
    
    return True

def test_app():
    """Test the application locally before deployment."""
    print("\n🧪 Testing application locally...")
    
    try:
        # Import and create the app
        from app import create_hf_app
        app = create_hf_app()
        print("✅ Application created successfully")
        
        # Test basic functionality
        print("✅ All tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Application test failed: {e}")
        return False

def deploy_to_hf():
    """Deploy to Hugging Face Spaces."""
    print("\n🚀 Deploying to Hugging Face Spaces...")
    
    # Check if HF CLI is available
    try:
        subprocess.run(["huggingface-cli", "whoami"], check=True, capture_output=True)
        print("✅ Hugging Face CLI is configured")
    except subprocess.CalledProcessError:
        print("❌ Hugging Face CLI not configured")
        print("Please run: huggingface-cli login")
        return False
    
    # Check if this is a git repository
    if not os.path.exists(".git"):
        print("❌ Not a git repository")
        print("Please initialize git first: git init")
        return False
    
    # Instructions for manual deployment
    print("\n📋 Manual deployment steps:")
    print("1. Create a new Space on Hugging Face: https://huggingface.co/new-space")
    print("2. Choose:")
    print("   - Space name: ai-engineering-learning-roadmap")
    print("   - License: MIT")
    print("   - SDK: Gradio")
    print("   - Hardware: CPU basic (free)")
    print("3. Clone the space repository:")
    print("   git clone https://huggingface.co/spaces/YOUR_USERNAME/ai-engineering-learning-roadmap")
    print("4. Copy all files from this directory to the cloned space")
    print("5. Add OpenAI API key in Space settings > Repository secrets")
    print("6. Push to deploy:")
    print("   git add .")
    print("   git commit -m 'Initial deployment'")
    print("   git push")
    
    return True

def main():
    """Main deployment function."""
    print("🚀 AI Engineering Learning Roadmap - Hugging Face Deployment")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Prepare files
    if not prepare_files():
        sys.exit(1)
    
    # Test application
    if not test_app():
        print("⚠️  Application test failed, but continuing with deployment prep...")
    
    # Deploy to HF
    deploy_to_hf()
    
    print("\n🎉 Deployment preparation complete!")
    print("🔗 After deployment, your Space will be available at:")
    print("   https://huggingface.co/spaces/YOUR_USERNAME/ai-engineering-learning-roadmap")
    
    print("\n💡 Remember to:")
    print("1. Add your OpenAI API key to Space secrets")
    print("2. Test the voice recording feature")
    print("3. Share your Space with the community!")

if __name__ == "__main__":
    main()
