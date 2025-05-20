import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import librosa
import os
import time
import numpy as np


def transcribe_audio(audio_path):
    """
    Transcribe an audio file using the Wav2Vec2 model from Hugging Face.
    Includes detailed GPU verification.

    Args:
        audio_path (str): Path to the audio file to transcribe

    Returns:
        str: Transcribed text
    """
    print("\n===== GPU VERIFICATION =====")
    # Check if CUDA is available
    if torch.cuda.is_available():
        gpu_count = torch.cuda.device_count()
        print(f"✅ CUDA is available with {gpu_count} GPU(s)")
        for i in range(gpu_count):
            print(f"   GPU {i}: {torch.cuda.get_device_name(i)}")
            print(f"   Memory: {torch.cuda.get_device_properties(i).total_memory / 1e9:.2f} GB")

        # Set device to the first GPU
        device = torch.device("cuda:0")
    else:
        print("❌ CUDA is not available. Using CPU instead.")
        print("   To use GPU, ensure you have CUDA installed and a compatible GPU.")
        device = torch.device("cpu")

    print("==========================\n")

    print(f"Loading Wav2Vec2 model from 'facebook/wav2vec2-large-960h-lv60-self'...")
    start_time = time.time()

    # Load model and processor for English
    model_name = "facebook/wav2vec2-large-960h-lv60-self"
    processor = Wav2Vec2Processor.from_pretrained(model_name)
    model = Wav2Vec2ForCTC.from_pretrained(model_name)

    # Move model to device
    model = model.to(device)

    # Verify model is on correct device
    print(f"Model loaded in {time.time() - start_time:.2f} seconds")
    print(f"Model is on device: {next(model.parameters()).device}")

    print(f"Loading audio file: {audio_path}")

    # Load and preprocess the audio
    try:
        # Load audio using librosa
        audio, sampling_rate = librosa.load(audio_path, sr=16000)

        # Make sure audio is float32 numpy array
        audio = np.array(audio, dtype=np.float32)

        # Process the audio - explicitly convert to list first for safer processing
        # This changes how we call the processor to avoid the padding error
        inputs = processor(
            audio.tolist(),  # Convert to list for more reliable processing
            sampling_rate=16000,
            return_tensors="pt",
            padding="longest"  # Changed from padding=True to be more explicit
        )

        # Extract input values
        input_values = inputs.input_values

        # Move input data to device
        input_values = input_values.to(device)
        print(f"Input data is on device: {input_values.device}")
        print(f"Input shape: {input_values.shape}")  # Debug info

        print("Processing audio...")
        start_inference = time.time()

        # Get logits from the model
        with torch.no_grad():
            logits = model(input_values).logits

        inference_time = time.time() - start_inference
        print(f"Inference completed in {inference_time:.2f} seconds")

        # Get the predicted token ids
        predicted_ids = torch.argmax(logits, dim=-1)

        # Decode the token ids to get the transcription
        transcription = processor.batch_decode(predicted_ids)[0]

        return transcription

    except Exception as e:
        import traceback
        traceback.print_exc()  # Print full error for debugging
        return f"Error processing audio file: {str(e)}"


def save_transcription(transcription, output_path=None):
    """
    Save the transcription to a file.

    Args:
        transcription (str): The transcribed text
        output_path (str, optional): Path to save the transcription. If None, will ask for input.
    """
    if output_path is None:
        save_option = input("Do you want to save the transcription to a file? (y/n): ").lower()
        if save_option == 'y':
            output_path = input("Enter the path to save the transcription: ")
        else:
            return

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcription)
        print(f"Transcription saved to {output_path}")
    except Exception as e:
        print(f"Error saving transcription to file: {str(e)}")


if __name__ == "__main__":
    print("Wav2Vec2 Audio Transcription Tool")
    print("-" * 50)

    # Check if PyTorch was built with CUDA
    print(f"PyTorch version: {torch.__version__}")
    print(f"PyTorch built with CUDA: {torch.backends.cudnn.enabled}")

    # Manual input for audio path
    while True:
        audio_path = input("Enter the path to the audio file: ")

        # Check if file exists
        if os.path.isfile(audio_path):
            break
        else:
            print(f"Error: File '{audio_path}' does not exist. Please enter a valid path.")

    transcription = transcribe_audio(audio_path)

    print("\nTranscription:")
    print("-" * 50)
    print(transcription)
    print("-" * 50)

    # Ask user if they want to save the transcription
    save_transcription(transcription)