# agent.py

import ast  # Import the ast library to safely evaluate the string result
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate

# --- Import your tools and llm from tools.py ---
from tools import llm, execute_query_tool, write_query_chain, rag_tool

# --- Define Tool Functions ---

def run_sql_query(question: str) -> str:
    """
    Takes a natural language question, generates a SQL query, cleans it,
    executes it, and returns a simplified, clean result.
    """
    # --- SQL Generation and Cleaning ---
    raw_sql_response = write_query_chain.invoke({"question": question})
    print(f"DEBUG: Raw LLM Output for SQL: {raw_sql_response}")

    if "SQLQuery:" in raw_sql_response:
        clean_sql = raw_sql_response.split("SQLQuery:")[-1].strip()
    elif "```" in raw_sql_response:
        clean_sql = raw_sql_response.split("```")[1].replace("sql", "").strip()
    else:
        clean_sql = raw_sql_response.strip()
    
    if clean_sql.endswith(';'):
        clean_sql = clean_sql[:-1]

    print(f"DEBUG: Cleaned SQL Query: {clean_sql}")

    # --- Execution and NEW SIMPLIFIED OUTPUT ---
    raw_result_str = execute_query_tool.invoke({"query": clean_sql})
    print(f"DEBUG: Raw DB Result: {raw_result_str}")

    try:
        # Safely evaluate the string to a Python object (e.g., a list of tuples)
        result_obj = ast.literal_eval(raw_result_str)
        
        # If the result is a list containing a tuple with one number
        if isinstance(result_obj, list) and len(result_obj) == 1 and isinstance(result_obj[0], tuple) and len(result_obj[0]) == 1:
            # Extract just the number
            final_value = result_obj[0][0]
            return f"The final answer is {final_value}"
        else:
            # Otherwise, return the structured result as a string
            return f"The query returned the following data: {raw_result_str}"
            
    except (ValueError, SyntaxError):
        # If the result is not a list/tuple (e.g., an error message), return as is
        return raw_result_str

def run_rag_query(question: str) -> str:
    """Queries the support ticket knowledge base."""
    response = rag_tool.invoke(question)
    return response.get('result', 'No answer found.')

# --- Create Tool Objects ---
sql_tool = Tool(
    name="SalesDB_Query",
    func=run_sql_query,
    description="Useful for when you need to answer questions about sales, revenue, clients, and financial data. Input should be a full question in natural language."
)

support_ticket_tool = Tool(
    name="Support_Ticket_KB",
    func=run_rag_query,
    description="Useful for when you need to find information about customer support tickets, issues, or client problems. Input should be a full question in natural language."
)

tools = [sql_tool, support_ticket_tool]

# --- Agent Creation with IMPROVED PROMPT ---
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

**IMPORTANT RULE: After you receive an Observation, if you have enough information to answer the user's question, you MUST immediately respond with a Thought and a Final Answer. Do not take another action. Do not repeat actions.**

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)