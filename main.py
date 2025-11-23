import streamlit as st
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ")

st.set_page_config(page_title="Layasaran LLM", page_icon="✨", layout="centered")

st.markdown("""
<style>
    .title {
        font-size: 38px;
        font-weight: 700;
        text-align: center;
        padding-top: 30px;
        color: #e0e0e0;
    }
    .subtitle {
        text-align: center;
        font-size: 16px;
        margin-top: -10px;
        margin-bottom: 40px;
        color: #b0b0b0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>✨ Layasaran Language Model ✨</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Experience fast and intelligent AI responses powered by Layasaran intelligent</div>",
            unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

llm = ChatGroq(model="llama-3.1-8b-instant")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Your Message")

if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    response = llm.invoke(user_input)
    reply = response.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
