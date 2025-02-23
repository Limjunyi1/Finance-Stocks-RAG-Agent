# Finance-Stocks-RAG-Agent
This project demonstrates an AI-powered Q&A assistant for the trading domain using Retrieval-Augmented Generation (RAG). The system retrieves context from a pre-curated corpus of trading articles (stored using FAISS), leverages Huggingface generative models to produce answers, and augments responses with real-time stock data (via yfinance). An agent orchestrates multiple tools so that user queries receive grounded, up-to-date, and context-rich responses.

## Objective:
* Build an AI-powered agent that answers trading-related questions by combining a curated document corpus (retrieved from FAISS) with a generative model (via Huggingface). The agent also pulls live stock information using yfinance.

## Approach:

Employ a Retrieval-Augmented Generation (RAG) setup along with an agile agent that:
* Retrieves context from domain-specific articles.
* Augments responses with dynamic stock data when needed.
* Generates coherent answers using natural language generation techniques.

## Technology Stack
* Language: Python 3
* Editor: Cursor AI/VS Code
* Key Libraries:
  * Huggingface Transformers
  * Sentence Transformers
  * FAISS
  * smolagents (or a custom orchestrator)
  * yfinance
  * Streamlit or Gradio
* Version Control: Git
