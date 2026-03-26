from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
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

llm = ChatGroq(model="llama-3.3-70b-versatile")

chat_history = []  # this stores the full conversation

print("Chatbot ready! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    chat_history.append(HumanMessage(content=user_input))

    response = llm.invoke(chat_history)

    chat_history.append(AIMessage(content=response.content))

    print(f"\nBot: {response.content}\n")