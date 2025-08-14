import speech_recognition as sr
from pydub import AudioSegment
import os
import tempfile
import logging
from typing import Dict, Any, Optional
from textblob import TextBlob
import numpy as np

logger = logging.getLogger(__name__)


class AudioProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.supported_formats = ['.wav', '.mp3', '.m4a', '.flac']
    
    def process_audio_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process audio file and extract transcription and analysis
        """
        try:
            # Validate file format
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in self.supported_formats:
                raise ValueError(f"Unsupported audio format: {file_ext}")
            
            # Convert to WAV if needed
            wav_path = self._convert_to_wav(file_path)
            
            # Extract audio features
            audio_features = self._extract_audio_features(wav_path)
            
            # Transcribe audio
            transcription = self._transcribe_audio(wav_path)
            
            # Analyze tone and sentiment
            tone_analysis = self._analyze_tone(transcription)
            
            # Clean up temporary file
            if wav_path != file_path:
                os.remove(wav_path)
            
            return {
                "transcription": transcription,
                "audio_features": audio_features,
                "tone_analysis": tone_analysis,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error processing audio file: {e}")
            return {
                "transcription": "",
                "audio_features": {},
                "tone_analysis": {},
                "success": False,
                "error": str(e)
            }
    
    def _convert_to_wav(self, file_path: str) -> str:
        """
        Convert audio file to WAV format for processing
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.wav':
            return file_path
        
        # Convert to WAV
        audio = AudioSegment.from_file(file_path)
        temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        audio.export(temp_wav.name, format='wav')
        
        return temp_wav.name
    
    def _extract_audio_features(self, wav_path: str) -> Dict[str, Any]:
        """
        Extract audio features like duration, volume, etc.
        """
        try:
            audio = AudioSegment.from_wav(wav_path)
            
            # Calculate features
            duration_ms = len(audio)
            duration_seconds = duration_ms / 1000
            
            # Calculate average volume
            samples = np.array(audio.get_array_of_samples())
            if audio.channels == 2:
                samples = samples.reshape((-1, 2))
            
            volume_db = audio.dBFS
            volume_linear = 10 ** (volume_db / 20)
            
            # Calculate speech rate (approximate)
            # This is a rough estimate based on average words per minute
            word_count = len(samples) // 16000  # Rough estimate
            speech_rate = word_count / (duration_seconds / 60) if duration_seconds > 0 else 0
            
            return {
                "duration_seconds": duration_seconds,
                "duration_ms": duration_ms,
                "volume_db": volume_db,
                "volume_linear": volume_linear,
                "sample_rate": audio.frame_rate,
                "channels": audio.channels,
                "speech_rate_estimate": speech_rate
            }
            
        except Exception as e:
            logger.error(f"Error extracting audio features: {e}")
            return {}
    
    def _transcribe_audio(self, wav_path: str) -> str:
        """
        Transcribe audio to text using speech recognition
        """
        try:
            with sr.AudioFile(wav_path) as source:
                audio = self.recognizer.record(source)
                
            # Use Google Speech Recognition
            transcription = self.recognizer.recognize_google(audio)
            return transcription
            
        except sr.UnknownValueError:
            logger.warning("Speech recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return ""
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return ""
    
    def _analyze_tone(self, text: str) -> Dict[str, Any]:
        """
        Analyze tone and sentiment of transcribed text
        """
        if not text.strip():
            return {
                "sentiment": "neutral",
                "sentiment_score": 0.0,
                "confidence": 0.0,
                "clarity_score": 0.0,
                "professionalism_score": 0.0
            }
        
        try:
            # Use TextBlob for sentiment analysis
            blob = TextBlob(text)
            sentiment_score = blob.sentiment.polarity
            sentiment_subjectivity = blob.sentiment.subjectivity
            
            # Determine sentiment category
            if sentiment_score > 0.1:
                sentiment = "positive"
            elif sentiment_score < -0.1:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            # Calculate clarity score (based on sentence structure)
            sentences = blob.sentences
            avg_sentence_length = np.mean([len(sentence.words) for sentence in sentences]) if sentences else 0
            
            # Clarity score based on sentence length (optimal: 15-20 words)
            if 10 <= avg_sentence_length <= 25:
                clarity_score = 1.0
            elif 5 <= avg_sentence_length <= 30:
                clarity_score = 0.8
            else:
                clarity_score = 0.5
            
            # Professionalism score (based on word choice and structure)
            professional_words = [
                "experience", "responsibility", "leadership", "collaboration",
                "achievement", "solution", "strategy", "implementation",
                "analysis", "development", "management", "coordination"
            ]
            
            text_lower = text.lower()
            professional_word_count = sum(1 for word in professional_words if word in text_lower)
            total_words = len(text.split())
            professionalism_score = min(1.0, professional_word_count / max(total_words, 1) * 10)
            
            return {
                "sentiment": sentiment,
                "sentiment_score": sentiment_score,
                "sentiment_subjectivity": sentiment_subjectivity,
                "clarity_score": clarity_score,
                "professionalism_score": professionalism_score,
                "avg_sentence_length": avg_sentence_length,
                "total_words": total_words,
                "professional_word_count": professional_word_count
            }
            
        except Exception as e:
            logger.error(f"Error analyzing tone: {e}")
            return {
                "sentiment": "neutral",
                "sentiment_score": 0.0,
                "sentiment_subjectivity": 0.0,
                "clarity_score": 0.0,
                "professionalism_score": 0.0,
                "avg_sentence_length": 0,
                "total_words": 0,
                "professional_word_count": 0
            }
    
    def calculate_tone_score(self, tone_analysis: Dict[str, Any]) -> float:
        """
        Calculate overall tone score based on analysis
        """
        try:
            # Weighted combination of different factors
            clarity_weight = 0.3
            professionalism_weight = 0.4
            sentiment_weight = 0.3
            
            clarity_score = tone_analysis.get("clarity_score", 0.0)
            professionalism_score = tone_analysis.get("professionalism_score", 0.0)
            sentiment_score = abs(tone_analysis.get("sentiment_score", 0.0))  # Use absolute value
            
            # Calculate weighted score
            tone_score = (
                clarity_score * clarity_weight +
                professionalism_score * professionalism_weight +
                sentiment_score * sentiment_weight
            )
            
            return min(100.0, tone_score * 100)  # Convert to 0-100 scale
            
        except Exception as e:
            logger.error(f"Error calculating tone score: {e}")
            return 0.0
