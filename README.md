# 🦜 LangChain AI Portfolio

A collection of production-ready AI applications built with LangChain, Groq, and Streamlit.

---

## 🚀 Projects

### 1. 📄 Single PDF Chatbot
Chat with any PDF document using RAG (Retrieval Augmented Generation)
- **Tech:** LangChain + FAISS + HuggingFace Embeddings + Groq
- **Run:** `streamlit run app_ui.py`

### 2. 📚 Multi-PDF Research Assistant
Upload multiple PDFs and ask questions across all of them simultaneously
- **Tech:** LangChain + FAISS + HuggingFace + Groq + Streamlit
- **Features:** Source attribution, page numbers, conversation memory, chat export
- **Run:** `streamlit run multi_pdf.py`

### 3. 🕵️ AI Web Research Agent
Autonomous AI agent that searches the web and generates research reports
- **Tech:** LangChain + Tavily Search + Groq + Streamlit
- **Features:** Multi-query search, structured reports, download reports
- **Run:** `streamlit run research_agent.py`

### 4. 🗄️ SQL Database Chatbot
Chat with databases in plain English — no SQL knowledge needed!
- **Tech:** LangChain + SQLite + Groq + Streamlit + Pandas
- **Features:** NL to SQL conversion, shows generated SQL, raw data view
- **Run:** `streamlit run sql_chat.py`

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| LangChain | AI application framework |
| Groq + LLaMA 3.3 | Large Language Model |
| FAISS | Vector similarity search |
| HuggingFace | Text embeddings |
| Tavily | Web search API |
| Streamlit | Web UI framework |
| SQLite | Database |

---

## ⚙️ Setup

1. Clone the repo:
\```bash
git clone https://github.com/YourUsername/langchain-portfolio.git
cd langchain-portfolio
\```

2. Install dependencies:
\```bash
pip install -r requirements.txt
\```

3. Create `.env` file:
\```
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
\```

4. Run any project:
\```bash
streamlit run multi_pdf.py
\```

---

## 👩‍💻 Author
**Sheema Saba** — AI Engineering Enthusiast
```

---

## 📄 Step 3: Update `.gitignore`
```
.env
__pycache__/
*.pyc
*.db
.cache/