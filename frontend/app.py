import streamlit as st

from src.agent import Agent
from src.memory import memory

st.set_page_config(page_title="Support Agent Chat", page_icon="💬", layout="wide")

st.title("Support Agent Chat")
st.markdown("Talk with the autonomous customer support agent in a simple chat UI.")

if "session_id" not in st.session_state:
    st.session_state.session_id = "default-session"

if "customer_id" not in st.session_state:
    st.session_state.customer_id = "customer_123"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = memory.get(st.session_state.session_id)

agent = Agent()

with st.sidebar:
    st.header("Session settings")
    session_id = st.text_input("Session ID", value=st.session_state.session_id)
    customer_id = st.text_input("Customer ID", value=st.session_state.customer_id)
    if st.button("Reset chat"):
        memory.sessions.pop(session_id, None)
        st.session_state.chat_history = []
        st.rerun()

st.session_state.session_id = session_id
st.session_state.customer_id = customer_id
st.session_state.chat_history = memory.get(session_id)

with st.form(key="chat_form", clear_on_submit=False):
    user_message = st.text_area("Your message", key="user_input", height=120)
    submitted = st.form_submit_button("Send")

    if submitted and user_message.strip():
        reply = agent.run(st.session_state.customer_id, user_message.strip(), memory.get(session_id))
        memory.add(session_id, user_message.strip(), reply)
        st.session_state.chat_history = memory.get(session_id)
        st.rerun()

st.divider()

if st.session_state.chat_history:
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Agent:** {message['content']}")
else:
    st.info("Send a message to begin the chat.")
