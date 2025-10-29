import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Talk to Paintings 🎨")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🖼️ Talk to a Painting")

painting_name = st.selectbox("Choose a painting:", ["Mona Lisa", "The Starry Night", "The Scream"])
persona = f"You are the painting '{painting_name}'. Speak in its tone, style, and era."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": persona}]

# Display messages
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.chat_message("user", avatar="🧑‍🎨").markdown(msg["content"])
    else:
        st.chat_message("assistant", avatar="🖌️").markdown(msg["content"])

# Input box
if user_input := st.chat_input("Ask the painting something..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user", avatar="🧑‍🎨").markdown(user_input)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )
    reply = response.choices[0].message.content

    st.chat_message("assistant", avatar="🎨").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
