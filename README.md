# 🧠 Jugaadu Translator  
### *Local Phrase Translator*  
**Preserve your roots. Understand each other. One phrase at a time.**

---

## 📌 Overview

**Jugaadu Translator** is a multilingual, community-driven Streamlit application that translates regional, colloquial, and dialect-based Indian phrases into standardized Hindi or English — and vice versa.

It bridges India’s linguistic diversity while **building a cultural corpus** that will help train inclusive, regional language models (LLMs) and preserve disappearing idioms and expressions.

---

## 🚀 Features

### 🗣️ Colloquial to Standard Translator  
Type regional or dialectal phrases and receive formal Hindi/English translations.

### 🔁 Bi-Directional Translation  
Translate both from local expressions to standard language and vice versa.

### ✍️ User-Contributed Phrases  
Users can contribute their own slang, idioms, or phrases — along with context or region — helping the app grow dynamically.

### 🌐 Indic Language & Transliteration Support  
Supports inputs in regional scripts as well as Romanized transliteration (e.g., Hinglish).

### 📤 Corpus Builder Mode  
All submitted phrases are logged (with consent) into a shared corpus including:
- Original Phrase  
- Translated Phrase  
- Region (State-level metadata)  
- Timestamp (optional)  
This data is stored in **Google Sheets** and/or exported to **CSV files**, which can later be used to train models, analyze dialects, or build fine-tuned translation systems.

> ⚠️ **Privacy Notice:** No user-identifying information or exact geolocation is stored. Contributions are anonymized. Only linguistic content and general region are recorded.

---

## 🌍 Problem Statement

India is home to hundreds of languages and dialects, but most NLP tools fail to capture the nuance of localized speech. From job applications to casual conversations, communication suffers when standardized tools ignore regional variation.

---

## 🧩 Our Solution

**Jugaadu Translator** serves as:

- A **practical translation assistant** for understanding everyday regional phrases  
- A **linguistic data collector** for training Indian-language models  
- A **preservation tool** for archiving disappearing dialects and folk idioms

---

## 💡 Use Cases

- A tourist from North India trying to understand a phrase in Telangana  
- Translating local slang into formal language for a resume or official document  
- NLP researchers analyzing regional variation and informal usage  
- Teachers and students learning about language diversity  
- Content creators and scriptwriters seeking authentic voice/tone  

---

## 📊 Data Collection & Corpus Uploading

All user-submitted data follows a structured process:

1. **Phrase Submission**  
   - User inputs: colloquial/local phrase  
   - User selects: language, region (dropdown or auto-detected)  
   - Optional: provides context or usage example

2. **Translation Output**  
   - The AI model returns standard Hindi/English translation  
   - User may refine or edit if they have a better alternative (community-validation loop)

3. **Corpus Logging**  
   - Every validated entry (phrase, translation, region, optional context) is saved to a **Google Sheet** via `gspread` or `pygsheets`  
   - Backup CSV exports are also stored for version control  
   - Each entry is time-stamped for chronological dataset building

4. **Corpus Usage**  
   - Data can be exported for downstream tasks like:
     - Training or fine-tuning translation models (IndicBERT, NLLB, etc.)
     - Semantic clustering of regional phrases
     - Building region-specific language packs

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
- [Streamlit](https://streamlit.io/) for the web interface

**Backend:**  
- Python  
- Google Sheets API (`gspread`, `pygsheets`)  
- CSV for lightweight backups  
- Geolocation based on dropdown or IP-region mapping (no precise data stored)

**AI/NLP Models:**  
- Hugging Face Transformers:
  - [IndicBERT](https://huggingface.co/ai4bharat/indic-bert)  
  - [NLLB-200](https://huggingface.co/facebook/nllb-200-distilled-600M)  
  - [MarianMT](https://huggingface.co/Helsinki-NLP)

**Hosting:**  
- [Hugging Face Spaces](https://huggingface.co/spaces) (via Gradio or Streamlit)  
- GitHub for version control and deployment hooks

---

## 📁 Folder Structure (Suggestion)

