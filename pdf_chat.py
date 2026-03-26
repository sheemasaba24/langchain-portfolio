from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass
import streamlit as st
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
if "TAVILY_API_KEY" in st.secrets:
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]

# 1. Load your PDF
print("Loading PDF...")
loader = PyPDFLoader("sample.pdf")
docs = loader.load()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
print(f"Split into {len(chunks)} chunks!")

# 3. Create embeddings & vector store
print("Creating embeddings... (first time may take a minute)")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(chunks, embeddings)

# 4. Setup retriever and LLM
retriever = vectorstore.as_retriever()
llm = ChatGroq(model="llama-3.3-70b-versatile")

# 5. Chat loop
print("\n✅ PDF loaded! Ask me anything about it. Type 'quit' to exit.\n")
while True:
    question = input("You: ")
    if question.lower() == "quit":
        break

    relevant_docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    prompt = f"""Use the following context from a PDF to answer the question.

Context:
{context}

Question: {question}

Answer:"""

    response = llm.invoke([HumanMessage(content=prompt)])
    print(f"\nBot: {response.content}\n")