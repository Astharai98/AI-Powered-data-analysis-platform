import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from utils import render_chat

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI setup
st.set_page_config(page_title="AI Data Analyzer", layout="wide")
st.title("📊 AI-Powered Data Analysis")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())

    # Convert a preview of the dataframe to string context
    df_preview = df.head(10).to_markdown(index=False)

    # Initialize the LLM
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o", openai_api_key=openai_api_key)

    st.subheader("🔍 Ask questions about your data")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    query = st.text_input("Type your question")

    if query:
        with st.spinner("Analyzing..."):
            try:
                # Build context-aware prompt
                prompt_template = ChatPromptTemplate.from_messages([
                    ("system", "You are a data analyst. Answer questions based on the following CSV data:\n\n{table}"),
                    ("human", "{question}")
                ])
                prompt = prompt_template.format_messages(table=df_preview, question=query)

                # Call the model
                response = llm.invoke(prompt)

                # Save to chat history
                st.session_state.chat_history.append((query, response.content))
                st.success("Response generated!")
            except Exception as e:
                st.error(f"Error: {e}")

    render_chat(st.session_state.chat_history)
