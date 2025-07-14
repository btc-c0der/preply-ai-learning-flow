#!/bin/bash
# Pre-build script for Hugging Face Spaces
# Install system dependencies for audio processing

echo "🔧 Installing system dependencies for audio processing..."

# Update package list
apt-get update

# Install ffmpeg for audio processing
apt-get install -y ffmpeg

# Install additional audio libraries
apt-get install -y libsndfile1 libsndfile1-dev

# Install portaudio for potential microphone support
apt-get install -y portaudio19-dev

echo "✅ System dependencies installed successfully!"
