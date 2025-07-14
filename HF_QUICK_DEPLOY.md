# Hugging Face Spaces Deployment Guide

Quick guide for deploying this application to Hugging Face Spaces.

## Step 1: Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Select:
   - SDK: Gradio
   - Space hardware: CPU (Free)
   - Click "Create Space"

## Step 2: Add OpenAI API Key

1. Go to Space settings → Repository secrets
2. Add secret:
   - Name: OPENAI_API_KEY
   - Value: (your OpenAI API key)

## Step 3: Prepare Files

1. Rename `requirements-hf.txt` to `requirements.txt`
2. Rename `README-HF.md` to `README.md` (optional)
3. Ensure `app.py` is at the root level

## Step 4: Upload Files

1. Use the Files tab to upload all files
2. Maintain the directory structure
3. Wait for the build to complete

## Step 5: Verify Deployment

1. Test the application after build completes
2. Check for any errors in the Factory logs

## Troubleshooting

- Make sure OPENAI_API_KEY is set correctly
- Check for any dependency issues in the logs
- Verify that port 7860 is used in app.py
