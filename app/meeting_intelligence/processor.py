"""
Meeting Intelligence implementation for audio processing, transcription, and analysis
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import spacy

# Ensure required NLTK packages are downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


class MeetingProcessor:
    """
    Process meeting recordings to extract transcripts, insights, and analytics
    """
    
    def __init__(self):
        """Initialize the meeting processor"""
        # Load the English language model for NLP processing
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            # If the model isn't installed, download it
            import subprocess
            subprocess.call([
                "python", "-m", "spacy", "download", "en_core_web_sm"
            ])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        
        # Initialize LLM for analysis
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            self.llm = OpenAI(api_key=openai_api_key)
        else:
            print("Warning: OPENAI_API_KEY not set. LLM functionality will be limited.")
            self.llm = None
    
    def process_recording(self, file_path: str) -> Dict[str, Any]:
        """
        Process a meeting recording end-to-end
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary containing processing results
        """
        # Convert audio to the format needed for speech recognition
        audio_segments = self._prepare_audio(file_path)
        
        # Transcribe the audio
        transcript, speaker_segments = self._transcribe_audio(audio_segments)
        
        # Analyze the transcript
        analysis = self._analyze_transcript(transcript, speaker_segments)
        
        # Generate a summary
        summary = self._generate_summary(transcript)
        
        # Extract action items
        action_items = self._extract_action_items(transcript)
        
        # Identify key topics
        topics = self._identify_topics(transcript)
        
        # Compile results
        results = {
            "transcript": transcript,
            "speaker_segments": speaker_segments,
            "analysis": analysis,
            "summary": summary,
            "action_items": action_items,
            "topics": topics,
            "processed_at": datetime.utcnow().isoformat()
        }
        
        return results
    
    def _prepare_audio(self, file_path: str) -> List[AudioSegment]:
        """
        Prepare audio for processing by converting format and splitting into segments
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            List of audio segments
        """
        try:
            # Load the audio file
            audio = AudioSegment.from_file(file_path)
            
            # Convert to mono if needed
            if audio.channels > 1:
                audio = audio.set_channels(1)
            
            # Set the sample rate to 16kHz for better speech recognition
            audio = audio.set_frame_rate(16000)
            
            # Split into 60-second segments for better processing
            segment_length = 60 * 1000  # 60 seconds in milliseconds
            segments = []
            
            for i in range(0, len(audio), segment_length):
                segment = audio[i:i + segment_length]
                segments.append(segment)
            
            return segments
        except Exception as e:
            print(f"Error preparing audio: {e}")
            return []
    
    def _transcribe_audio(self, audio_segments: List[AudioSegment]) -> tuple:
        """
        Transcribe audio segments to text
        
        Args:
            audio_segments: List of audio segments to transcribe
            
        Returns:
            Tuple of (full transcript, speaker segments)
        """
        transcript = ""
        speaker_segments = []
        
        try:
            for i, segment in enumerate(audio_segments):
                # Export segment to a temporary file
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    segment_path = temp_file.name
                    segment.export(segment_path, format="wav")
                
                # Transcribe the segment
                with sr.AudioFile(segment_path) as source:
                    audio_data = self.recognizer.record(source)
                    segment_text = self.recognizer.recognize_google(audio_data)
                
                # Clean up the temporary file
                os.unlink(segment_path)
                
                # Add to transcript
                if segment_text:
                    timestamp = i * 60  # 60 seconds per segment
                    formatted_timestamp = f"{timestamp // 60:02d}:{timestamp % 60:02d}"
                    
                    # For real speaker diarization, we would use a more sophisticated approach
                    # This is a placeholder that assumes speaker changes every segment
                    speaker = f"Speaker {(i % 3) + 1}"
                    
                    segment_info = {
                        "speaker": speaker,
                        "start_time": formatted_timestamp,
                        "text": segment_text
                    }
                    speaker_segments.append(segment_info)
                    
                    transcript += f"[{formatted_timestamp}] {speaker}: {segment_text}\n\n"
            
            return transcript, speaker_segments
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return "", []
    
    def _analyze_transcript(self, transcript: str, speaker_segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze the transcript for insights
        
        Args:
            transcript: Full meeting transcript
            speaker_segments: List of speaker segments
            
        Returns:
            Dictionary of analysis results
        """
        # Calculate speaker statistics
        speaker_stats = self._calculate_speaker_stats(speaker_segments)
        
        # Extract named entities
        entities = self._extract_entities(transcript)
        
        # Sentiment analysis
        sentiment = self._analyze_sentiment(transcript)
        
        # Extract key phrases
        key_phrases = self._extract_key_phrases(transcript)
        
        return {
            "speaker_stats": speaker_stats,
            "entities": entities,
            "sentiment": sentiment,
            "key_phrases": key_phrases
        }
    
    def _calculate_speaker_stats(self, speaker_segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics about speaker participation"""
        speakers = {}
        total_words = 0
        
        for segment in speaker_segments:
            speaker = segment["speaker"]
            text = segment["text"]
            words = len(word_tokenize(text))
            total_words += words
            
            if speaker in speakers:
                speakers[speaker]["segments"] += 1
                speakers[speaker]["words"] += words
            else:
                speakers[speaker] = {
                    "segments": 1,
                    "words": words
                }
        
        # Calculate percentages
        for speaker, stats in speakers.items():
            stats["contribution_percentage"] = round((stats["words"] / total_words) * 100, 2) if total_words > 0 else 0
        
        return speakers
    
    def _extract_entities(self, transcript: str) -> Dict[str, List[str]]:
        """Extract named entities from transcript"""
        doc = self.nlp(transcript)
        
        entities = {}
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            
            # Avoid duplicates
            if ent.text not in entities[ent.label_]:
                entities[ent.label_].append(ent.text)
        
        return entities
    
    def _analyze_sentiment(self, transcript: str) -> Dict[str, Any]:
        """Analyze sentiment in the transcript"""
        # In a real implementation, this would use a sentiment analysis model
        # This is a placeholder that returns neutral sentiment
        
        return {
            "overall": "neutral",
            "score": 0.0,
            "segments": []
        }
    
    def _extract_key_phrases(self, transcript: str) -> List[str]:
        """Extract key phrases from the transcript"""
        # Use TF-IDF to find important phrases
        sentences = sent_tokenize(transcript)
        
        if len(sentences) < 3:
            return []
        
        try:
            vectorizer = TfidfVectorizer(max_df=0.9, min_df=2, stop_words="english", ngram_range=(1, 3))
            X = vectorizer.fit_transform(sentences)
            
            # Get top terms
            feature_names = vectorizer.get_feature_names_out()
            scores = X.sum(axis=0).A1
            
            # Sort by score and get top 10
            top_indices = scores.argsort()[-10:][::-1]
            top_phrases = [feature_names[i] for i in top_indices]
            
            return top_phrases
        except Exception:
            return []
    
    def _generate_summary(self, transcript: str) -> str:
        """Generate a summary of the meeting"""
        if not self.llm:
            return "Summary generation requires OpenAI API key."
        
        # Use LangChain to generate summary
        try:
            summary_template = """
            Please provide a concise summary of this meeting transcript:
            
            {transcript}
            
            Summary (3-5 sentences):
            """
            
            prompt = PromptTemplate(
                input_variables=["transcript"],
                template=summary_template,
            )
            
            # Create and run the chain
            summary_chain = LLMChain(llm=self.llm, prompt=prompt)
            
            # Truncate transcript if it's too long
            max_len = 4000
            truncated_transcript = transcript[:max_len] if len(transcript) > max_len else transcript
            
            summary = summary_chain.run(truncated_transcript)
            return summary.strip()
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def _extract_action_items(self, transcript: str) -> List[Dict[str, Any]]:
        """Extract action items from the transcript"""
        if not self.llm:
            return []
        
        # Use LangChain to extract action items
        try:
            action_item_template = """
            Extract all action items from this meeting transcript. For each action item, identify:
            1. The task to be completed
            2. Who is assigned to do it (if mentioned)
            3. The due date (if mentioned)
            
            Return as JSON format with fields: text, assignee, due_date
            
            Transcript:
            {transcript}
            
            Action Items (JSON):
            """
            
            prompt = PromptTemplate(
                input_variables=["transcript"],
                template=action_item_template,
            )
            
            # Create and run the chain
            action_chain = LLMChain(llm=self.llm, prompt=prompt)
            
            # Truncate transcript if it's too long
            max_len = 4000
            truncated_transcript = transcript[:max_len] if len(transcript) > max_len else transcript
            
            result = action_chain.run(truncated_transcript)
            
            # Parse the JSON result
            try:
                # Find JSON in the response
                start_idx = result.find("[")
                end_idx = result.rfind("]")
                if start_idx >= 0 and end_idx >= 0:
                    json_str = result[start_idx:end_idx + 1]
                    action_items = json.loads(json_str)
                    return action_items
                return []
            except:
                return []
        except Exception as e:
            print(f"Error extracting action items: {e}")
            return []
    
    def _identify_topics(self, transcript: str) -> List[str]:
        """Identify main topics discussed in the meeting"""
        if not self.llm:
            return []
        
        # Use LangChain to identify topics
        try:
            topic_template = """
            Identify the 3-5 main topics discussed in this meeting transcript.
            Return them as a comma-separated list.
            
            Transcript:
            {transcript}
            
            Topics:
            """
            
            prompt = PromptTemplate(
                input_variables=["transcript"],
                template=topic_template,
            )
            
            # Create and run the chain
            topic_chain = LLMChain(llm=self.llm, prompt=prompt)
            
            # Truncate transcript if it's too long
            max_len = 4000
            truncated_transcript = transcript[:max_len] if len(transcript) > max_len else transcript
            
            result = topic_chain.run(truncated_transcript)
            
            # Parse the result
            topics = [topic.strip() for topic in result.split(",")]
            return topics
        except Exception as e:
            print(f"Error identifying topics: {e}")
            return []