import os
import requests
import gradio as gr
from groq import Groq

# Load API keys safely
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not GROQ_API_KEY or not SERPER_API_KEY:
    raise ValueError("Missing API keys. Please add them in Hugging Face Space Secrets.")

client = Groq(api_key=GROQ_API_KEY)


def search_google(query):
    url = "https://google.serper.dev/search"
    payload = {"q": query, "gl": "us", "hl": "en"}
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        return "Search failed."

    results = response.json().get("organic", [])[:3]

    formatted_results = ""
    for i, r in enumerate(results, 1):
        formatted_results += (
            f"[{i}] {r.get('title')}\n"
            f"{r.get('snippet')}\n"
            f"Source: {r.get('link')}\n\n"
        )

    return formatted_results


def ask_agent(question, history):
    search_results = search_google(question)

    prompt = f"""
You are an expert AI research assistant.

Use the search results below to answer the question.
Cite sources using [number] notation.

Search Results:
{search_results}

User Question:
{question}

Provide:
1. A concise summary
2. Why it matters
3. Source references like [1], [2]
Format nicely using markdown.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a professional AI research assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


demo = gr.ChatInterface(
    fn=ask_agent,
    title="🔎 AI Research Assistant",
    description="Live Google-powered AI using Groq + Serper"
)

if __name__ == "__main__":
    demo.launch()
