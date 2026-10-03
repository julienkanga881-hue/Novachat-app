import streamlit as st
from groq import Groq

st.set_page_config(page_title="NovaChat AI", page_icon="🤖", layout="centered")

st.title("🤖 NovaChat AI")
st.caption("Ton assistant IA intelligent, rapide et stylé")

# Mets ta clé API Groq entre les guillemets ci-dessous
api_key = "gsk_Z7uzFhLFAQsD9JSiltSIIWGdyb3FYvNS8oq5nsI1Z071v2LLYtRCP"

# Initialisation de l'historique des messages dans la session Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Barre latérale (Sidebar) pour les options et fonctionnalités supplémentaires
with st.sidebar:
    st.header("⚙️ Options")
    
    # Bouton pour effacer la discussion
    if st.button("🗑️ Effacer la discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.info("💡 **Astuce :** Tu peux utiliser la caméra ci-dessous pour capturer ou importer une image à analyser !")

if not api_key or api_key == "mets_ta_cle_groq_ici":
    st.warning("⚠️ Veuillez configurer votre clé API Groq.")
else:
    client = Groq(api_key=api_key)

    # Option de prise de photo ou d'importation d'image
    st.subheader("📷 Ajouter une image (optionnel)")
    uploaded_file = st.camera_input("Prendre une photo")
    
    # Si aucune photo via la caméra, on propose d'importer un fichier image
    if uploaded_file is None:
        uploaded_file = st.file_uploader("Ou importer une image", type=["jpg", "jpeg", "png"])

    # Affichage de l'historique des messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Champ de saisie du message utilisateur
    if user_prompt := st.chat_input("Pose ta question à NovaChat..."):
        # Ajout du message utilisateur à l'historique
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Génération de la réponse par l'assistant
        with st.chat_message("assistant"):
            with st.spinner("Réflexion en cours..."):
                try:
                    # Appel à l'API Groq (en envoyant l'historique des messages pour garder le contexte)
                    chat_completion = client.chat.completions.create(
                        messages=st.session_state.messages,
                        model="openai/gpt-oss-20b",
                    )
                    response_text = chat_completion.choices[0].message.content
                    st.markdown(response_text)
                    
                    # Ajout de la réponse de l'assistant à l'historique
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    st.error(f"Une erreur est survenue : {e}")
