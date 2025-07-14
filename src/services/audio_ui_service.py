"""
Audio UI service for handling audio input, sentiment analysis, and chatbot integration.
Coordinates between audio processing, sentiment analysis, and OpenAI services.
"""

from typing import Dict, Any, Optional, Tuple
import os
import tempfile
from src.services.openai_service import OpenAIService
from src.services.audio_sentiment_service import AudioSentimentService


class AudioUIService:
    """
    Service for handling audio UI interactions.
    
    Single Responsibility: Coordinates audio processing with AI services.
    Dependency Inversion: Depends on OpenAI and AudioSentiment service abstractions.
    """
    
    def __init__(self, openai_service: OpenAIService, sentiment_service: AudioSentimentService):
        """
        Initialize the audio UI service.
        
        Args:
            openai_service: Service for OpenAI API interactions
            sentiment_service: Service for audio sentiment analysis
        """
        self.openai_service = openai_service
        self.sentiment_service = sentiment_service
    
    def process_audio_input(self, audio_file_path: str, user_progress: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process audio input through the complete pipeline.
        
        Args:
            audio_file_path: Path to the recorded audio file
            user_progress: Optional user progress information
            
        Returns:
            Complete processing results
        """
        try:
            # Step 1: Transcribe audio to text
            transcription = self.openai_service.transcribe_audio(audio_file_path)
            
            # Step 2: Analyze sentiment from audio
            sentiment_analysis = self.sentiment_service.analyze_audio_sentiment(audio_file_path)
            
            # Step 3: Create sentiment context for AI
            sentiment_context = self._create_sentiment_context(sentiment_analysis)
            
            # Step 4: Get AI response with context
            ai_response = self.openai_service.process_learning_query(
                transcription, 
                sentiment_context, 
                user_progress
            )
            
            # Step 5: Compile results
            return {
                "transcription": transcription,
                "sentiment_analysis": sentiment_analysis,
                "ai_response": ai_response,
                "recommendation": sentiment_analysis.get("recommendation", ""),
                "success": True
            }
            
        except Exception as e:
            return {
                "transcription": "",
                "sentiment_analysis": {},
                "ai_response": f"Sorry, I encountered an error processing your audio: {str(e)}",
                "recommendation": "Please try recording again or check your microphone.",
                "success": False
            }
    
    def create_chatbot_response(self, message: str, sentiment_context: str = "", user_progress: Optional[Dict] = None) -> str:
        """
        Create a chatbot response for text input.
        
        Args:
            message: User's text message
            sentiment_context: Optional sentiment context
            user_progress: Optional user progress information
            
        Returns:
            AI-generated response
        """
        try:
            return self.openai_service.process_learning_query(message, sentiment_context, user_progress)
        except Exception as e:
            return f"I'm having trouble responding right now: {str(e)}. Please try again."
    
    def get_topic_help(self, topic_id: str, question: str) -> str:
        """
        Get specific help for a learning topic.
        
        Args:
            topic_id: ID of the learning topic
            question: User's specific question
            
        Returns:
            Topic-specific guidance
        """
        try:
            return self.openai_service.get_topic_specific_help(topic_id, question)
        except Exception as e:
            return f"I'm having trouble accessing topic help: {str(e)}. Please try again."
    
    def format_sentiment_display(self, sentiment_data: Dict[str, Any]) -> str:
        """
        Format sentiment analysis results for display.
        
        Args:
            sentiment_data: Sentiment analysis results
            
        Returns:
            HTML-formatted sentiment display
        """
        emotion = sentiment_data.get("emotion", "unknown")
        confidence = sentiment_data.get("confidence", 0.0)
        analysis = sentiment_data.get("analysis", "No analysis available")
        
        # Emotion to emoji mapping
        emotion_emojis = {
            "excited": "🚀",
            "positive": "😊",
            "calm": "😌",
            "neutral": "😐",
            "stressed": "😰",
            "negative": "😔"
        }
        
        emoji = emotion_emojis.get(emotion, "🤔")
        confidence_pct = f"{confidence * 100:.0f}%"
        
        # Color coding based on emotion
        emotion_colors = {
            "excited": "#FF6B35",
            "positive": "#4CAF50", 
            "calm": "#2196F3",
            "neutral": "#9E9E9E",
            "stressed": "#FF9800",
            "negative": "#F44336"
        }
        
        color = emotion_colors.get(emotion, "#9E9E9E")
        
        return f"""
        <div class="sentiment-display" style="background: linear-gradient(135deg, {color}20, {color}10); 
             border-left: 4px solid {color}; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <h4 style="margin: 0 0 10px 0; color: {color};">
                {emoji} Detected Emotion: {emotion.title()}
            </h4>
            <div style="margin-bottom: 8px;">
                <strong>Confidence:</strong> {confidence_pct}
            </div>
            <div style="margin-bottom: 8px;">
                <strong>Analysis:</strong> {analysis}
            </div>
            <div class="confidence-bar" style="background: #e0e0e0; border-radius: 10px; overflow: hidden; height: 6px;">
                <div style="background: {color}; height: 100%; width: {confidence_pct}; transition: width 0.3s ease;"></div>
            </div>
        </div>
        """
    
    def format_audio_response(self, processing_result: Dict[str, Any]) -> Tuple[str, str, str]:
        """
        Format the complete audio processing result for UI display.
        
        Args:
            processing_result: Complete processing result
            
        Returns:
            Tuple of (transcription_html, sentiment_html, response_html)
        """
        if not processing_result.get("success", False):
            error_msg = processing_result.get("ai_response", "Unknown error")
            return (
                f"<div class='error'>❌ {error_msg}</div>",
                "<div class='error'>❌ Could not analyze sentiment</div>",
                f"<div class='error'>❌ {error_msg}</div>"
            )
        
        # Format transcription
        transcription = processing_result.get("transcription", "")
        transcription_html = f"""
        <div class="transcription" style="background: #f0f8ff; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <h4 style="margin: 0 0 10px 0; color: #1976d2;">🎤 What you said:</h4>
            <p style="margin: 0; font-style: italic;">"{transcription}"</p>
        </div>
        """
        
        # Format sentiment
        sentiment_data = processing_result.get("sentiment_analysis", {}).get("sentiment", {})
        sentiment_html = self.format_sentiment_display(sentiment_data)
        
        # Format AI response
        ai_response = processing_result.get("ai_response", "")
        recommendation = processing_result.get("recommendation", "")
        
        response_html = f"""
        <div class="ai-response" style="background: #f9f9f9; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <h4 style="margin: 0 0 10px 0; color: #388e3c;">🤖 AI Learning Assistant:</h4>
            <p style="margin: 0 0 15px 0; line-height: 1.6;">{ai_response}</p>
            {f'<div class="recommendation" style="background: #e8f5e8; padding: 10px; border-radius: 6px; border-left: 3px solid #4caf50;"><strong>💡 Recommendation:</strong> {recommendation}</div>' if recommendation else ''}
        </div>
        """
        
        return transcription_html, sentiment_html, response_html
    
    def format_audio_processing_result(self, result: Dict[str, Any]) -> str:
        """
        Format the complete audio processing result for display.
        
        Args:
            result: Dictionary containing processing results
            
        Returns:
            HTML-formatted string for display
        """
        transcription = result.get("transcription", "")
        sentiment_analysis = result.get("sentiment_analysis", {})
        ai_response = result.get("ai_response", "")
        recommendation = result.get("recommendation", "")
        
        # Format sentiment info
        emotion = sentiment_analysis.get("emotion", "neutral")
        confidence = sentiment_analysis.get("confidence", 0.0)
        confidence_pct = f"{confidence * 100:.0f}%"
        
        formatted_result = f"""
        <div class="audio-processing-result">
            <h3>🎙️ Audio Processing Complete</h3>
            
            <div class="transcription-section">
                <h4>📝 Transcription:</h4>
                <p>"{transcription}"</p>
            </div>
            
            <div class="sentiment-section">
                <h4>😊 Sentiment Analysis:</h4>
                <p>Emotion: <strong>{emotion}</strong> (Confidence: {confidence_pct})</p>
            </div>
            
            <div class="response-section">
                <h4>🤖 AI Response:</h4>
                <p>{ai_response}</p>
            </div>
            
            {f'<div class="recommendation-section"><h4>💡 Recommendation:</h4><p>{recommendation}</p></div>' if recommendation else ''}
        </div>
        """
        
        return formatted_result
    
    def _create_sentiment_context(self, sentiment_analysis: Dict[str, Any]) -> str:
        """
        Create sentiment context string for AI processing.
        
        Args:
            sentiment_analysis: Sentiment analysis results
            
        Returns:
            Formatted sentiment context
        """
        sentiment = sentiment_analysis.get("sentiment", {})
        emotion = sentiment.get("emotion", "neutral")
        confidence = sentiment.get("confidence", 0.0)
        analysis = sentiment.get("analysis", "")
        
        return f"User's emotional state: {emotion} (confidence: {confidence:.2f}). Audio analysis: {analysis}"
