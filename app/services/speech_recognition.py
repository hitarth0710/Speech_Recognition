import os
import time
import numpy as np
from flask import current_app
import librosa
import torch

# Global variables for lazy loading
_model = None
_processor = None

def _load_wav2vec2_model():
    """Load the Wav2Vec2 model from Hugging Face"""
    global _model, _processor
    
    if _model is None or _processor is None:
        try:
            from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
            
            # Use the model from exmple.py
            model_name = current_app.config.get('WAV2VEC2_MODEL', 'facebook/wav2vec2-large-960h-lv60-self')
            current_app.logger.info(f"Loading Wav2Vec2 model: {model_name}")
            
            start_time = time.time()
            _processor = Wav2Vec2Processor.from_pretrained(model_name)
            _model = Wav2Vec2ForCTC.from_pretrained(model_name)
            
            # Move model to GPU if available
            device = "cuda:0" if torch.cuda.is_available() else "cpu"
            _model = _model.to(device)
            
            current_app.logger.info(f"Model loaded in {time.time() - start_time:.2f} seconds")
            current_app.logger.info(f"Model is on device: {next(_model.parameters()).device}")
                
        except Exception as e:
            current_app.logger.error(f"Error loading Wav2Vec2 model: {str(e)}")
            raise RuntimeError(f"Failed to load the Wav2Vec2 model: {str(e)}")
    
    return _model, _processor

def transcribe_audio(audio_path):
    """
    Transcribe an audio file using the Wav2Vec2 model from Hugging Face.
    
    Args:
        audio_path: Path to the audio file
        
    Returns:
        str: Transcribed text
    """
    try:
        # Verify GPU status and log information
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            current_app.logger.info(f"CUDA is available with {gpu_count} GPU(s)")
            for i in range(gpu_count):
                current_app.logger.info(f"GPU {i}: {torch.cuda.get_device_name(i)}")
                current_app.logger.info(f"Memory: {torch.cuda.get_device_properties(i).total_memory / 1e9:.2f} GB")
            device = torch.device("cuda:0")
        else:
            current_app.logger.info("CUDA is not available. Using CPU instead.")
            device = torch.device("cpu")
        
        # Load the model
        model, processor = _load_wav2vec2_model()
        
        # Log loading audio
        current_app.logger.info(f"Loading audio file: {audio_path}")
        
        # Load and preprocess the audio
        audio, sampling_rate = librosa.load(audio_path, sr=16000)
        
        # Make sure audio is float32 numpy array
        audio = np.array(audio, dtype=np.float32)
        
        # Process the audio - convert to list first for safer processing as in exmple.py
        inputs = processor(
            audio.tolist(),  # Convert to list for more reliable processing
            sampling_rate=16000,
            return_tensors="pt",
            padding="longest"  # More explicit than padding=True
        )
        
        # Extract input values
        input_values = inputs.input_values
        
        # Move to GPU if available
        input_values = input_values.to(device)
        current_app.logger.info(f"Input data is on device: {input_values.device}")
        current_app.logger.info(f"Input shape: {input_values.shape}")
        
        current_app.logger.info("Processing audio...")
        start_inference = time.time()
        
        # Generate tokens with no grad for inference
        with torch.no_grad():
            logits = model(input_values).logits
        
        inference_time = time.time() - start_inference
        current_app.logger.info(f"Inference completed in {inference_time:.2f} seconds")
        
        # Get the predicted token ids
        predicted_ids = torch.argmax(logits, dim=-1)
        
        # Decode the tokens
        transcription = processor.batch_decode(predicted_ids)[0]
        
        current_app.logger.info(f"Transcription successful: {transcription[:30]}...")
        return transcription
        
    except Exception as e:
        import traceback
        current_app.logger.error(f"Error during transcription: {traceback.format_exc()}")
        return f"Error processing audio file: {str(e)}"

# Keep the recognize_speech function for backward compatibility
def recognize_speech(audio_file_path):
    """
    Legacy speech recognition function for compatibility with original app
    
    Args:
        audio_file_path: Path to the audio file
        
    Returns:
        str or None: Transcribed text or None if recognition failed
    """
    try:
        # Use the new transcribe_audio function
        return transcribe_audio(audio_file_path)
    except Exception as e:
        current_app.logger.error(f"Error in Wav2Vec2 transcription, trying fallback: {str(e)}")
        
        # Original implementation as fallback
        import speech_recognition as sr
        
        if not os.path.exists(audio_file_path):
            current_app.logger.error(f"Audio file not found: {audio_file_path}")
            return None

        recognizer = sr.Recognizer()

        try:
            with sr.AudioFile(audio_file_path) as source:
                # Adjust for ambient noise and record
                recognizer.adjust_for_ambient_noise(source)
                audio_data = recognizer.record(source)

                # Use the specified model for recognition
                text = recognizer.recognize_google(audio_data)

                current_app.logger.info(f"Speech recognition successful: {text[:30]}...")
                return text

        except sr.UnknownValueError:
            current_app.logger.warning(f"Speech could not be understood")
            return None
        except sr.RequestError as e:
            current_app.logger.error(f"Speech recognition service error: {str(e)}")
            return None
        except Exception as e:
            current_app.logger.error(f"Speech recognition unexpected error: {str(e)}")
            return None