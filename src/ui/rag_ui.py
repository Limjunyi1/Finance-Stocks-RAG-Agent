import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import streamlit as st
from src.agent.rag_agent import agent

# Run by typing "streamlit run src/ui/rag_ui.py" in the terminal
def main():
    # Set page configuration
    st.set_page_config(
        page_title="Finance & Stocks RAG Agent", 
        page_icon=":chart_with_upwards_trend:", 
        layout="wide"
    )
    
    # Custom CSS styling for the page (header, answer card, chain-of-thought, etc.)
    st.markdown(
        """
        <style>
        .header {
            background: linear-gradient(90deg, #0a2342 0%, #1a456f 100%);
            padding: 20px;
            border-radius: 5px;
            color: white;
            text-align: center;
        }
        .final-answer {
            background-color: #dff0d8;
            padding: 20px;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 18px;
            border-left: 8px solid #3c763d;
        }
        .cot-section {
            background-color: #f2f2f2;
            border-radius: 5px;
            padding: 15px;
            font-family: monospace;
            white-space: pre-wrap;
            margin-top: 10px;
            border: 1px solid #ccc;
        }
        </style>
        """, unsafe_allow_html=True
    )
    
    # Banner image
    st.image("https://ih0.redbubble.net/cover.2079180.2400x600.jpg", use_container_width=True)

    # Header
    st.markdown("<div class='header'><h1>Finance & Stocks RAG Agent</h1></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center;">
            This intelligent agent combines financial document retrieval and real-time stock data analysis to answer your trading-related queries.
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style="text-align: center;">
            Enter your question below and see the agent in action along with its internal chain-of-thought.
        </div>
        """, unsafe_allow_html=True
    )

    # User input area
    user_query = st.text_area("Enter your query", height=120)
    
    if st.button("Get Answer"):
        if not user_query.strip():
            st.error("Please enter a query before submitting.")
        else:
            with st.spinner("Processing your query..."):
                # Run the agent.
                answer = agent.run(user_query)
                    
            # Display final answer in a styled card with improved color and contrast
            st.markdown(f"<div class='final-answer' style='background-color: #d4edda; color: #155724; padding: 20px; border-radius: 5px; margin-top: 20px; font-size: 18px; border-left: 8px solid #3c763d;'><strong>Final Answer:</strong><br>{answer}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main() 