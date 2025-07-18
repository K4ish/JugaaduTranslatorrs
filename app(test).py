import os

# ✅ Redirect cache to a writable directory
os.environ["XDG_CACHE_HOME"] = "/tmp/whisper-cache"

import streamlit as st
import datetime
import whisper
import geocoder
from pydub import AudioSegment
from io import BytesIO
from googletrans import Translator

# Page setup
st.set_page_config(page_title="🌍 Multilingual Transcriber", layout="centered")
st.title("🎙 Multilingual Audio Transcriber with Location + Metadata")

# Create writable recordings directory
RECORDINGS_DIR = "/tmp/recordings"
os.makedirs(RECORDINGS_DIR, exist_ok=True)

# Load whisper model
@st.cache_resource
def load_model():
    return whisper.load_model("base", download_root="/tmp/whisper-cache")

model = load_model()
translator = Translator()

# Upload audio
st.header("1. Upload Audio File")
audio_file = st.file_uploader("Upload your audio file (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])

if audio_file:
    st.audio(audio_file)

    # Convert to WAV
    audio = AudioSegment.from_file(audio_file).set_channels(1).set_frame_rate(16000)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"{timestamp}_{audio_file.name.split('.')[0]}"
    file_path = os.path.join(RECORDINGS_DIR, base_filename + ".wav")
    audio.export(file_path, format="wav")

    st.success(f"📁 Audio saved to `{file_path}`")

    # Transcribe
    st.header("2. Transcription")
    with st.spinner("Transcribing..."):
        result = model.transcribe(file_path)
        transcription = result["text"]
        detected_lang = result["language"]

    st.markdown(f"**🗣 Detected Language:** `{detected_lang.upper()}`")
    st.text_area("📄 Transcription", transcription, height=180)

    # Translate
    if detected_lang != "en":
        st.subheader("3. Translation to English")
        with st.spinner("Translating..."):
            translated = translator.translate(transcription, src=detected_lang, dest="en").text
        st.text_area("🌐 English Translation", translated, height=180)
    else:
        translated = transcription

    # Metadata
    st.subheader("4. Metadata Generation")
    def generate_metadata(text):
        title = f"Audio Note - {text[:10]}..."
        description = f"This recording discusses: {text[:100]}..."
        return title, description

    title, description = generate_metadata(translated)
    st.write(f"**📌 Title:** {title}")
    st.write(f"**🧾 Description:** {description}")

    # Location
    st.subheader("5. Approximate Location")
    try:
        g = geocoder.ip("me")
        coords = f"{g.latlng[0]}, {g.latlng[1]}" if g.latlng else "Unknown"
        if g.latlng:
            st.map(data={"lat": [g.latlng[0]], "lon": [g.latlng[1]]})
        st.success(f"📍 Coordinates: {coords}")
    except:
        st.warning("Unable to determine location.")

    # Summary
    st.subheader("✅ Summary")
    st.markdown(f"""
    - **File Name:** `{base_filename}.wav`
    - **Language:** `{detected_lang.upper()}`
    - **Title:** {title}
    - **Location:** {coords if 'coords' in locals(
