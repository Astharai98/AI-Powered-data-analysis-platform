import streamlit as st

def render_chat(chat_history):
    for query, response in reversed(chat_history):
        st.markdown(f"**🧑 You:** {query}")
        st.markdown(f"**🤖 AI:** {response}")
        st.markdown("---")
