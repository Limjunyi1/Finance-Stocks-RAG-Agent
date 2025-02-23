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

## Sample documents used
* https://finance.yahoo.com/news/warren-buffett-says-berkshire-hathaway-did-better-than-i-expected-last-year-in-latest-letter-to-shareholders-151248284.html
* https://finance.yahoo.com/news/mercedes-benz-wont-be-following-tesla-and-elon-musk-into-robotaxis-132803197.html
* https://finance.yahoo.com/news/gold-heads-for-eighth-weekly-gain-as-precious-metals-shipments-to-us-rise-195332488.html
* https://finance.yahoo.com/news/rivian-posts-170-million-gross-profit-in-q4-sees-losses-decreasing-as-variable-costs-improve-185717790.html
* https://finance.yahoo.com/news/reddit-stock-falls-more-than-20-since-last-weeks-earnings-report-as-6-month-rally-eases-143107638.html
