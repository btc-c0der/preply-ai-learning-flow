"""
Tests for AudioSentimentService.
Following TDD principles - RED phase.
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch
from src.services.audio_sentiment_service import AudioSentimentService


class TestAudioSentimentService:
    """Test cases for AudioSentimentService class."""
    
    def test_create_audio_sentiment_service(self):
        """Test creating the audio sentiment service."""
        # RED: This test should fail initially
        service = AudioSentimentService()
        assert service is not None
    
    def test_analyze_audio_features(self):
        """Test analyzing audio features from file path."""
        # RED: This test should fail initially
        service = AudioSentimentService()
        
        # Mock audio data - simulate a typical audio waveform
        mock_audio = np.random.rand(22050)  # 1 second at 22050 Hz
        
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (mock_audio, 22050)
            
            features = service.analyze_audio_features("test_audio.wav")
            
            # Should return a dictionary with audio features
            assert isinstance(features, dict)
            assert "energy" in features
            assert "tempo" in features
            assert "spectral_centroid" in features
            assert "zero_crossing_rate" in features
            assert "mfccs" in features
    
    def test_predict_sentiment_from_features(self):
        """Test predicting sentiment from audio features."""
        # RED: This test should fail initially
        service = AudioSentimentService()
        
        # Mock audio features
        features = {
            "energy": 0.5,
            "tempo": 120.0,
            "spectral_centroid": 2000.0,
            "zero_crossing_rate": 0.1,
            "mfccs": np.random.rand(13)
        }
        
        sentiment = service.predict_sentiment_from_features(features)
        
        # Should return sentiment with confidence
        assert isinstance(sentiment, dict)
        assert "emotion" in sentiment
        assert "confidence" in sentiment
        assert "analysis" in sentiment
        assert sentiment["emotion"] in ["positive", "negative", "neutral", "excited", "calm", "stressed"]
    
    def test_analyze_audio_sentiment_end_to_end(self):
        """Test complete audio sentiment analysis."""
        # RED: This test should fail initially
        service = AudioSentimentService()
        
        mock_audio = np.random.rand(44100)  # 2 seconds at 22050 Hz
        
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (mock_audio, 22050)
            
            result = service.analyze_audio_sentiment("test_audio.wav")
            
            assert isinstance(result, dict)
            assert "sentiment" in result
            assert "features" in result
            assert "recommendation" in result
    
    def test_get_learning_recommendation_based_on_sentiment(self):
        """Test getting learning recommendations based on sentiment."""
        # RED: This test should fail initially
        service = AudioSentimentService()
        
        # Test different sentiments
        positive_rec = service.get_learning_recommendation("positive", 0.8)
        assert "positive" in positive_rec.lower() or "great" in positive_rec.lower() or "excellent" in positive_rec.lower()
        
        stressed_rec = service.get_learning_recommendation("stressed", 0.7)
        assert "stress" in stressed_rec.lower() or "calm" in stressed_rec.lower() or "breath" in stressed_rec.lower()
        
        excited_rec = service.get_learning_recommendation("excited", 0.9)
        assert "excited" in excited_rec.lower() or "energy" in excited_rec.lower() or "great" in excited_rec.lower()
