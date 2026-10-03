import os
import streamlit as st
from google import genai

st.set_page_config(page_title="NovaChat AI", page_icon="🤖")
st.title("🤖 NovaChat AI")
st.caption("Ton assistant IA intelligent, rapide et stylé")

api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("La clé API GEMINI_API_KEY est manquante dans les Secrets.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Pose ta question à NovaChat..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = genai.Client(api_key=api_key)

    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )
                bot_reply = response.text
                st.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"Erreur : {e}")
