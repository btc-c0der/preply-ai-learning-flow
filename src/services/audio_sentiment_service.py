"""
Audio sentiment analysis service using audio wave analysis.
Analyzes audio features to determine emotional state and provides learning recommendations.
"""

import numpy as np
import librosa
from typing import Dict, Any, Tuple
import os


class AudioSentimentService:
    """
    Service for analyzing sentiment from audio features.
    
    Single Responsibility: Handles audio analysis and sentiment prediction.
    Uses audio wave characteristics like energy, tempo, spectral features.
    """
    
    def __init__(self):
        """Initialize the audio sentiment service."""
        self.sample_rate = 22050
        self.sentiment_thresholds = {
            "energy_high": 0.02,
            "energy_low": 0.005,
            "tempo_fast": 140,
            "tempo_slow": 80,
            "zcr_high": 0.15,
            "zcr_low": 0.05
        }
    
    def analyze_audio_features(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Extract audio features from an audio file.
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Dictionary containing audio features
        """
        try:
            # Load audio file
            y, sr = librosa.load(audio_file_path, sr=self.sample_rate)
            
            # Extract features
            features = {}
            
            # Energy (RMS)
            rms = librosa.feature.rms(y=y)[0]
            features["energy"] = float(np.mean(rms))
            
            # Tempo
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            features["tempo"] = float(tempo)
            
            # Spectral centroid (brightness)
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            features["spectral_centroid"] = float(np.mean(spectral_centroids))
            
            # Zero crossing rate (voice quality indicator)
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            features["zero_crossing_rate"] = float(np.mean(zcr))
            
            # MFCCs (Mel-frequency cepstral coefficients)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            features["mfccs"] = np.mean(mfccs, axis=1)
            
            # Additional features
            features["duration"] = float(len(y) / sr)
            features["pitch_variance"] = float(np.var(spectral_centroids))
            
            return features
            
        except ImportError as e:
            if 'aifc' in str(e):
                # Handle Python 3.13 aifc module removal - use fallback
                return self._extract_basic_features_fallback(audio_file_path)
            else:
                raise e
        except Exception as e:
            raise RuntimeError(f"Error analyzing audio features: {str(e)}")
    
    def _extract_basic_features_fallback(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Fallback feature extraction for environments without full audio support.
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Dictionary of basic features
        """
        try:
            # Try to load with soundfile instead
            import soundfile as sf
            data, samplerate = sf.read(audio_file_path)
            
            # Extract very basic features
            features = {
                'duration': len(data) / samplerate,
                'energy': float(np.mean(np.abs(data))),
                'spectral_centroid': 1000.0,  # Default value
                'zero_crossing_rate': float(np.sum(np.diff(np.signbit(data))) / len(data)),
                'tempo': 120.0,  # Default tempo
                'pitch_variance': 100.0,  # Default variance
                'mfccs': np.zeros(13),  # Dummy MFCCs
            }
            
            return features
            
        except Exception as e:
            # Last resort: return mock features based on file characteristics
            import os
            file_size = os.path.getsize(audio_file_path)
            return {
                'duration': min(file_size / 44100, 10.0),  # Estimate duration
                'energy': 0.5,  # Default energy
                'spectral_centroid': 1000.0,
                'zero_crossing_rate': 0.1,
                'tempo': 120.0,
                'pitch_variance': 100.0,
                'mfccs': np.zeros(13),
            }
    
    def predict_sentiment_from_features(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict sentiment based on audio features.
        
        Args:
            features: Dictionary of audio features
            
        Returns:
            Dictionary containing sentiment prediction
        """
        energy = features["energy"]
        tempo = features["tempo"]
        zcr = features["zero_crossing_rate"]
        spectral_centroid = features["spectral_centroid"]
        pitch_variance = features.get("pitch_variance", 0)
        
        # Sentiment analysis based on audio characteristics
        sentiment_scores = {
            "excited": 0.0,
            "positive": 0.0,
            "neutral": 0.0,
            "calm": 0.0,
            "stressed": 0.0,
            "negative": 0.0
        }
        
        # Energy-based analysis
        if energy > self.sentiment_thresholds["energy_high"]:
            sentiment_scores["excited"] += 0.3
            sentiment_scores["positive"] += 0.2
        elif energy < self.sentiment_thresholds["energy_low"]:
            sentiment_scores["calm"] += 0.3
            sentiment_scores["negative"] += 0.1
        else:
            sentiment_scores["neutral"] += 0.2
        
        # Tempo-based analysis
        if tempo > self.sentiment_thresholds["tempo_fast"]:
            sentiment_scores["excited"] += 0.25
            sentiment_scores["stressed"] += 0.15
        elif tempo < self.sentiment_thresholds["tempo_slow"]:
            sentiment_scores["calm"] += 0.25
            sentiment_scores["negative"] += 0.1
        else:
            sentiment_scores["positive"] += 0.2
            sentiment_scores["neutral"] += 0.15
        
        # Zero crossing rate (voice stability)
        if zcr > self.sentiment_thresholds["zcr_high"]:
            sentiment_scores["stressed"] += 0.2
            sentiment_scores["excited"] += 0.1
        elif zcr < self.sentiment_thresholds["zcr_low"]:
            sentiment_scores["calm"] += 0.2
            sentiment_scores["positive"] += 0.1
        
        # Spectral centroid (brightness/energy)
        if spectral_centroid > 3000:
            sentiment_scores["excited"] += 0.15
            sentiment_scores["positive"] += 0.1
        elif spectral_centroid < 1500:
            sentiment_scores["calm"] += 0.15
            sentiment_scores["negative"] += 0.05
        
        # Pitch variance (emotional expressiveness)
        if pitch_variance > 1000000:
            sentiment_scores["excited"] += 0.1
            sentiment_scores["stressed"] += 0.1
        elif pitch_variance < 100000:
            sentiment_scores["calm"] += 0.1
            sentiment_scores["neutral"] += 0.1
        
        # Normalize scores
        total_score = sum(sentiment_scores.values())
        if total_score > 0:
            sentiment_scores = {k: v/total_score for k, v in sentiment_scores.items()}
        
        # Get dominant emotion
        dominant_emotion = max(sentiment_scores.items(), key=lambda x: x[1])
        emotion = dominant_emotion[0]
        confidence = dominant_emotion[1]
        
        # Create analysis text
        analysis_parts = []
        if energy > self.sentiment_thresholds["energy_high"]:
            analysis_parts.append("high energy")
        elif energy < self.sentiment_thresholds["energy_low"]:
            analysis_parts.append("low energy")
        
        if tempo > self.sentiment_thresholds["tempo_fast"]:
            analysis_parts.append("fast speech")
        elif tempo < self.sentiment_thresholds["tempo_slow"]:
            analysis_parts.append("slow speech")
        
        if zcr > self.sentiment_thresholds["zcr_high"]:
            analysis_parts.append("variable tone")
        
        analysis = f"Detected {', '.join(analysis_parts) if analysis_parts else 'moderate characteristics'}"
        
        return {
            "emotion": emotion,
            "confidence": confidence,
            "scores": sentiment_scores,
            "analysis": analysis
        }
    
    def get_learning_recommendation(self, emotion: str, confidence: float) -> str:
        """
        Get learning recommendations based on detected emotion.
        
        Args:
            emotion: Detected emotion
            confidence: Confidence level
            
        Returns:
            Personalized learning recommendation
        """
        recommendations = {
            "excited": [
                "Great energy! This is perfect for tackling challenging topics like AI Agents or Infrastructure.",
                "Your enthusiasm is awesome! Consider diving into complex topics like RAG systems.",
                "Amazing energy! Perfect time to explore advanced topics like Multi-agent systems."
            ],
            "positive": [
                "Positive attitude detected! Good time for structured learning like LLM APIs.",
                "Great mindset! Consider working through the Model Adaptation topics.",
                "Excellent mood for learning! Try the Storage for Retrieval section."
            ],
            "calm": [
                "Nice calm energy! Perfect for detailed topics like Security or Observability.",
                "Great focus detected! Ideal for reading documentation and resources.",
                "Calm and focused! Perfect for deep-diving into theoretical concepts."
            ],
            "neutral": [
                "Steady state! Good for any topic in the roadmap. Consider your prerequisites.",
                "Balanced energy! Great for methodical progress through the learning path.",
                "Good baseline! Perfect for reviewing previous topics or starting new ones."
            ],
            "stressed": [
                "Take a breath! Maybe start with easier topics or review familiar material.",
                "Detected some tension. Consider shorter learning sessions or basic concepts.",
                "Stress detected. Try starting with overview materials or taking a break."
            ],
            "negative": [
                "Tough day? Consider light review or motivational content about AI careers.",
                "Low energy detected. Maybe watch some inspiring AI demos or success stories.",
                "Not feeling it? Try exploring the 'Forward looking elements' for inspiration."
            ]
        }
        
        emotion_recs = recommendations.get(emotion, recommendations["neutral"])
        
        # Add confidence-based modifier
        if confidence > 0.7:
            confidence_modifier = " (High confidence in this assessment)"
        elif confidence > 0.5:
            confidence_modifier = " (Moderate confidence)"
        else:
            confidence_modifier = " (Low confidence - this is just a suggestion)"
        
        import random
        return random.choice(emotion_recs) + confidence_modifier
    
    def analyze_audio_sentiment(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Complete audio sentiment analysis pipeline.
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Complete analysis results
        """
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
        
        # Extract features
        features = self.analyze_audio_features(audio_file_path)
        
        # Predict sentiment
        sentiment = self.predict_sentiment_from_features(features)
        
        # Get recommendation
        recommendation = self.get_learning_recommendation(
            sentiment["emotion"], 
            sentiment["confidence"]
        )
        
        return {
            "sentiment": sentiment,
            "features": features,
            "recommendation": recommendation
        }
