🧠 Jugaadu Translator
Local Phrase Translator
Preserve your roots. Understand each other. One phrase at a time.

📌 Overview
Jugaadu Translator is a multilingual, community-powered Streamlit application that translates colloquial and local phrases into standardized Hindi or English. It aims to bridge India’s rich linguistic diversity by collecting culturally significant data to train better, more inclusive language models.

🚀 Features
🗣️ Colloquial to Standard Translator
Type regional/dialect phrases and get translations in formal Hindi or English.

🔁 Bi-Directional Translation
Translate from standard to local expressions and vice versa.

✍️ User-Contributed Phrases
Allow users to contribute new slang, idioms, or regional terms.

🌐 Indic Language Support
Supports transliterated input (e.g., Hinglish) and multiple Indian languages.

📤 Corpus Builder Mode
Every phrase contributes to a crowdsourced linguistic dataset.
Data includes:

Phrase

Translation

Region (state-level geolocation)
Stored anonymously in Google Sheets for future training and analysis.

⚠️ Privacy Note: All contributions are anonymized. No exact user location is stored—only phrase, translation, and general region.

🌍 Problem Statement
India’s diversity in dialects makes communication across regions difficult.
Modern LLMs lack sufficient data on local idioms and speech patterns, causing poor performance in real-world multilingual usage.

🧩 Our Solution
Jugaadu Translator functions as:

A daily-use translation tool for region-specific speech

A data generator for collecting dialectal expressions to train regional LLMs

A language preservation utility for documenting disappearing idioms

💡 Use Cases
A tourist from North India understanding phrases in Telangana

Job seekers converting informal local language into formal resume-ready language

NLP researchers collecting dialectal variations

Language learners and school children learning colloquial speech

👥 Team
Name	Role
Krishna Mishra	Project Manager
Syed Adnan	Developer (Backend & AI)
Karthikeya	UI Engineer
Nandhu	UX Designer
Abhishek	QA & Tester

🛠️ Tech Stack
Frontend:

Streamlit

Backend:

Google Sheets

Python

CSV-based phrase store (scalable to Firebase/Supabase)

NLP / AI Models:

Hugging Face Transformers

IndicBERT

NLLB

MarianMT

Hosting:

Hugging Face Spaces (Gradio/Streamlit)

GitHub

