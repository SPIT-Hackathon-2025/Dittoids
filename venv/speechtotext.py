import streamlit as st
from audio_recorder_streamlit import audio_recorder
import assemblyai as aai
import io
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set AssemblyAI API Key
aai.settings.api_key = os.getenv("ASSEMBLY_API_KEY")

def transcribe_audio(audio_data):
    audio_io = io.BytesIO(audio_data)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_io)
    
    if transcript.status == aai.TranscriptStatus.error:
        return f"Transcription failed: {transcript.error}"
    return transcript.text

def main():
    st.title("Audio Recorder and Transcription")

    # Record audio for a fixed duration of 10 seconds
    audio_bytes = audio_recorder(
        energy_threshold=(-1.0, 1.0),
        pause_threshold=10.0,
        sample_rate=41000,
        text="",
        recording_color="#e8b62c",
        neutral_color="#6aa36f",
        icon_name="microphone",
        icon_size="6x"
    )

    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        st.success("Recording completed!")

        # Store the audio in a variable
        audio_data = audio_bytes

        # Display the audio data
        st.write("Audio data stored in variable:")

        # Transcribe the audio data
        transcript_text = transcribe_audio(audio_data)
        st.subheader("Transcription:")
        st.write(transcript_text)

if __name__ == "__main__":
    main()