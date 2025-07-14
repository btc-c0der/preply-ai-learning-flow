#!/usr/bin/env python3
"""
Demonstration of the enhanced audio features with real OpenAI API integration.
"""

import os
from dotenv import load_dotenv
from src.services.openai_service import OpenAIService
from src.services.audio_sentiment_service import AudioSentimentService
from src.services.audio_ui_service import AudioUIService
from tests.test_config import TestConfig


def main():
    """Demonstrate the enhanced audio and AI features."""
    
    print("🎤 Enhanced AI Learning Roadmap - Audio Features Demo")
    print("=" * 60)
    
    # Load configuration
    load_dotenv()
    config = TestConfig()
    
    if not config.has_openai_key():
        print("❌ OpenAI API key not found in .env file")
        print("🔑 Please set OPENAI_API_KEY in your .env file to test audio features")
        return
    
    print("✅ OpenAI API key configured")
    
    # Initialize services
    print("\n📦 Initializing enhanced services...")
    openai_service = OpenAIService(config.openai_api_key)
    sentiment_service = AudioSentimentService()
    audio_ui_service = AudioUIService(openai_service, sentiment_service)
    
    # Test 1: Basic chatbot functionality
    print("\n🤖 Testing AI Learning Assistant...")
    test_query = "What are the key differences between supervised and unsupervised learning?"
    sentiment_context = "User seems eager to understand machine learning concepts"
    
    try:
        response = audio_ui_service.create_chatbot_response(test_query, sentiment_context)
        print(f"✅ AI Response generated successfully! ({len(response)} chars)")
        print("📝 Response preview:")
        print(f"   {response[:200]}...")
        
    except Exception as e:
        print(f"❌ AI Response test failed: {e}")
    
    # Test 2: Audio sentiment analysis
    print("\n🎵 Testing audio sentiment analysis...")
    try:
        # Create a test audio file
        test_audio_path = config.get_test_audio_file()
        print(f"📁 Using test audio file: {test_audio_path}")
        
        # Analyze sentiment
        sentiment_result = sentiment_service.analyze_audio_sentiment(test_audio_path)
        print("✅ Audio sentiment analysis completed!")
        print(f"📊 Result: {sentiment_result}")
        
    except Exception as e:
        print(f"❌ Audio sentiment analysis test failed: {e}")
    
    # Test 3: Topic-specific help
    print("\n🎯 Testing topic-specific AI assistance...")
    try:
        help_response = openai_service.get_topic_specific_help(
            "llm-apis", 
            "I'm having trouble understanding how to implement structured outputs with OpenAI's API"
        )
        print(f"✅ Topic help generated successfully! ({len(help_response)} chars)")
        print("📝 Help preview:")
        print(f"   {help_response[:200]}...")
        
    except Exception as e:
        print(f"❌ Topic help test failed: {e}")
    
    # Test 4: Audio transcription
    print("\n🎤 Testing audio transcription...")
    try:
        test_audio_path = config.get_test_audio_file()
        transcription = openai_service.transcribe_audio(test_audio_path)
        print(f"✅ Audio transcription completed!")
        print(f"📝 Transcription: '{transcription}'")
        if not transcription.strip():
            print("   (Empty transcription expected for pure sine wave test audio)")
        
    except Exception as e:
        print(f"❌ Audio transcription test failed: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 Enhanced Audio Features Demo Complete!")
    print()
    print("📊 Features demonstrated:")
    print("   ✅ AI-powered learning assistance")
    print("   ✅ Audio sentiment analysis")
    print("   ✅ Topic-specific help generation")
    print("   ✅ Audio transcription capabilities")
    print()
    print("🚀 Ready to run the full Gradio application with:")
    print("   python run.py")
    print()
    print("💡 The app will include:")
    print("   🎤 Live audio recording")
    print("   😊 Real-time sentiment analysis")
    print("   💬 Interactive AI chatbot")
    print("   📚 Personalized learning recommendations")


if __name__ == "__main__":
    main()
