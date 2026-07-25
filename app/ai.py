# AI helper functions using Ollama (local LLM)
# - summarize_ticket(text): returns a short summary
# - analyze_sentiment(text): returns sentiment and reasoning
# - suggest_reply(text): returns a professional support reply

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def call_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=300)
    response.raise_for_status()

    data = response.json()
    return data.get("response", "").strip()


def summarize_ticket(text: str) -> str:
    prompt = f"""
You are a customer support assistant.
Summarize the following customer support ticket in 1-2 short sentences:

{text}

Summary:
"""
    return call_ollama(prompt)


def analyze_sentiment(text: str) -> str:
    prompt = f"""
Respond in this exact format:

Sentiment: <Positive / Neutral / Negative>
Reasoning: <One sentence explanation>


Message:
{text}

Sentiment analysis:
"""
    return call_ollama(prompt)


def suggest_reply(text: str) -> str:
    prompt = f"""
You are a professional customer support agent.
Write a polite, helpful, and professional reply to the following customer message:

Customer message:
{text}

Suggested reply:
"""
    return call_ollama(prompt)
