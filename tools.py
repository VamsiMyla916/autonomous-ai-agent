# tools.py

# --- Core Imports ---
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain, RetrievalQA
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

#################################################################
# TOOL 1: SQL DATABASE TOOL
#################################################################

# 1. Initialize the basic Ollama LLM
llm = Ollama(model="llama3:8b", temperature=0)

# 2. Connect to the database
db = SQLDatabase.from_uri("sqlite:///sales_db.sqlite")

# 3. Create the chain that converts questions to SQL queries
write_query_chain = create_sql_query_chain(llm, db)

# 4. Create the tool that executes the SQL queries
execute_query_tool = QuerySQLDataBaseTool(db=db)


#################################################################
# TOOL 2: RAG SYSTEM TOOL
#################################################################

def setup_rag_tool():
    """
    Sets up the entire RAG pipeline and returns a queryable chain.
    """
    loader = TextLoader('./data/support_tickets.txt')
    documents = loader.load()
    
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    
    embeddings = OllamaEmbeddings(model="llama3:8b")
    
    vector_store = FAISS.from_documents(docs, embeddings)
    
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )
    
    return rag_chain

# Create an instance of the RAG tool
rag_tool = setup_rag_tool()