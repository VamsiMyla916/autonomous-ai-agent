# app.py

import streamlit as st
from agent import agent_executor
import re

# --- App Configuration ---
st.set_page_config(
    page_title="Autonomous Sales Agent",
    page_icon="🤖",
    layout="wide"
)

# --- App Title ---
st.title("🤖 Autonomous Sales Operations Agent")
st.write("Ask complex questions about sales and support, and the agent will use its tools to find the answer.")

# --- Main Interaction ---
# Get user input from a standard text box
user_question = st.text_input("Enter your question:")

if user_question:
    # Display a loading spinner while the agent is working
    with st.spinner("The agent is thinking..."):
        try:
            # Invoke the agent with the user's question
            response = agent_executor.invoke({
                "input": user_question
            })
            
            # Extract and clean the final answer
            raw_answer = response["output"]
            cleaned_answer = re.split(r'\s*\([^)]*\)$', raw_answer)[0].strip()

            # Display the final answer in a success box
            st.success("Here is the answer:")
            st.write(cleaned_answer)

        except Exception as e:
            st.error(f"An error occurred: {e}")