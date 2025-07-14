# 🚀 Hugging Face Spaces Deployment Guide

This guide will help you deploy the AI Engineering Learning Roadmap to Hugging Face Spaces.

## 📋 Prerequisites

1. **Hugging Face Account**: Create account at [huggingface.co](https://huggingface.co)
2. **OpenAI API Key** (optional): Get from [OpenAI Platform](https://platform.openai.com/account/api-keys)
3. **Git** installed on your system

## 🔧 Deployment Steps

### 1. Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Fill in the details:
   - **Space name**: `ai-engineering-roadmap` (or your preferred name)
   - **License**: MIT
   - **Select the SDK**: Gradio
   - **Hardware**: CPU Basic (free tier)
   - **Visibility**: Public

### 2. Clone and Prepare Repository

```bash
# Clone your new space
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# Copy the prepared files from this project
cp /path/to/this/project/app.py .
cp /path/to/this/project/requirements.txt .
cp /path/to/this/project/packages.txt .
cp /path/to/this/project/pre-build.sh .
cp -r /path/to/this/project/src/ .
```

### 3. Essential Files for HF Spaces

Your space should have these files:

```
📁 YOUR_SPACE_NAME/
├── 📄 app.py                 # Main entry point (✅ Ready)
├── 📄 requirements.txt       # Python dependencies (✅ Ready)
├── 📄 packages.txt          # System packages (✅ Ready)
├── 📄 pre-build.sh          # Pre-build script (✅ Ready)
├── 📄 README.md             # Space description (✅ Ready)
├── 📁 src/                  # Source code
│   ├── 📁 services/
│   ├── 📁 repositories/
│   ├── 📁 ui/
│   ├── 📄 app_enhanced.py
│   └── 📄 app.py
└── 📁 .git/
```

### 4. Configure Environment Variables (Optional)

To enable AI features:

1. Go to your Space settings
2. Navigate to **"Repository secrets"**
3. Add new secret:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key

### 5. Deploy

```bash
# Add and commit files
git add .
git commit -m "🚀 Initial deployment of AI Engineering Learning Roadmap"

# Push to deploy
git push origin main
```

## 🎯 Post-Deployment

### Monitor Build Process

1. Go to your Space page on Hugging Face
2. Watch the **"Building"** logs in real-time
3. Look for:
   ✅ System packages installation (ffmpeg, audio libs)
   ✅ Python packages installation  
   ✅ App startup without errors

### Test Features

1. **Basic Features** (always available):
   - Learning Path Explorer
   - Topic Explorer  
   - Progress Tracker

2. **AI Features** (with API key):
   - Audio Recording & Sentiment Analysis
   - AI Chatbot
   - Topic-Specific Help
   - AI-Generated Study Guides

## 🔍 Troubleshooting

### Common Issues

#### 1. Build Fails - Audio Dependencies
**Error**: `Failed to install audio libraries`
**Solution**: Ensure `packages.txt` includes:
```
ffmpeg
libsndfile1
portaudio19-dev
```

#### 2. App Doesn't Start
**Error**: `Application failed to launch`
**Solutions**:
- Check `app.py` is in root directory
- Verify `requirements.txt` has correct dependencies
- Check logs for specific error messages

#### 3. Audio Features Not Working
**Error**: `Audio recording fails`
**Solutions**:
- Verify OpenAI API key is set in repository secrets
- Check browser permissions for microphone access
- Ensure hardware supports audio (CPU Basic should work)

#### 4. Import Errors
**Error**: `ModuleNotFoundError`
**Solutions**:
- Check all source files are in `src/` directory
- Verify `requirements.txt` includes all dependencies
- Ensure Python path includes project root

### Performance Optimization

#### For CPU Basic (Free Tier):
- ✅ Audio processing optimized for CPU
- ✅ Lightweight model loading
- ✅ Efficient memory usage
- ✅ Fallback modes for heavy operations

#### For Better Performance:
- Upgrade to **CPU Upgraded** for faster audio processing
- Consider **GPU** if adding speech synthesis features

## 📊 Space Configuration

### README.md Header
Your space will automatically use the header from `README_HF.md`:

```yaml
title: AI Engineering Learning Roadmap
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.9.1
app_file: app.py
pinned: false
license: mit
```

### Hardware Requirements

| Feature | CPU Basic | CPU Upgraded | GPU |
|---------|-----------|--------------|-----|
| Basic Learning Roadmap | ✅ | ✅ | ✅ |
| Audio Recording | ✅ | ✅ | ✅ |
| Sentiment Analysis | ✅ | ✅ | ✅ |
| OpenAI Integration | ✅ | ✅ | ✅ |
| Multiple Users | ⚠️ | ✅ | ✅ |

## 🎉 Success Checklist

After deployment, verify:

- [ ] Space builds successfully without errors
- [ ] App loads and displays welcome page
- [ ] All tabs are accessible
- [ ] Basic features work (learning paths, progress tracking)
- [ ] Audio recording interface appears (even without API key)
- [ ] AI features work when API key is provided
- [ ] Mobile responsive design works
- [ ] No console errors in browser

## 🔗 Useful Links

- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Gradio Documentation](https://gradio.app/docs/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Project Repository](https://github.com/YOUR_USERNAME/YOUR_REPO)

## 💡 Next Steps

After successful deployment:

1. **Share your Space**: Get the public URL and share with learners
2. **Monitor Usage**: Check analytics in HF Spaces dashboard
3. **Iterate**: Based on user feedback, enhance features
4. **Community**: Engage with the Hugging Face community

---

**🚀 Ready to deploy? Follow the steps above and you'll have your AI Engineering Learning Roadmap live on Hugging Face Spaces!**
