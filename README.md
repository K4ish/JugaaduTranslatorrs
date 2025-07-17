# 🧠 Jugaadu Translator: Local Phrase Translator

**Preserve your roots. Understand each other. One phrase at a time.**

Jugaadu Translator is a multilingual, community-powered Streamlit application that helps users translate colloquial and local phrases into standardized Hindi or English. This app bridges India's rich linguistic diversity, one phrase at a time, while collecting culturally significant data that helps build better, more inclusive language models.

---

## 🚀 Features

- 🗣️ **Colloquial to Standard Translator**  
  Type regional/dialect phrases and get translations in formal Hindi or English.

- 🔁 **Bi-Directional Translation**  
  Translate from standard to local expressions and vice versa.

- ✍️ **User-Contributed Phrases**  
  Let users teach the app new slang, idioms, or regional terms.

- 🌐 **Indic Language Support**  
  Support for transliterated input (e.g., Hinglish), multiple Indian languages.

- 📤 **Corpus Builder Mode**  
  Every phrase contributes to a crowdsourced linguistic dataset.

---

## 🌍 Problem Statement

People across India often struggle to communicate across dialects or regions due to highly localized phrases and cultural expressions. At the same time, most modern language models lack exposure to these local speech patterns.

### 🧩 Our Solution

Jugaadu Translator acts as:
- A **daily-use translation tool** for understanding region-specific speech
- A **data generator** for collecting and training regional LLMs
- A **language preservation utility** to document and share disappearing idioms

---

## 💡 Use Cases

- A North Indian tourist trying to understand a phrase in Telangana
- Job seekers translating informal language for formal resumes
- Researchers collecting dialectal variation for NLP
- Language learners and school children understanding colloquialism

---

## 👥 Team

| Name           | Role                     |
|----------------|--------------------------|
| Krishna Mishra | Project Manager          |
| Syed Adnan     | Developer (Backend & AI) |
| Karthikeya     | UI Engineer              |
| Nandhu         | UX Designer              |
| Abhishek       | QA & Tester              |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, CSV-based phrase store (easy to scale to Firebase/Supabase)
- **NLP/AI**: Hugging Face Transformers (IndicBERT, NLLB, MarianMT)
- **Hosting**: Hugging Face Spaces (Gradio/Streamlit), GitHub

---

## 📦 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-team/jugaadu-translator.git
cd jugaadu-translator
