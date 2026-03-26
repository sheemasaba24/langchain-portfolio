import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage

from datetime import datetime


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
st.set_page_config(page_title="AI Research Agent", page_icon="🕵️", layout="wide")
st.title("🕵️ AI Web Research Agent")
st.markdown("Give me any topic — I'll search the web and write a full research report!")

if "reports" not in st.session_state:
    st.session_state.reports = []

# Sidebar
with st.sidebar:
    st.header("📋 Research History")
    if st.session_state.reports:
        for i, r in enumerate(reversed(st.session_state.reports)):
            st.markdown(f"**{i+1}.** {r['topic'][:40]}...")
        st.markdown("---")
        all_reports = "\n\n" + "="*60 + "\n\n".join(
            [f"Topic: {r['topic']}\n\n{r['report']}" for r in st.session_state.reports]
        )
        st.download_button(
            label="📥 Download All Reports",
            data=all_reports,
            file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )
    else:
        st.info("No research done yet!")

# Main input
topic = st.text_input(
    "🔍 What do you want to research?",
    placeholder="e.g. Latest developments in quantum computing 2026"
)

col1, col2 = st.columns([1, 4])
with col1:
    depth = st.selectbox("Search Depth", ["Basic", "Detailed", "Deep"])

search_count = {"Basic": 3, "Detailed": 5, "Deep": 8}[depth]

if st.button("🚀 Start Research", type="primary"):
    if not topic:
        st.warning("Please enter a topic first!")
    else:
        llm = ChatGroq(model="llama-3.3-70b-versatile")
        search_tool = TavilySearchResults(max_results=search_count)

        with st.status("🔍 Agent is researching...", expanded=True) as status:
            try:
                # Step 1: Generate smart search queries
                st.write("🤔 Planning search strategy...")
                query_prompt = f"""Generate {min(search_count, 4)} different specific search queries to research this topic comprehensively: '{topic}'
Return ONLY the queries, one per line, no numbering or extra text."""
                queries_response = llm.invoke([HumanMessage(content=query_prompt)])
                queries = [q.strip() for q in queries_response.content.strip().split('\n') if q.strip()][:search_count]

                # Step 2: Search for each query
                all_results = []
                for i, query in enumerate(queries):
                    st.write(f"🌐 Searching: *{query}*")
                    results = search_tool.invoke(query)
                    if isinstance(results, list):
                        for r in results:
                            if isinstance(r, dict):
                                all_results.append({
                                    "query": query,
                                    "content": r.get("content", ""),
                                    "url": r.get("url", "")
                                })

                # Step 3: Compile context
                st.write("📝 Writing research report...")
                context = ""
                sources = []
                for r in all_results:
                    context += f"\nSource: {r['url']}\n{r['content']}\n---\n"
                    if r['url'] not in sources:
                        sources.append(r['url'])

                # Step 4: Generate final report
                report_prompt = f"""You are an expert research analyst. Based on the search results below, write a comprehensive research report about: '{topic}'

Search Results:
{context}

Write a well-structured report with these sections:
## 📌 Overview
## 🔍 Key Findings
## 📊 Details & Analysis
## 🔮 Future Outlook
## 📚 Sources

Today's date: {datetime.now().strftime('%B %d, %Y')}
Be detailed, specific, and professional. Include relevant facts and data from the search results."""

                report_response = llm.invoke([HumanMessage(content=report_prompt)])
                report = report_response.content
                status.update(label="✅ Research Complete!", state="complete")

            except Exception as e:
                status.update(label="❌ Error occurred", state="error")
                st.error(f"Error: {str(e)}")
                report = None

        if report:
            st.markdown("---")
            st.markdown(f"## 📝 Research Report: {topic}")
            st.markdown(f"*Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}*")
            st.markdown("---")
            st.markdown(report)

            st.session_state.reports.append({
                "topic": topic,
                "report": report,
                "date": datetime.now().strftime('%Y-%m-%d %H:%M')
            })

            st.download_button(
                label="📥 Download This Report",
                data=f"Research Report: {topic}\nDate: {datetime.now().strftime('%B %d, %Y')}\n\n{report}",
                file_name=f"report_{topic[:30].replace(' ', '_')}.txt",
                mime="text/plain"
            )