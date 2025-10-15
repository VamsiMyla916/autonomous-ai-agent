# tools.py
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain, RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, convert_system_message_to_human=True)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

db = SQLDatabase.from_uri("sqlite:///sales_db.sqlite")
write_query_chain = create_sql_query_chain(llm, db)
execute_query_tool = QuerySQLDataBaseTool(db=db)

def setup_rag_tool():
    loader = TextLoader('./data/support_tickets.txt')
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    vector_store = FAISS.from_documents(docs, embeddings)
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=vector_store.as_retriever()
    )
    return rag_chain

rag_tool = setup_rag_tool()