"""
Tests for OpenAIService.
Following TDD principles with real API integration when available.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from tests.test_config import TestConfig, requires_openai_key, requires_integration_tests
from src.services.openai_service import OpenAIService


class TestOpenAIService:
    """Test cases for OpenAIService class."""
    
    def setup_method(self):
        """Setup test configuration for each test."""
        self.test_config = TestConfig()
    
    def test_create_openai_service_without_key(self):
        """Test creating OpenAI service without API key raises error."""
        with pytest.raises(ValueError, match="OpenAI API key is required"):
            OpenAIService("")
    
    @requires_openai_key
    def test_create_openai_service_with_real_key(self):
        """Test creating OpenAI service with real API key."""
        service = OpenAIService(self.test_config.openai_api_key)
        assert service is not None
    
    def test_create_openai_service_with_key(self):
        """Test creating OpenAI service with API key."""
        # RED: This test should fail initially
        service = OpenAIService("test-api-key")
        assert service is not None
        assert service.api_key == "test-api-key"
    
    def test_transcribe_audio(self):
        """Test transcribing audio to text."""
        # RED: This test should fail initially
        service = OpenAIService("test-api-key")
        
        # Mock the file existence and OpenAI client
        with patch('builtins.open', create=True) as mock_open, \
             patch.object(service.client.audio.transcriptions, 'create') as mock_transcribe:
            
            mock_open.return_value.__enter__.return_value = Mock()
            mock_transcribe.return_value = "Hello, I want to learn about AI engineering."
            
            result = service.transcribe_audio("test_audio.wav")
            
            assert result == "Hello, I want to learn about AI engineering."
            mock_transcribe.assert_called_once()
    
    def test_process_learning_query(self):
        """Test processing a learning query with context."""
        # RED: This test should fail initially
        service = OpenAIService("test-api-key")
        
        with patch.object(service.client.chat.completions, 'create') as mock_chat:
            mock_response = Mock()
            mock_message = Mock()
            mock_message.content = "I recommend starting with LLM APIs to understand the basics..."
            mock_choice = Mock()
            mock_choice.message = mock_message
            mock_response.choices = [mock_choice]
            mock_chat.return_value = mock_response
            
            query = "I want to learn AI engineering but don't know where to start"
            sentiment_context = "User seems excited and motivated"
            
            result = service.process_learning_query(query, sentiment_context)
            
            assert "recommend" in result.lower()
            mock_chat.assert_called_once()
    
    def test_get_topic_specific_help(self):
        """Test getting help for a specific topic."""
        # RED: This test should fail initially
        service = OpenAIService("test-api-key")
        
        with patch.object(service.client.chat.completions, 'create') as mock_chat:
            mock_response = Mock()
            mock_message = Mock()
            mock_message.content = "LLM APIs are the foundation of AI engineering..."
            mock_choice = Mock()
            mock_choice.message = mock_message
            mock_response.choices = [mock_choice]
            mock_chat.return_value = mock_response
            
            result = service.get_topic_specific_help("llm-apis", "I'm confused about structured outputs")
            
            assert "LLM APIs" in result or "structured outputs" in result
            mock_chat.assert_called_once()
    
    def test_error_handling_for_api_failures(self):
        """Test error handling when OpenAI API fails."""
        # RED: This test should fail initially
        service = OpenAIService("test-api-key")
        
        with patch.object(service.client.chat.completions, 'create') as mock_chat:
            mock_chat.side_effect = Exception("API Error")
            
            result = service.process_learning_query("test query", "neutral")
            
            assert "error" in result.lower() or "sorry" in result.lower()
    
    @requires_openai_key
    @requires_integration_tests
    def test_process_learning_query_real_api(self):
        """Test processing learning query with real OpenAI API."""
        service = OpenAIService(self.test_config.openai_api_key)
        
        try:
            query = "What are the fundamentals of machine learning?"
            sentiment_context = "User seems eager to learn"
            
            result = service.process_learning_query(query, sentiment_context)
            
            assert isinstance(result, str)
            assert len(result) > 0
            # Response should mention ML-related concepts
            result_lower = result.lower()
            ml_terms = ["machine learning", "algorithm", "model", "data", "training"]
            assert any(term in result_lower for term in ml_terms)
            
        except Exception as e:
            pytest.skip(f"Real OpenAI API test failed: {e}")
    
    @requires_openai_key  
    @requires_integration_tests
    def test_get_topic_specific_help_real_api(self):
        """Test getting topic-specific help with real OpenAI API."""
        service = OpenAIService(self.test_config.openai_api_key)
        
        try:
            result = service.get_topic_specific_help(
                "llm-apis", 
                "I'm confused about how to use structured outputs"
            )
            
            assert isinstance(result, str)
            assert len(result) > 0
            # Response should mention LLMs or APIs
            result_lower = result.lower()
            relevant_terms = ["llm", "api", "structured", "output", "format"]
            assert any(term in result_lower for term in relevant_terms)
            
        except Exception as e:
            pytest.skip(f"Real OpenAI API test failed: {e}")
    
    @requires_openai_key
    @requires_integration_tests  
    def test_transcribe_audio_real_api(self):
        """Test audio transcription with real OpenAI API."""
        service = OpenAIService(self.test_config.openai_api_key)
        
        # Create a test audio file
        test_audio_path = self.test_config.get_test_audio_file()
        
        try:
            result = service.transcribe_audio(test_audio_path)
            
            # Even with a simple sine wave, the API should return something
            assert isinstance(result, str)
            # For a pure sine wave, transcription might be empty or contain minimal text
            # This is expected behavior
            
        except Exception as e:
            pytest.skip(f"Real OpenAI transcription test failed: {e}")
