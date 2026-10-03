import streamlit as st
from groq import Groq

# Configuration de la page (largeur, titre, icône)
st.set_page_config(
    page_title="NovaChat AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé pour ressembler à ChatGPT (bulles de chat, design propre)
st.markdown("""
    <style>
    .stChatInput {
        position: fixed;
        bottom: 0;
        background-color: white;
        padding-bottom: 20px;
    }
    /* Style pour les messages */
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex; flex-direction: row; align-items: flex-start;
    }
    </style>
""", unsafe_allow_html=True)

# Titre principal discret et élégant
st.title("🤖 NovaChat AI")
st.caption("Votre assistant intelligent, rapide et stylé")

# Mets ta clé API Groq valide ici
api_key = "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"

# Initialisation de l'historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Barre latérale (Sidebar) - Style ChatGPT (historique / options)
with st.sidebar:
    st.header("💬 Discussion")
    
    # Bouton pour nouvelle discussion / effacer
    if st.button("➕ Nouvelle discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.subheader("⚙️ Options & Médias")
    
    # Option d'importation d'image (façon bouton "+" de ChatGPT)
    uploaded_file = st.file_uploader("Importer une image", type=["jpg", "jpeg", "png"])
    
    st.markdown("---")
    st.markdown("Propulsé par **Groq & Llama**")

# Vérification de la clé API
if not api_key or api_key == "TA_CLE_API_GROQ_ICI":
    st.warning("⚠️ Veuillez configurer votre clé API Groq dans le code source.")
else:
    client = Groq(api_key=api_key)

    # Affichage de l'image si elle a été importée
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Image importée pour analyse", width=250)

    # Affichage de tout l'historique de la conversation
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Zone de saisie du message en bas (comme ChatGPT)
    if user_prompt := st.chat_input("Envoyez un message à NovaChat..."):
        
        # Ajout du message utilisateur
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Génération de la réponse de l'assistant avec l'historique complet
        with st.chat_message("assistant"):
            with st.spinner("NovaChat réfléchit..."):
                try:
                    # Appel à l'API Groq avec le modèle rapide et performant
                    chat_completion = client.chat.completions.create(
                        messages=st.session_state.messages,
                        model="openai/gpt-oss-20b",
                    )
                    response_text = chat_completion.choices[0].message.content
                    st.markdown(response_text)
                    
                    # Ajout de la réponse dans l'historique
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    st.error(f"Une erreur est survenue : {e}")
