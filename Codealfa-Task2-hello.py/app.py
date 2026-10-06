"""
FAQ Chatbot - Streamlit Web UI (Optional part of Task 2)
Run with: streamlit run app.py
"""

import streamlit as st
from chatbot import FAQChatbot

st.set_page_config(page_title="FAQ Chatbot", page_icon="🤖")

st.title("🤖 FAQ Chatbot")
st.caption("CodeAlpha AI Internship — Task 2")

# Load the chatbot once and cache it across reruns
@st.cache_resource
def load_bot():
    return FAQChatbot("faq_data.json")

bot = load_bot()

# Keep chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask a question...")

if user_input:
    answer = bot.get_answer(user_input)
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("bot", answer))

for role, message in st.session_state.chat_history:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.write(message)

with st.sidebar:
    st.subheader("Sample questions to try")
    for q in bot.questions[:6]:
        st.markdown(f"- {q}")
