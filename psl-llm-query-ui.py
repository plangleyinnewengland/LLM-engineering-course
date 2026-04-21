import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

openrouter = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=openrouter_api_key)

MODELS = {
    "Llama 3.3 70B (free)": "meta-llama/llama-3.3-70b-instruct:free",
    "Llama 3.2 3B (free)": "meta-llama/llama-3.2-3b-instruct:free",
    "Gemini 2.5 Flash": "google/gemini-2.5-flash",
    "Claude Sonnet 4": "anthropic/claude-sonnet-4",
    "GPT-4.1 Mini": "openai/gpt-4.1-mini",
    "DeepSeek V3.1": "deepseek/deepseek-chat-v3.1",
}

st.set_page_config(page_title="LLM Query", page_icon="🤖")
st.title("🤖 LLM Query")
st.caption("Ask any question and choose which model answers it")

selected_model = st.selectbox("Select a model", list(MODELS.keys()))

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"Querying {selected_model}..."):
            try:
                response = openrouter.chat.completions.create(
                    model=MODELS[selected_model],
                    messages=st.session_state.messages,
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"⚠️ Error from {selected_model}: {e}"
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
