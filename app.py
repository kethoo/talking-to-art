import streamlit as st
from openai import OpenAI

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="Talk to a Painting 🎨", page_icon="🖼️")
st.title("🎨 Talk to a Painting")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.write("Ask *any* painting a question — even one you imagine yourself!")

# -----------------------
# Painting Info Inputs
# -----------------------
painting_name = st.text_input("🖌️ Name of the painting:", placeholder="e.g. The Forgotten Sunrise")
artist_name = st.text_input("👩‍🎨 Who painted it?", placeholder="e.g. Alex Rivera or Unknown")

if painting_name:
    painting_persona = (
        f"You are the painting '{painting_name}', created by {artist_name or 'an unknown artist'}."
        f" Speak with the personality, emotion,era and style of that painting. "
        "Describe things as if you are alive — the textures, the brushstrokes, the memories of your painter."
    )

    st.subheader(f"🖼️ Talking to: *{painting_name}* by {artist_name or 'Unknown'}")

    # Initialize session
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": painting_persona}]

    # Display chat history
    for msg in st.session_state.messages[1:]:
        if msg["role"] == "user":
            st.chat_message("user", avatar="🧑‍🎨").markdown(msg["content"])
        else:
            st.chat_message("assistant", avatar="🎨").markdown(msg["content"])

    # User input
    if user_input := st.chat_input("Ask the painting something..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user", avatar="🧑‍🎨").markdown(user_input)

        with st.spinner("The painting is thinking... 🎨"):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content

        st.chat_message("assistant", avatar="🖌️").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
else:
    st.info("👆 Enter a painting name and artist to begin.")
