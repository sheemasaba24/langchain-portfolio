import streamlit as st

st.set_page_config(
    page_title="Sheema Saba | AI Portfolio",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .hero {
        text-align: center;
        padding: 40px 0;
    }
    .hero h1 {
        font-size: 3em;
        background: linear-gradient(90deg, #00d2ff, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p {
        font-size: 1.2em;
        color: #888;
    }
    .card {
        background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
        border-radius: 15px;
        padding: 25px;
        margin: 10px;
        border: 1px solid #3a3a5e;
        transition: transform 0.3s;
    }
    .card:hover {
        border-color: #7b2ff7;
    }
    .card h3 {
        color: #00d2ff;
        font-size: 1.4em;
    }
    .card p {
        color: #aaa;
        font-size: 0.95em;
    }
    .tag {
        background: #2a2a3e;
        border: 1px solid #7b2ff7;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.8em;
        color: #00d2ff;
        margin: 3px;
        display: inline-block;
    }
    .launch-btn {
        background: linear-gradient(90deg, #00d2ff, #7b2ff7);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-size: 1em;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        margin-top: 15px;
    }
    .stats {
        text-align: center;
        padding: 10px;
    }
    .stats h2 {
        color: #00d2ff;
        font-size: 2.5em;
        margin: 0;
    }
    .stats p {
        color: #888;
        margin: 0;
    }
    .section-title {
        text-align: center;
        color: white;
        font-size: 1.8em;
        margin: 30px 0 10px 0;
    }
    .divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #7b2ff7, transparent);
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <h1>🤖 Sheema Saba</h1>
    <p>AI Engineer | LangChain Developer | Building intelligent apps with LLMs</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="stats">
        <h2>4</h2>
        <p>AI Projects</p>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="stats">
        <h2>3</h2>
        <p>Live Apps</p>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="stats">
        <h2>5+</h2>
        <p>Technologies</p>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="stats">
        <h2>1</h2>
        <p>Day Built 🔥</p>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Projects Section
st.markdown('<h2 class="section-title">🚀 My LangChain Projects</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>📚 Multi-PDF Research Assistant</h3>
        <p>Upload multiple PDFs and ask questions across all of them simultaneously. 
        Features source attribution, page numbers, conversation memory and chat export.</p>
        <br>
        <span class="tag">RAG</span>
        <span class="tag">FAISS</span>
        <span class="tag">LangChain</span>
        <span class="tag">HuggingFace</span>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("🚀 Launch App", "https://sheemszzz-langchain-pdf.streamlit.app/", use_container_width=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>🕵️ AI Web Research Agent</h3>
        <p>Autonomous AI agent that searches the web across multiple queries and 
        generates comprehensive structured research reports on any topic.</p>
        <br>
        <span class="tag">AI Agents</span>
        <span class="tag">Tavily Search</span>
        <span class="tag">LangChain</span>
        <span class="tag">Groq</span>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("🚀 Launch App", "https://langchain-sheemsz-research-agent.streamlit.app/", use_container_width=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>🗄️ SQL Database Chatbot</h3>
        <p>Chat with databases in plain English — no SQL knowledge needed! 
        Automatically converts natural language to SQL and explains results conversationally.</p>
        <br>
        <span class="tag">NL to SQL</span>
        <span class="tag">SQLite</span>
        <span class="tag">LangChain</span>
        <span class="tag">Pandas</span>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("🚀 Launch App", "https://langchain-sheemsz-sql-chat.streamlit.app/", use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Tech Stack
st.markdown('<h2 class="section-title">🛠️ Tech Stack</h2>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
techs = [
    ("🦜", "LangChain", "AI Framework"),
    ("⚡", "Groq + LLaMA", "LLM Provider"),
    ("🧠", "FAISS", "Vector Search"),
    ("🔍", "Tavily", "Web Search"),
    ("🌐", "Streamlit", "UI Framework"),
]
for col, (icon, name, desc) in zip([col1, col2, col3, col4, col5], techs):
    with col:
        st.markdown(f"""
        <div class="card" style="text-align:center">
            <div style="font-size:2em">{icon}</div>
            <h3 style="text-align:center">{name}</h3>
            <p style="text-align:center">{desc}</p>
        </div>""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; color:#555; padding:20px">
    <p>Built with ❤️ using LangChain, Groq & Streamlit</p>
    <p>
        <a href="https://github.com/sheemasaba24/langchain-portfolio" 
           style="color:#00d2ff; text-decoration:none">
           🐙 View on GitHub
        </a>
    </p>
</div>
""", unsafe_allow_html=True)