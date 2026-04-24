import os
import requests
import gradio as gr
from groq import Groq

# Load API keys safely
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SEARCH_PROVIDER = os.getenv("SEARCH_PROVIDER", "serper").lower()

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY. Please add it in Hugging Face Space Secrets.")

if SEARCH_PROVIDER == "tavily":
    if not TAVILY_API_KEY:
        raise ValueError("Missing TAVILY_API_KEY. Please add it in Hugging Face Space Secrets.")
    from tavily import TavilyClient
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
else:
    if not SERPER_API_KEY:
        raise ValueError("Missing SERPER_API_KEY. Please add it in Hugging Face Space Secrets.")

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


def search_tavily(query):
    response = tavily_client.search(
        query=query,
        max_results=3,
        search_depth="basic"
    )

    results = response.get("results", [])[:3]

    formatted_results = ""
    for i, r in enumerate(results, 1):
        formatted_results += (
            f"[{i}] {r.get('title')}\n"
            f"{r.get('content')}\n"
            f"Source: {r.get('url')}\n\n"
        )

    return formatted_results


def ask_agent(question, history):
    if SEARCH_PROVIDER == "tavily":
        search_results = search_tavily(question)
    else:
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
    description="Live AI Research Assistant powered by Groq + Serper/Tavily"
)

if __name__ == "__main__":
    demo.launch()
