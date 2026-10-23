# Customer Support Agent

A Streamlit + CrewAI application that routes customer support questions through a multi-agent workflow:

- A customer support assistant answers from knowledge first
- A web-search assistant is used only when the answer is uncertain or unavailable
- An entry agent records the interaction in `answers.txt`

## Features

- Multi-agent support workflow using CrewAI
- Web search fallback through Serper
- Streamlit web interface
- Support interaction logging

## Project structure

- `app.py` — Streamlit app UI
- `crew/agents.py` — agent definitions
- `crew/tasks.py` — task definitions for assistant, search, and record flow
- `crew/crew.py` — orchestration logic for the support workflow
- `answers.txt` — saved support records

## Run locally

1. Activate the project virtual environment:
   ```bash
   .\venv\Scripts\activate
   ```
2. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Environment

Create a `.env` file with your API keys:

```env
OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serper_key
```

## Notes

This project expects the dependencies installed in the project virtual environment and the keys configured in `.env` before running the app.
