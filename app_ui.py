import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage

import tempfile
import os

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

st.set_page_config(page_title="Chat with PDF", page_icon="📄")
st.title("📄 Chat with your PDF")
st.markdown("Upload a PDF and ask anything about it!")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

with st.sidebar:
    st.header("📂 Upload your PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        if st.button("Process PDF"):
            with st.spinner("Reading and processing PDF..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                loader = PyPDFLoader(tmp_path)
                docs = loader.load()

                # bigger chunks, more overlap = better context
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )
                chunks = splitter.split_documents(docs)

                embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                st.session_state.vectorstore = FAISS.from_documents(chunks, embeddings)
                st.session_state.messages = []

                os.unlink(tmp_path)
                st.success(f"✅ PDF processed! ({len(chunks)} chunks)")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if question := st.chat_input("Ask something about your PDF..."):
    if st.session_state.vectorstore is None:
        st.warning("⚠️ Please upload and process a PDF first!")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # fetch top 6 chunks instead of default 4
                retriever = st.session_state.vectorstore.as_retriever(
                    search_kwargs={"k": 6}
                )
                relevant_docs = retriever.invoke(question)
                context = "\n\n".join([doc.page_content for doc in relevant_docs])

                prompt = f"""You are a helpful assistant. Answer the question using the context below from a PDF document.
Be specific and detailed. If the answer is in the context, provide it fully.

Context:
{context}

Question: {question}

Answer:"""

                llm = ChatGroq(model="llama-3.3-70b-versatile")
                response = llm.invoke([HumanMessage(content=prompt)])
                answer = response.content

            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})