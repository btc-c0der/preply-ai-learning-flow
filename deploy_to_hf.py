#!/usr/bin/env python3
"""
Direct deployment script for Hugging Face Spaces
Uses HF Hub API to deploy to https://huggingface.co/spaces/fartec0/ai-learning-path-audio-sentiment
"""

import os
import subprocess
import sys
from pathlib import Path
import shutil

def setup_deployment():
    """Set up the deployment environment."""
    print("🚀 Setting up deployment for HF Spaces...")
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("❌ Not in a git repository. Initializing...")
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'config', 'user.email', 'deployment@example.com'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'Deployment Bot'], check=True)
    
    # Create .gitignore if it doesn't exist
    if not os.path.exists('.gitignore'):
        with open('.gitignore', 'w') as f:
            f.write("""
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Environment files
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Audio files
*.wav
*.mp3
*.m4a
*.flac
temp_audio*

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# HF Spaces
flagged/
""")
    
    print("✅ Git repository setup complete")

def prepare_files():
    """Prepare files for deployment."""
    print("📁 Preparing files for deployment...")
    
    # Ensure all required files exist
    required_files = {
        'app.py': 'Main application file',
        'requirements.txt': 'Dependencies file',
        'README.md': 'Documentation with HF header',
        'src/app.py': 'Source application',
        'src/services/audio_sentiment_service.py': 'Audio sentiment service'
    }
    
    missing_files = []
    for file_path, description in required_files.items():
        if os.path.exists(file_path):
            print(f"✅ {file_path} - {description}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path} - {description} (MISSING)")
    
    if missing_files:
        print(f"\n❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present")
    return True

def deploy_to_hf_space():
    """Deploy to the specific HF Space."""
    space_url = "https://huggingface.co/spaces/fartec0/ai-learning-path-audio-sentiment"
    
    print(f"🚀 Deploying to {space_url}")
    
    # Check if HF CLI is installed and configured
    try:
        result = subprocess.run(['huggingface-cli', 'whoami'], capture_output=True, text=True, check=True)
        username = result.stdout.strip()
        print(f"✅ Logged in as: {username}")
    except subprocess.CalledProcessError:
        print("❌ Please login to Hugging Face CLI first:")
        print("   huggingface-cli login")
        return False
    except FileNotFoundError:
        print("❌ Hugging Face CLI not found. Install it with:")
        print("   pip install huggingface-hub")
        return False
    
    # Clone the space repository
    space_dir = "hf_space_temp"
    if os.path.exists(space_dir):
        shutil.rmtree(space_dir)
    
    try:
        print("📥 Cloning HF Space repository...")
        subprocess.run([
            'git', 'clone', 
            'https://huggingface.co/spaces/fartec0/ai-learning-path-audio-sentiment',
            space_dir
        ], check=True)
        
        # Copy files to the space directory
        print("📋 Copying files to space...")
        files_to_copy = [
            'app.py',
            'requirements.txt', 
            'README.md',
            'src/',
            '.gitignore'
        ]
        
        for item in files_to_copy:
            src_path = Path(item)
            dst_path = Path(space_dir) / item
            
            if src_path.is_file():
                shutil.copy2(src_path, dst_path)
                print(f"✅ Copied {item}")
            elif src_path.is_dir():
                if dst_path.exists():
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, dst_path)
                print(f"✅ Copied {item}/ directory")
        
        # Change to space directory and commit
        os.chdir(space_dir)
        
        print("📦 Committing changes...")
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Check if there are changes to commit
        result = subprocess.run(['git', 'diff', '--cached', '--quiet'], capture_output=True)
        if result.returncode != 0:
            subprocess.run([
                'git', 'commit', '-m', 
                'Deploy AI Learning Path with Audio Sentiment Analysis'
            ], check=True)
            
            print("🚀 Pushing to Hugging Face Space...")
            subprocess.run(['git', 'push'], check=True)
            
            print("✅ Deployment successful!")
            print(f"🌐 Your Space is available at: {space_url}")
            
        else:
            print("ℹ️  No changes to deploy")
        
        # Clean up
        os.chdir('..')
        shutil.rmtree(space_dir)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False

def main():
    """Main deployment function."""
    print("🚀 AI Learning Path - HF Spaces Deployment")
    print("=" * 60)
    
    # Setup deployment environment
    setup_deployment()
    
    # Prepare files
    if not prepare_files():
        sys.exit(1)
    
    # Deploy to HF Space
    if deploy_to_hf_space():
        print("\n🎉 Deployment completed successfully!")
        print("💡 Next steps:")
        print("1. Go to https://huggingface.co/spaces/fartec0/ai-learning-path-audio-sentiment")
        print("2. Add your OPENAI_API_KEY to Space secrets")
        print("3. Test the voice recording feature")
        print("4. Share your Space with the community!")
    else:
        print("\n❌ Deployment failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
