# Race Against AI — Agentic AI Stall Game

## Run
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Run: `pip install -r requirements.txt`
4. Run: `python app.py`
5. Open `http://127.0.0.1:5000` in a browser.

No API key is required for this demo. The AI agent is simulated deterministically so it works offline at a stall.

## What it demonstrates
Goal -> planning -> tool selection -> data retrieval -> simulation -> evaluation -> decision.

For a production version, replace `/api/agent` with a real tool-calling LLM agent while keeping the visible action log.
