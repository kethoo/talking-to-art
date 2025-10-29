import streamlit as st
from openai import OpenAI
import tempfile

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="Talk to a Painting 🎨", page_icon="🖼️")
st.title("🖌️ Talk to a Painting")

# Initialize OpenAI client (uses Streamlit Secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.write("Talk to any artwork — even one from your imagination. Now it can talk back to you!")

# -----------------------
# Painting Input Section
# -----------------------
col1, col2 = st.columns([3, 2])

with col1:
    painting_name = st.text_input("🎨 Name of the artwork", placeholder="e.g. The Whispering Shadows")
with col2:
    artist_name = st.text_input("🧑‍🎨 by (optional)", placeholder="e.g. Lara Mendez")

# -----------------------
# If painting name entered
# -----------------------
if painting_name:
    if artist_name:
        st.markdown(f"### 🖼️ *{painting_name}* by **{artist_name}**")
    else:
        st.markdown(f"### 🖼️ *{painting_name}*")

    painting_persona = (
        f"You are the painting '{painting_name}'"
        + (f", created by {artist_name}" if artist_name else "")
        + f". Speak as if you are {painting_name} — express your tone, mood, era, and artistic essence."
    )

    # Initialize conversation
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": painting_persona}]

    # Display conversation history
    for msg in st.session_state.messages[1:]:
        if msg["role"] == "user":
            st.chat_message("user", avatar="🧑‍🎨").markdown(msg["content"])
        else:
            st.chat_message("assistant", avatar="🎨").markdown(msg["content"])

    # Chat input
    if user_input := st.chat_input("Ask the painting something..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user", avatar="🧑‍🎨").markdown(user_input)

        with st.spinner("The painting is thinking... 🎨"):
            # Generate response (limit to 4 sentences)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages + [
                    {"role": "system", "content": "Answer in at most 4 sentences, like a painting speaking with emotion and brevity."}
                ]
            )
            reply = response.choices[0].message.content

        st.chat_message("assistant", avatar="🖌️").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

        # -----------------------
        # 🎙️ Generate speech from reply
        # -----------------------
        with st.spinner("🎧 Generating the painting's voice..."):
            speech_response = client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="alloy",  # options: "verse", "coral"
                input=reply
            )

            # Save and play audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
                speech_response.stream_to_file(tmp_audio.name)
                st.audio(tmp_audio.name, format="audio/mp3")

else:
    st.info("👆 Enter the name of a painting to begin chatting.")
