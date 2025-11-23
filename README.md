# Intelligent Voice Bot for Customer Interaction

A full-stack AI Voice Bot capable of real-time speech recognition, intent understanding, and dynamic audio responses. Built for the AI Intern Assignment (Round 1).

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.0-orange)
![Streamlit](https://img.shields.io/badge/Analytics-Streamlit-red)

## Key Features
* **Speech-to-Text:** Uses Google Gemini 2.0 Flash for high-accuracy transcription.
* **Natural Language Understanding (NLU):** Classifies user intents (Balance, FAQs, Greetings) using LLMs.
* **Text-to-Speech:** Generates natural audio responses using gTTS.
* **Database Integration:** Fetches real-time account details and FAQs from an SQLite database.
* **Analytics Dashboard:** Tracks user queries, response times, and intent distribution via Streamlit.

## Project Structure
```text
voice_bot_project/
├── app/
│   ├── main.py       # FastAPI Server (The "Front Door")
│   ├── dialog.py     # Conversation Manager (The "Manager")
│   ├── db.py         # Database & Logging
│   └── utils/        # AI Modules (STT, NLU, TTS)
├── client/
│   └── mic_record.py # Client-side voice recorder
├── analytics/
│   └── dashboard.py  # Streamlit Analytics Dashboard
├── data/             # SQLite Database storage
└── requirements.txt  # Project dependencies


graph TD
    User((User)) -->|Voice Input| Mic[Client Recorder]
    Mic -->|WAV File| Server[FastAPI Backend]
    
    subgraph "AI Processing Pipeline"
        Server -->|Audio| STT[Gemini STT]
        STT -->|Text| NLU[Gemini Intent Analyzer]
        NLU -->|Intent| Logic{Decision Engine}
        
        Logic -- "Balance/FAQ" --> DB[(SQLite Database)]
        Logic -- "General Chat" --> LLM[Gemini LLM]
    end
    
    DB --> Response
    LLM --> Response
    
    Response -->|Text| TTS[gTTS Engine]
    TTS -->|MP3 Audio| User
