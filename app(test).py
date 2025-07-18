import streamlit as st
import openai
import pandas as pd
from st_audiorecorder import st_audiorecorder
import os
from datetime import datetime

# --- App Configuration ---
st.set_page_config(page_title="Audio Translator", page_icon="🎤", layout="centered")

# --- OpenAI API Setup ---
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("OpenAI API key not found! Please add it to your Streamlit secrets.")
    st.stop()

# --- Data Storage Setup --
DATA_DIR = "audio_data"
LOG_FILE = "translations_log.csv"

# Create directories and files if they don't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(LOG_FILE):
    # Create the CSV file with headers if it doesn't exist
    pd.DataFrame(columns=[
        "timestamp", "location", "audio_filename",
        "original_transcription", "english_translation"
    ]).to_csv(LOG_FILE, index=False)

# --- Helper Functions ---

def transcribe_audio(audio_filepath):
    """Transcribes audio using OpenAI's Whisper model."""
    try:
        with open(audio_filepath, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="json"
            )
        return transcript.text
    except Exception as e:
        st.error(f"Error during transcription: {e}")
        return None

def translate_text_to_english(text):
    """Translates text to English using OpenAI's GPT model."""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that translates text to English."},
                {"role": "user", "content": f"Translate the following text to English: {text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error during translation: {e}")
        return None

def save_data(location, audio_filename, original_transcription, english_translation):
    """Saves the new data entry to the CSV log file."""
    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "location": location,
        "audio_filename": audio_filename,
        "original_transcription": original_transcription,
        "english_translation": english_translation
    }
    # Append the new entry to the CSV file
    entry_df = pd.DataFrame([new_entry])
    entry_df.to_csv(LOG_FILE, mode='a', header=False, index=False)


# --- Main Application UI ---

st.title("🎤 Audio Transcription and Translation App")
st.markdown("""
This app records your audio, transcribes it, and translates the transcription to English.
All data is stored locally for future reference.
""")

st.header("Step 1: Record Your Audio")
# The st_audiorecorder component returns audio data in bytes
audio_bytes = st_audiorecorder()

st.header("Step 2: Enter Your Location")
location = st.text_input("Your Location (e.g., 'Paris, France')", placeholder="Enter city and country")

st.header("Step 3: Process and Save")
if st.button("Translate and Store Data"):
    # --- Input Validation ---
    if audio_bytes is None:
        st.warning("Please record some audio first.")
    elif not location.strip():
        st.warning("Please enter your location.")
    else:
        with st.spinner("Processing your request... Please wait."):
            # 1. Save the recorded audio to a file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_filename = f"{timestamp}_{location.replace(' ', '_')}.wav"
            audio_filepath = os.path.join(DATA_DIR, audio_filename)

            with open(audio_filepath, "wb") as f:
                f.write(audio_bytes)
            
            st.success(f"Audio saved as `{audio_filepath}`")

            # 2. Transcribe the audio
            st.info("Transcribing audio...")
            transcription = transcribe_audio(audio_filepath)

            if transcription:
                st.subheader("Original Transcription:")
                st.write(transcription)

                # 3. Translate the transcription to English
                st.info("Translating text to English...")
                translation = translate_text_to_english(transcription)
                
                if translation:
                    st.subheader("English Translation:")
                    st.write(translation)
                    
                    # 4. Save all data to the log file
                    save_data(location, audio_filename, transcription, translation)
                    st.success("All data has been successfully stored!")
                else:
                    st.error("Could not get translation. Data not fully saved.")
            else:
                st.error("Could not get transcription. Data not saved.")


# --- Display Stored Data ---
st.divider()
st.header("📖 View Stored Data")

if st.checkbox("Show all collected data"):
    try:
        df = pd.read_csv(LOG_FILE)
        if df.empty:
            st.info("The data log is currently empty. Submit some data to see it here.")
        else:
            st.dataframe(df)
    except FileNotFoundError:
        st.info("The data log file does not exist yet. Submit some data to create it.")