import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Talk to Paintings 🎨")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

painting_name = st.selectbox("Choose a painting:", ["Mona Lisa", "The Scream"])
persona = f"You are the painting '{painting_name}'. Speak like it would."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": persona}]

for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).markdown(msg["content"])

if user_input := st.chat_input("Ask the painting something..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)
