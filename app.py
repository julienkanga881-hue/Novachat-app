import streamlit as st
from google import genai

# Configuration de la page
st.set_page_config(page_title="NovaChat AI", page_icon="🤖", layout="centered")

st.title("🤖 NovaChat AI")
st.caption("Ton assistant IA intelligent, rapide et stylé")

# Ta clé API
GEMINI_API_KEY = "AQ.Ab8RN6JTf..." # Remets ta clé API ici
client = genai.Client(api_key=GEMINI_API_KEY)

# Initialisation de l'IA et de l'historique
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model='gemini-2.5-flash',
        config={
            "system_instruction": "Tu es NovaChat, une IA ultra-rapide, moderne, amicale et intelligente. Tu réponds de manière dynamique et bien structurée."
        }
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des anciens messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Barre de saisie
if prompt := st.chat_input("Pose ta question à NovaChat..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("NovaChat réfléchit..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                reponse_txt = response.text
            except Exception as e:
                reponse_txt = f"⚠️ Erreur : {e}"
            
            st.markdown(reponse_txt)
            st.session_state.messages.append({"role": "assistant", "content": reponse_txt})