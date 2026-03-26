import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

import tempfile
import os
from datetime import datetime

import os
try:
    # Local development
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Streamlit Cloud
import streamlit as st
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

st.set_page_config(page_title="Multi-PDF Research Assistant", page_icon="📚", layout="wide")
st.title("📚 Multi-PDF Research Assistant")
st.markdown("Upload multiple PDFs and ask questions across all of them!")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # LangChain memory
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

# Sidebar
with st.sidebar:
    st.header("📂 Upload PDFs")
    uploaded_files = st.file_uploader(
        "Upload one or more PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("⚡ Process All PDFs"):
            all_chunks = []
            progress = st.progress(0)
            file_names = []

            for i, uploaded_file in enumerate(uploaded_files):
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(uploaded_file.read())
                        tmp_path = tmp.name

                    loader = PyPDFLoader(tmp_path)
                    docs = loader.load()

                    for doc in docs:
                        doc.metadata["source"] = uploaded_file.name

                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200
                    )
                    chunks = splitter.split_documents(docs)
                    all_chunks.extend(chunks)
                    file_names.append(uploaded_file.name)
                    os.unlink(tmp_path)

                progress.progress((i + 1) / len(uploaded_files))

            with st.spinner("Building knowledge base..."):
                embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                st.session_state.vectorstore = FAISS.from_documents(all_chunks, embeddings)
                st.session_state.processed_files = file_names
                st.session_state.messages = []
                st.session_state.chat_history = []

            st.success(f"✅ {len(uploaded_files)} PDFs processed! ({len(all_chunks)} chunks)")

    # Loaded files list
    if st.session_state.processed_files:
        st.markdown("### 📄 Loaded Documents")
        for f in st.session_state.processed_files:
            st.markdown(f"- 📄 {f}")

    st.markdown("---")

    # Download chat history
    if st.session_state.messages:
        st.markdown("### 💾 Export Chat")
        chat_text = f"Chat Export — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        chat_text += "=" * 50 + "\n\n"
        for msg in st.session_state.messages:
            role = "You" if msg["role"] == "user" else "Assistant"
            chat_text += f"{role}:\n{msg['content']}\n\n"
            if "sources" in msg:
                chat_text += f"Sources: {', '.join(msg['sources'])}\n"
            chat_text += "-" * 30 + "\n\n"

        st.download_button(
            label="📥 Download Chat History",
            data=chat_text,
            file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )

        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.rerun()

# Chat history display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        # Show sources with page numbers
        if "sources" in msg and msg["sources"]:
            st.markdown("---")
            st.markdown("📎 **Sources:**")
            for src in msg["sources"]:
                st.markdown(f"- {src}")

# Chat input
if question := st.chat_input("Ask anything across your PDFs..."):
    if st.session_state.vectorstore is None:
        st.warning("⚠️ Please upload and process at least one PDF first!")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching across documents..."):
                retriever = st.session_state.vectorstore.as_retriever(
                    search_kwargs={"k": 6}
                )
                relevant_docs = retriever.invoke(question)

                # Build context with source + page number
                context_parts = []
                source_details = []
                seen = set()

                for doc in relevant_docs:
                    source = doc.metadata.get("source", "Unknown")
                    page = doc.metadata.get("page", 0) + 1  # pages are 0-indexed
                    tag = f"📄 {source} — Page {page}"
                    context_parts.append(f"[From: {source}, Page {page}]\n{doc.page_content}")
                    if tag not in seen:
                        source_details.append(tag)
                        seen.add(tag)

                context = "\n\n".join(context_parts)

                # Build conversation history for memory
                history_text = ""
                for h in st.session_state.chat_history[-6:]:  # last 3 exchanges
                    if isinstance(h, HumanMessage):
                        history_text += f"User: {h.content}\n"
                    elif isinstance(h, AIMessage):
                        history_text += f"Assistant: {h.content}\n"

                prompt = f"""You are an expert research assistant helping analyze PDF documents.
Use the context below to answer the question. Mention which document and page the info comes from.
If the answer isn't in the context, say so clearly.

Previous Conversation:
{history_text}

Context from PDFs:
{context}

Current Question: {question}

Answer:"""

                llm = ChatGroq(model="llama-3.3-70b-versatile")
                response = llm.invoke([HumanMessage(content=prompt)])
                answer = response.content

                # Update memory
                st.session_state.chat_history.append(HumanMessage(content=question))
                st.session_state.chat_history.append(AIMessage(content=answer))

            st.write(answer)

            # Show sources with page numbers
            if source_details:
                st.markdown("---")
                st.markdown("📎 **Sources:**")
                for src in source_details:
                    st.markdown(f"- {src}")

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": source_details
            })