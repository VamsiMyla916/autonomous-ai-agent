Autonomous AI Agent for Business Intelligence 🤖
This project is a sophisticated AI agent that functions as a junior business analyst. It can understand complex, multi-part questions asked in natural language, reason about a plan, and use a set of tools to autonomously gather information from different data sources to provide a comprehensive answer.

The agent is capable of querying both structured data from a SQL database (e.g., sales figures) and unstructured data from a document knowledge base (e.g., support tickets), making it a powerful tool for business intelligence.

Key Features ✨
Natural Language to SQL: Allows non-technical users to query a sales database using plain English.

RAG on Documents: Uses a Retrieval-Augmented Generation (RAG) system to find and synthesize information from a knowledge base of support tickets.

Autonomous Tool Selection: The agent can intelligently decide which tool (SQL or RAG) is needed to answer a user's question, and can even use multiple tools in sequence.

Local LLM Powered: Runs entirely on your local machine using Ollama and the Llama 3 model, requiring no API keys or internet connection.

Interactive Web UI: A clean, user-friendly chat interface built with Streamlit.

High-Level Architecture 🏗️
The application follows a modern agentic architecture where the user interacts with an agent that orchestrates various tools.

+----------------+ +-----------------+ +-----------------+
| User Interface |----->| LangChain |----->| Tools |
| (Streamlit) | | Agent Executor | | (SQL, RAG, etc) |
+----------------+ +-----------------+ +-------+---------+
^ | | |
| v v v
+-----------------+ +-----------+ +-------------+
| LLM (Ollama) | | SQL DB | | Vector Store|
+-----------------+ +-----------+ +-------------+
Tech Stack 🛠️
LLM Framework: LangChain

LLM: Meta Llama 3 (via Ollama)

Web Framework: Streamlit

Database: SQLite

Vector Store: FAISS

Core Language: Python

🚀 Setup and Installation
Follow these steps to get the application running on your local machine.

Prerequisites
Python: Make sure you have Python 3.9+ installed.

Ollama: You must have Ollama installed and running.

Step-by-Step Guide
Pull the Llama 3 Model:
Open your terminal and run the following command to download the Llama 3 model.

Bash

ollama pull llama3:8b
Clone the Repository:

Bash

git clone https://github.com/YourUsername/autonomous-ai-agent.git
cd autonomous-ai-agent
(Replace YourUsername with your actual GitHub username.)

Create and Activate a Virtual Environment:
It is highly recommended to use a virtual environment to manage dependencies.

Bash

# Create the environment

python -m venv venv

# Activate the environment

# On Windows:

.\venv\Scripts\Activate

# On macOS/Linux:

source venv/bin/activate
Install Dependencies:
Install all the required Python packages from the requirements.txt file.

Bash

pip install -r requirements.txt
Set Up the Database:
Run the setup script to create the sales_db.sqlite database and populate it with mock data.

Bash

python setup_database.py
Launch the Application:
You're all set! Run the following command to start the Streamlit web server.

Bash

streamlit run app.py
Your browser should automatically open a new tab with the application running.

Usage Guide 📖
Once the application is running, you can interact with the agent through the chat interface.

Try asking some questions like:

What was our total revenue?

Show me the top 3 clients by sales amount.

What is the open support ticket for Innovate Solutions?

Summarize the support ticket for our highest-paying client.
