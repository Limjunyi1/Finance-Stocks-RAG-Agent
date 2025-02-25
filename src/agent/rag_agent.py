import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from smolagents import CodeAgent, tool, HfApiModel, FinalAnswerTool
import yaml
from src.retrieval.vecdb_retrieval import retrieve_documents
from src.agent.stock_tool import get_stock_price


@tool
def retrieve_context(query: str) -> str:
    """
    A tool that retrieves relevant context from the FAISS vector database.
    
    Args:
        query: The query string used to search for relevant document chunks.
    
    Returns:
        str: A single string containing concatenated document chunks similar to the query.
    """
    docs = retrieve_documents(query)
    context = "\n".join([doc.get("chunk_text", "") for doc in docs])
    return context


@tool
def fetch_stock_price(symbol: str, date: str) -> str:
    """
    Tool that retrieves stock price information for a specified stock symbol on a given date.
    
    Args:
        symbol: The stock symbol (e.g., "AAPL", "TSLA").
        date: The date in YYYY-MM-DD format.
    
    Returns:
        str: A formatted string with the closing price or an error message.
    """
    return get_stock_price(symbol, date)


# Load prompt templates from YAML file.
with open("src/agent/prompts.yaml", "r") as f:
    prompt_templates = yaml.safe_load(f)

final_answer = FinalAnswerTool()

# Initialize the Hugging Face model wrapper using HfApiModel.
# Feel free to change the model_id to another open-source model on Hugging Face if desired.
model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    model_id="",  # Provide the model ID here and set up the HF token
)

# Create the CodeAgent by supplying the model, prompt templates, and the tools.
agent = CodeAgent(
    model=model,
    tools=[final_answer, retrieve_context, fetch_stock_price],
    max_steps=6,
    prompt_templates=prompt_templates
)


def main():
    query = input("Enter your query: ")
    result = agent.run(query)
    print("Final Answer:")
    print(result)


if __name__ == "__main__":
    main() 