# app.py
import streamlit as st
import re
import os
from setup_database import create_and_populate_db

# This runs once and caches the result
@st.cache_resource
def initial_setup():
    # Create the database on first run
    create_and_populate_db()
    # Dynamically import the agent after setup
    from agent import agent_executor
    return agent_executor

# The API key is handled by Streamlit's secrets management
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

agent_executor = initial_setup()

st.set_page_config(page_title="AI Co-pilot", page_icon="🤖", layout="wide")
st.title("🤖 AI Co-pilot for Business Intelligence")
st.write("Ask complex questions about sales and support, and the agent will find the answer.")
user_question = st.text_input("Enter your question:")

if user_question:
    with st.spinner("The agent is thinking..."):
        try:
            response = agent_executor.invoke({"input": user_question})
            raw_answer = response["output"]
            cleaned_answer = re.split(r'\s*\([^)]*\)$', raw_answer)[0].strip()
            st.success("Here is the answer:")
            st.write(cleaned_answer)
        except Exception as e:
            st.error(f"An error occurred: {e}")