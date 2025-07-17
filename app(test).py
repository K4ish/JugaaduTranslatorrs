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
from dotenv import load_dotenv
import streamlit_authenticator as stauth

# --- Load Environment Variables ---
load_dotenv()
COOKIE_NAME = os.getenv("COOKIE_NAME")
COOKIE_KEY = os.getenv("COOKIE_KEY")
GSHEET_NAME = os.getenv("GSHEET_NAME")
GSHEET_CREDS = "service_account.json"

# --- Google Sheets Append ---
def append_to_gsheet(local, english, location, source_lang=None, contributor=None, title=None, description=None):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GSHEET_CREDS, scope)
    client = gspread.authorize(creds)
    sheet = client.open(GSHEET_NAME).sheet1
    sheet.append_row([
        contributor or "Anonymous",
        title or "Untitled",
        description or "",
        local,
        english,
        location,
        source_lang or "N/A"
    ])

# --- Title & Description Generator ---
def generate_title_description(local_phrase, english_translation):
    title = f"Meaning of '{local_phrase[:20].capitalize()}'"
    description = f"'{local_phrase}' means \"{english_translation}\" in standard English."
    return title, description

# --- Load & Save DB ---
DB_FILE = "phrases_db.json"
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
    except:
        return {}

def save_database(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- Authentication Setup ---
users = {
    "usernames": {
        "alice@gmail.com": {"name": "Alice", "password": "test123"},
        "bob@gmail.com": {"name": "Bob", "password": "secret456"},
    }
}

hashed_passwords = stauth.Hasher(
    [u["password"] for u in users["usernames"].values()]
).generate()

for (username, user), pwd_hash in zip(users["usernames"].items(), hashed_passwords):
    user["hashed_password"] = pwd_hash

authenticator = stauth.Authenticate(
    users["usernames"],
    COOKIE_NAME,
    COOKIE_KEY,
    cookie_expiry_days=1
)

name, auth_status, username = authenticator.login("Login", "main")
if not auth_status:
    st.stop()
authenticator.logout("Logout", "sidebar")

# --- Translator App Logic ---
st.set_page_config(page_title="Jugaadu Translator", page_icon="💡")
translator = Translator()
phrases_db = load_database()
location_info = geocoder.ip('me')
user_location = f"{location_info.city}, {location_info.country}" if location_info.city else "Unknown"

# --- Sidebar Navigation ---
st.sidebar.header("Navigation")
mode = st.sidebar.radio("Choose a mode", ["Translate a Phrase", "Contribute a New Phrase", "🎙 Auto Speech Translator"])

# --- Translate a Phrase ---
if mode == "Translate a Phrase":
    st.title("🔄 Translate")
    direction = st.radio("Direction", ["Local → English", "English → Local"])

    if direction == "Local → English":
        db = phrases_db
        prompt = "Enter local phrase:"
    else:
        db = {v.lower(): k for k, v in phrases_db.items()}
        prompt = "Enter English phrase:"

    user_input = st.text_input(prompt)

    if st.button("Translate"):
        if user_input:
            result = db.get(user_input.strip().lower(), "Not found. Try contributing!")
            st.success(result)
        else:
            st.warning("Enter a phrase to translate.")

# --- Contribute a New Phrase ---
elif mode == "Contribute a New Phrase":
    st.title("✍️ Contribute")

    st.subheader("Optional: Use audio")
    audio_file = st.file_uploader("Upload audio (mp3/wav/m4a)", type=["mp3", "wav", "m4a"])
    transcript = ""

    if audio_file:
        try:
            audio = AudioSegment.from_file(audio_file).set_channels(1).set_frame_rate(16000)
            buf = BytesIO()
            audio.export(buf, format="wav")
            buf.seek(0)
            r = sr.Recognizer()
            with sr.AudioFile(buf) as source:
                audio_data = r.record(source)
                transcript = r.recognize_google(audio_data)
                st.success(f"Transcript: {transcript}")
        except:
            st.error("Failed to transcribe audio.")

    with st.form("contribution_form"):
        local_phrase = st.text_input("Local Phrase", value=transcript)
        english_phrase = st.text_input("English Translation")
        submit = st.form_submit_button("Submit")

        if submit and local_phrase and english_phrase:
            local_key = local_phrase.strip().lower()
            phrases_db[local_key] = english_phrase.strip()
            save_database(phrases_db)
            title, description = generate_title_description(local_key, english_phrase)
            append_to_gsheet(local_key, english_phrase, user_location, contributor=username, title=title, description=description)
            st.success("Thank you for contributing!")
            st.balloons()
        elif submit:
            st.warning("Please fill in both fields.")

# --- Auto Speech Translator ---
elif mode == "🎙 Auto Speech Translator":
    st.title("🎙 Auto Speech Translator")

    audio_file = st.file_uploader("Upload audio (mp3/wav/m4a)", type=["mp3", "wav", "m4a"])
    if audio_file:
        try:
            audio = AudioSegment.from_file(audio_file).set_channels(1).set_frame_rate(16000)
            buf = BytesIO()
            audio.export(buf, format="wav")
            buf.seek(0)
            r = sr.Recognizer()
            with sr.AudioFile(buf) as source:
                audio_data = r.record(source)
                spoken = r.recognize_google(audio_data)
                detected = translator.detect(spoken).lang
                translated = translator.translate(spoken, dest="en").text
                title, description = generate_title_description(spoken, translated)
                append_to_gsheet(spoken, translated, user_location, source_lang=detected, contributor=username, title=title, description=description)

                st.success(f"🗣 Original: {spoken}")
                st.info(f"📘 Translated: {translated}")
                st.caption(description)
        except Exception as e:
            st.error(f"Error: {e}")

# --- Database Viewer ---
with st.expander("📚 View Current Phrase DB"):
    st.json(phrases_db)
