import streamlit as st
import json
import os
import geocoder
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googletrans import Translator

# --- Configuration ---
DB_FILE = "phrases_db.json"
GSHEET_CREDS = "your_credentials.json"  # Replace with your Google service account JSON file
GSHEET_NAME = "Jugaadu_Translations"    # Replace with your Google Sheet name

# --- Google Sheets Append ---
def append_to_gsheet(local, english, location, source_lang=None, title=None, description=None):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GSHEET_CREDS, scope)
    client = gspread.authorize(creds)
    sheet = client.open(GSHEET_NAME).sheet1
    sheet.append_row([
        title or "Untitled",
        description or "No description provided.",
        local,
        english,
        location,
        source_lang or "N/A"
    ])

# --- Title & Description Generation ---
def generate_title_description(local_phrase, english_translation):
    title = f"Meaning of '{local_phrase[:20].capitalize()}'"
    description = f"'{local_phrase}' means \"{english_translation}\" in standard English."
    return title, description

# --- Load & Save Local DB ---
def load_database():
    if not os.path.exists(DB_FILE):
        initial_data = {
            "kaisa hai?": "How are you?",
            "sab theek hai": "Everything is fine.",
            "tuition laga lo": "Get a tutor / Start tuition classes.",
            "timepass kar raha hoon": "I'm just passing time.",
            "panga mat le": "Don't mess with me.",
            "oye!": "Hey!",
            "chalega": "It will work / That's acceptable."
        }
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=4)
        return initial_data
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_database(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- App Setup ---
st.set_page_config(page_title="Jugaadu Translator", page_icon="💡", layout="centered")
phrases_db = load_database()
translator = Translator()

# --- Geolocation ---
location_info = geocoder.ip('me')
user_location = f"{location_info.city}, {location_info.country}" if location_info.city else "Unknown"

# --- Sidebar Navigation ---
st.sidebar.header("Choose a mode")
mode = st.sidebar.radio("What do you want to do?", (
    'Translate a Phrase',
    'Contribute a New Phrase',
    '🎙 Auto Speech Translator'
))

# --- Auto Speech Translator Mode ---
if mode == '🎙 Auto Speech Translator':
    st.title("🎙 Automatic Speech Translator")

    audio_file = st.file_uploader("Upload audio (wav/mp3/m4a)", type=["wav", "mp3", "m4a"])
    if audio_file:
        st.audio(audio_file)

        try:
            audio = AudioSegment.from_file(audio_file).set_channels(1).set_frame_rate(16000)
            with BytesIO() as buf:
                audio.export(buf, format="wav")
                buf.seek(0)

                recognizer = sr.Recognizer()
                with sr.AudioFile(buf) as source:
                    audio_data = recognizer.record(source)
                    spoken_text = recognizer.recognize_google(audio_data)

                st.success(f"🎤 Detected Speech: {spoken_text}")

                detected_lang = translator.detect(spoken_text).lang
                translated_text = translator.translate(spoken_text, dest='en').text

                st.info(f"🌍 Detected Language: {detected_lang}")
                st.success(f"🗣 Translation: {translated_text}")

                title, description = generate_title_description(spoken_text, translated_text)

                append_to_gsheet(
                    local=spoken_text,
                    english=translated_text,
                    location=user_location,
                    source_lang=detected_lang,
                    title=title,
                    description=description
                )

                st.success(f"✅ Title: {title}")
                st.caption(description)
                st.balloons()

        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError:
            st.error("Speech recognition service failed.")
        except Exception as e:
            st.error(f"Error: {e}")

# --- Translate Mode ---
elif mode == 'Translate a Phrase':
    st.title("🔄 Translate")

    direction = st.radio("Translation direction:", (
        'Local Dialect → Standard English',
        'Standard English → Local Dialect'
    ))

    if direction.startswith('Local'):
        input_label = "Enter the local phrase:"
        source_db = phrases_db
        not_found = "Sorry, I don't know that one yet. Try contributing it!"
    else:
        input_label = "Enter the English phrase:"
        source_db = {v.lower(): k for k, v in phrases_db.items()}
        not_found = "No local version found. Want to contribute it?"

    user_input = st.text_input(input_label, placeholder="Type a phrase here...")

    if st.button("Translate", use_container_width=True, type="primary"):
        if user_input:
            query = user_input.strip().lower()
            translation = source_db.get(query, not_found)
            st.subheader("Translation:")
            st.success(translation)
        else:
            st.warning("Please enter a phrase first.")

# --- Contribute Mode ---
elif mode == 'Contribute a New Phrase':
    st.title("✍️ Contribute a Phrase")
    st.info("Add your own local phrase and help others understand your lingo!", icon="🙏")

    st.subheader("🎤 Optional: Use audio input")
    audio_file = st.file_uploader("Upload audio (wav/mp3/m4a)", type=["wav", "mp3", "m4a"])
    transcript = ""

    if audio_file:
        st.audio(audio_file)
        try:
            audio = AudioSegment.from_file(audio_file).set_channels(1).set_frame_rate(16000)
            with BytesIO() as buf:
                audio.export(buf, format="wav")
                buf.seek(0)

                recognizer = sr.Recognizer()
                with sr.AudioFile(buf) as source:
                    audio_data = recognizer.record(source)
                    transcript = recognizer.recognize_google(audio_data)
                    st.success(f"Recognized: {transcript}")
        except:
            st.error("Could not process the audio.")

    with st.form("contribution_form"):
        local_phrase = st.text_input("Local/Colloquial Phrase:", value=transcript)
        english_phrase = st.text_input("Standard English Equivalent:")
        submit = st.form_submit_button("Submit")

        if submit:
            if local_phrase and english_phrase:
                local_key = local_phrase.strip().lower()
                english_val = english_phrase.strip()
                phrases_db[local_key] = english_val
                save_database(phrases_db)

                title, description = generate_title_description(local_key, english_val)

                append_to_gsheet(
                    local=local_key,
                    english=english_val,
                    location=user_location,
                    title=title,
                    description=description
                )

                st.success("Thank you! Your phrase was added.")
                st.info(f"📝 Title: {title}")
                st.caption(description)
                st.balloons()
            else:
                st.error("Please fill in both fields.")

# --- View Database ---
with st.expander("🧐 See all known phrases"):
    st.json(phrases_db)
