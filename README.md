# AI Job Search & Resume Automation Agent — Phase 1

## Setup (Linux/macOS)
    python -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env

## Setup (Windows)
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    copy .env.example .env

Gemini API key: https://aistudio.google.com/apikey → paste into `.env` as GEMINI_API_KEY.

## Run
    streamlit run app.py

## Test
    pytest -q
# JobPilot-AI
