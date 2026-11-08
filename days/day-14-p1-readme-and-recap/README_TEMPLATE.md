# Ticket Summarizer

Reads 20 sample support tickets from `tickets.json` and writes a short summary for each one into `report.json`, using an LLM API.

![output](output.png)

## Run

```
pip install google-genai
cp .env.example .env
python summarizer.py
```

After the second command, open `.env` and paste your own API key. Windows Command Prompt: use `copy .env.example .env`.

## Kya seekha

- How to call an LLM from Python and keep the key in `.env`, not in the code.
- How to ask for the answer in a fixed format, so the code can save it as JSON.
- How to run the same prompt on many tickets with a loop.

## Data

Sample tickets only. No company data.

---
Built by YOUR NAME as Project 1 of the 42-day AI Engineer challenge.
