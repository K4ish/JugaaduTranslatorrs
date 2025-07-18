# 🧠 Jugaadu Translator  
### *Local Phrase Translator*  
**Preserve your roots. Understand each other. One phrase at a time.**

---

## 📌 Overview

**Jugaadu Translator** is a multilingual, community-driven Streamlit application that translates regional, colloquial, and dialect-based Indian phrases into standardized Hindi or English — and vice versa.

It bridges India’s linguistic diversity while **building a cultural corpus** that helps train inclusive, regional language models (LLMs) and preserves disappearing idioms and expressions — now with **speech-to-text audio input** for verbal submissions.

--

## 🚀 Features

### 🗣️ Colloquial to Standard Translator  
Type or **speak** regional/dialect phrases and get translations in formal Hindi or English.

### 🔁 Bi-Directional Translation  
Translate from standard language to local expressions and vice versa.

### 🎙️ Audio Input with Speech-to-Text  
Users can **record audio** of local phrases.  
The app transcribes spoken input using a Speech-to-Text model before translation.

### ✍️ User-Contributed Phrases  
Users can contribute their own slang, idioms, or phrases — along with category, title, and context.

### 🌐 Indic Language & Transliteration Support  
Supports both native scripts and Romanized input (e.g., Hinglish).

### 📤 Corpus Builder Mode  
All entries go into a structured, crowdsourced linguistic dataset with the following fields:
- Original Phrase (Text or Transcribed Audio)  
- Translated Phrase  
- **Category** (e.g., Greeting, Insult, Folk Saying)  
- **Title** (Short label)  
- **Description** (Context/Usage)  
- **Geo-coordinates**  
- **User alias**  
- Timestamp  

Stored securely in **Google Sheets** and exported to CSV for open-source training purposes.

> ⚠️ **Privacy Notice:** No exact user location or personal data is collected. Only regional-level metadata is retained.

---

## 🌍 Problem Statement

India is home to hundreds of languages and dialects, yet most NLP tools overlook these variations. Without context-aware, region-sensitive translation, digital tools fail real users.

---

## 🧩 Our Solution

**Jugaadu Translator** serves as:

- A **daily-use translator** for regional speech  
- A **speech-aware language dataset builder**  
- A **cultural preservation platform** for fading idioms  
- A **resource for training multilingual LLMs**

--

## 💡 Use Cases

- Tourists trying to understand a phrase by speaking it  
- Elders dictating folk idioms for preservation  
- Job applicants refining casual slang into formal English  
- Linguistic researchers collecting geo-tagged voice data  
- Students and educators learning authentic dialect

---

## 📊 Data Collection & Corpus Uploading

### 🔄 Input Flow:

1. **User Input**  
   - Enter phrase by **text** or **microphone recording**  
   - Add **title**, **description**, **category**, and **region**  
   - Location auto-detected via browser or entered manually  
   - Optional pseudonymous user alias

2. **Processing**  
   - Audio input is converted to text using a Speech-to-Text model  
   - Phrase is translated to formal Hindi/English  
   - User reviews and confirms or edits output

3. **Corpus Logging**  
   - Each validated phrase and its metadata is stored in:
     - Google Sheets via `gspread` or `pygsheets`
     - CSV backups for export or downstream use

4. **Corpus Usage**  
   - LLM fine-tuning (e.g., IndicBERT, NLLB)  
   - Audio-text alignment for STT improvement  
   - Region-based semantic search systems

---

## 👥 Team

| Name           | Role                         |
|----------------|------------------------------|
| Krishna Mishra | Project Manager              |
| Syed Adnan     | Frontend Developer           |
| Karthikeya     | UI Engineer                  |
| Nandhu         | QA & Tester                  |
| Abhishek       | Backend Developer            |

---

## 🛠️ Tech Stack

**Frontend:**  
- Streamlit  
- HTML5 Audio API for microphone access

**Backend & Storage:**  
- Python  
- Google Sheets API (`gspread`, `pygsheets`)  
- CSV data storage  
- GeoIP or browser location API

**AI/NLP Models:**  
- Hugging Face Transformers:
  - [IndicBERT](https://huggingface.co/ai4bharat/indic-bert)  
  - [NLLB-200](https://huggingface.co/facebook/nllb-200-distilled-600M)  
  - [MarianMT](https://huggingface.co/Helsinki-NLP)

**Speech-to-Text:**  
- [Whisper by OpenAI](https://github.com/openai/whisper) *(default)*  
- Optional fallback: Google Cloud STT or Vosk (offline)

**Hosting:**  
- Hugging Face Spaces (Gradio/Streamlit)  
- GitHub for CI/CD & collaboration

---

## 📁 Folder Structure (Suggested)

