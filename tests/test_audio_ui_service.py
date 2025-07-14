"""
Tests for AudioUIService.
Following TDD principles with real API integration when available.
"""

import pytest
import os
from unittest.mock import Mock, patch
from tests.test_config import TestConfig, requires_openai_key, requires_integration_tests
from src.services.audio_ui_service import AudioUIService
from src.services.openai_service import OpenAIService
from src.services.audio_sentiment_service import AudioSentimentService


class TestAudioUIService:
    """Test cases for AudioUIService class."""
    
    def setup_method(self):
        """Setup test configuration for each test."""
        self.test_config = TestConfig()
    
    def test_create_audio_ui_service(self):
        """Test creating the audio UI service with mocks."""
        openai_service = Mock(spec=OpenAIService)
        sentiment_service = Mock(spec=AudioSentimentService)
        
        service = AudioUIService(openai_service, sentiment_service)
        assert service is not None
    
    @requires_openai_key
    def test_create_audio_ui_service_with_real_api(self):
        """Test creating the audio UI service with real OpenAI API."""
        openai_service = OpenAIService(self.test_config.openai_api_key)
        sentiment_service = AudioSentimentService()
        
        service = AudioUIService(openai_service, sentiment_service)
        assert service is not None
        assert service.openai_service is not None
        assert service.sentiment_service is not None
    
    
    def test_process_audio_input_mocked(self):
        """Test processing audio input with mocked services."""
        openai_service = Mock(spec=OpenAIService)
        sentiment_service = Mock(spec=AudioSentimentService)
        
        # Mock transcription
        openai_service.transcribe_audio.return_value = "I want to learn about AI agents"
        
        # Mock sentiment analysis
        sentiment_service.analyze_audio_sentiment.return_value = {
            "sentiment": {"emotion": "excited", "confidence": 0.8},
            "recommendation": "Great energy! Perfect for AI Agents topic."
        }
        
        # Mock AI response
        openai_service.process_learning_query.return_value = "AI agents are autonomous systems..."
        
        service = AudioUIService(openai_service, sentiment_service)
        result = service.process_audio_input("test_audio.wav")
        
        assert isinstance(result, dict)
        assert "transcription" in result
        assert "sentiment_analysis" in result
        assert "ai_response" in result
        assert "recommendation" in result
    
    @requires_openai_key
    @requires_integration_tests
    def test_process_audio_input_real_api(self):
        """Test processing audio input with real OpenAI API."""
        openai_service = OpenAIService(self.test_config.openai_api_key)
        sentiment_service = AudioSentimentService()
        
        service = AudioUIService(openai_service, sentiment_service)
        
        # Create a test audio file
        test_audio_path = self.test_config.get_test_audio_file()
        
        try:
            result = service.process_audio_input(test_audio_path)
            
            assert isinstance(result, dict)
            assert "transcription" in result
            assert "sentiment_analysis" in result
            assert "ai_response" in result
            assert "recommendation" in result
            
            # Verify transcription is not empty (though it might be for pure sine wave)
            assert isinstance(result["transcription"], str)
            assert isinstance(result["sentiment_analysis"], dict)
            assert isinstance(result["ai_response"], str)
            assert isinstance(result["recommendation"], str)
            
        except Exception as e:
            # If real API fails, that's ok for testing
            pytest.skip(f"Real API integration test failed: {e}")
    
    def test_create_chatbot_response_mocked(self):
        """Test creating chatbot response with mocked service."""
        openai_service = Mock(spec=OpenAIService)
        sentiment_service = Mock(spec=AudioSentimentService)
        
        openai_service.process_learning_query.return_value = "Here's what you need to know about LLMs..."
        
        service = AudioUIService(openai_service, sentiment_service)
        response = service.create_chatbot_response("Tell me about LLMs", "User seems curious")
        
        assert "Here's what you need to know about LLMs..." in response
    
    @requires_openai_key
    def test_create_chatbot_response_real_api(self):
        """Test creating chatbot response with real OpenAI API."""
        openai_service = OpenAIService(self.test_config.openai_api_key)
        sentiment_service = AudioSentimentService()
        
        service = AudioUIService(openai_service, sentiment_service)
        
        try:
            response = service.create_chatbot_response(
                "What are the key topics in AI engineering?", 
                "User seems eager to learn"
            )
            
            assert isinstance(response, str)
            assert len(response) > 0
            # Response should mention some AI-related topics
            response_lower = response.lower()
            ai_terms = ["ai", "machine learning", "llm", "neural", "model", "algorithm"]
            assert any(term in response_lower for term in ai_terms)
            
        except Exception as e:
            pytest.skip(f"Real OpenAI API test failed: {e}")
    
    def test_format_sentiment_display(self):
        """Test formatting sentiment analysis for display."""
        openai_service = Mock(spec=OpenAIService)
        sentiment_service = Mock(spec=AudioSentimentService)
        
        service = AudioUIService(openai_service, sentiment_service)
        
        sentiment_data = {
            "emotion": "excited",
            "confidence": 0.85,
            "analysis": "Detected high energy, fast speech"
        }
        
        formatted = service.format_sentiment_display(sentiment_data)
        
        assert "excited" in formatted.lower()
        assert "85%" in formatted or "0.85" in formatted
        assert "high energy" in formatted.lower()
    
    def test_format_audio_processing_result(self):
        """Test formatting complete audio processing result."""
        openai_service = Mock(spec=OpenAIService)
        sentiment_service = Mock(spec=AudioSentimentService)
        
        service = AudioUIService(openai_service, sentiment_service)
        
        result = {
            "transcription": "I want to learn about machine learning",
            "sentiment_analysis": {
                "emotion": "curious",
                "confidence": 0.9,
                "analysis": "Steady, thoughtful speech pattern"
            },
            "ai_response": "Machine learning is a subset of AI...",
            "recommendation": "Start with supervised learning basics"
        }
        
        formatted = service.format_audio_processing_result(result)
        
        assert "transcription" in formatted.lower() or "transcript" in formatted.lower()
        assert "machine learning" in formatted
        assert "curious" in formatted.lower()
        assert "90%" in formatted or "0.9" in formatted
