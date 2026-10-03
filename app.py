Import os
import streamlit as st
from google import genai

# Configuration de la page
st.set_page_config(page_title="NovaChat AI", page_icon="🤖", layout="centered")

st.title("🤖 NovaChat AI")
st.caption("Ton assistant IA intelligent, rapide et stylé")

# Récupération de la clé API
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("La clé API GEMINI_API_KEY est manquante dans les Secrets.")
    st.stop()

# Barre latérale (Sidebar) pour les options
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    # Choix de la personnalité
    persona = st.selectbox(
        "Rôle de l'assistant :",
        ["Assistant général et utile", "Expert en programmation (Code)", "Rédacteur créatif et littéraire"]
    )
    
    st.markdown("---")
    
    # Bouton pour effacer l'historique
    if st.button("🗑️ Effacer la discussion"):
        st.session_state.messages = []
        st.rerun()

# Initialisation de l'historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique des messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Gestion de l'entrée utilisateur
if prompt := st.chat_input("Pose ta question à NovaChat..."):
    # Ajout du message utilisateur à l'état
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Initialisation du client GenAI
    client = genai.Client(api_key=api_key)

    # Ajustement des instructions selon le rôle choisi
    system_instruction = "Tu es NovaChat, un assistant IA utile, moderne et chaleureux."
    if persona == "Expert en programmation (Code)":
        system_instruction = "Tu es un expert en programmation informatique. Fournis des explications claires et du code propre."
    elif persona == "Rédacteur créatif et littéraire":
        system_instruction = "Tu es un écrivain et rédacteur extrêmement créatif. Soigne ton style d'écriture."

    # Appel au modèle avec consigne système et message
    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours..."):
            try:
                # Utilisation de contents avec la consigne système intégrée
                full_prompt = f"[{system_instruction}]\n\nUtilisateur : {prompt}"
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=full_prompt
                )
                bot_reply = response.text
                st.markdown(bot_reply)
                
                # Enregistrement de la réponse dans l'historique
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"Erreur : {e}")
