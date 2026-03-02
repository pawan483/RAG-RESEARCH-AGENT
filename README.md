---
title: Ai Research Assistant
emoji: 🌍
colorFrom: gray
colorTo: yellow
sdk: gradio
sdk_version: 6.5.1
app_file: app.py
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

🔎 AI Research Assistant – Real-Time Web-Powered LLM

This project is a real-time AI research assistant built using Groq LLM (Llama 3.1 8B Instant) and Google search integration via Serper API. The system combines live web search with large language model reasoning to generate accurate, up-to-date, and well-structured answers with proper source citations.

Unlike traditional static LLM applications, this assistant first retrieves the top relevant search results from Google, formats them, and then feeds the information into the LLM as contextual grounding. The model then generates:

A concise summary

Explanation of why the topic matters

Proper source references using citation notation

The application is built with Gradio ChatInterface for a clean, interactive user experience and is securely deployed using environment-based secret keys for API protection.

🚀 Key Features

Live Google search integration (Serper API)

Groq-powered ultra-fast LLM inference

Citation-based answers

Structured markdown formatting

Secure API key handling via environment variables

Deployable on Hugging Face Spaces

🛠️ Tech Stack

Python

Groq API (Llama 3.1 8B Instant)

Serper API (Google Search)

Gradio

Requests

This project demonstrates practical knowledge of retrieval-augmented generation (RAG-style architecture), API integration, prompt engineering, and production-level deployment on Hugging Face.

It is designed for research automation, current affairs analysis, and AI-powered knowledge retrieval.
