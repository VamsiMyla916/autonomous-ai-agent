# agent.py

from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain_core.prompts import ChatPromptTemplate

# --- This file is model-agnostic. It just needs an LLM and tools. ---

def create_agent(llm, sql_tool, rag_tool):
    """Creates the AI agent executor."""
    tools = [
        Tool(
            name="SalesDB_Query",
            func=sql_tool.invoke,
            description="Useful for when you need to answer questions about sales, revenue, clients, and financial data. Input should be a full natural language question."
        ),
        Tool(
            name="Support_Ticket_KB",
            func=lambda q: rag_tool.invoke({"query": q}),
            description="Useful for when you need to find information about customer support tickets, issues, or client problems."
        ),
    ]

    prompt_template = """
    You are an assistant that answers questions by using tools.

    You have access to the following tools:
    {tools}

    Use the following format:
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action

    **IMPORTANT RULE: After you receive an Observation, if you have enough information to answer the user's question, you MUST immediately respond with a Thought and a Final Answer. Do not take another action.**

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False)

# We are no longer importing this directly in app.py, so it's good practice
# to remove the old direct creation logic if it's still there.
# The create_agent function is all that is needed.