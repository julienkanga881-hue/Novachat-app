import streamlit as st
from google import genai

# Configuration de la page Streamlit
st.set_page_config(
    page_title="NovaChat AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 🎨 DESIGN CSS PERSONNALISÉ (Style Gemini & ChatGPT combinés)
st.markdown("""
<style>
    /* Style global de l'application */
    .main {
        background-color: #131314;
        color: #e3e3e3;
    }
    
    /* Masquer le menu par défaut et le footer Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Style des bulles de messages */
    .stChatMessage {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
        line-height: 1.5;
    }
    
    /* Message de l'utilisateur */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #1e1f20;
        border: 1px solid #333538;
    }
    
    /* Message de l'assistant AI */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #2b2d31;
        border: 1px solid #3f4248;
    }

    /* Style de la zone de saisie en bas */
    .stChatInputContainer {
        padding-bottom: 1rem;
    }
    
    /* En-tête personnalisé */
    .chat-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 1px solid #333538;
        margin-bottom: 2rem;
    }
    .chat-header h1 {
        font-size: 2.2rem;
        background: linear-gradient(90deg, #4285F4, #9B72CF, #D96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    .chat-header p {
        color: #8e918f;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# En-tête visuel de l'application
st.markdown("""
    <div class="chat-header">
        <h1>NovaChat AI</h1>
        <p>Votre assistant intelligent, rapide et élégant</p>
    </div>
""", unsafe_allow_html=True)

# Barre latérale (Sidebar) pour les paramètres
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=70)
    st.title("Paramètres")
    st.markdown("---")
    
    # Sélection du modèle ou options
    model_choice = st.selectbox("Modèle IA", ["Gemini 2.5 Flash", "Gemini Pro"])
    
    st.markdown("---")
    if st.button("Effacer la conversation", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("<div style='position: fixed; bottom: 20px; color: #8e918f; font-size: 0.8rem;'>Propulsé par Google GenAI & Streamlit</div>", unsafe_allow_html=True)

# Initialisation de l'historique des messages dans la session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour ! Je suis NovaChat. Comment puis-je vous aider aujourd'hui ?"}
    ]

# Affichage de l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Gestion de la saisie utilisateur et appel API
if prompt := st.chat_input("Envoyez un message à NovaChat..."):
    # Ajout du message utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Génération de la réponse de l'IA
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Réflexion en cours...")
        
        try:
            # Connexion au client GenAI (assure-toi d'avoir configuré ta clé API dans les secrets Streamlit)
            client = genai.Client()
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            ai_response = response.text
        except Exception as e:
            ai_response = f"Une erreur est survenue : {e}"
            
        message_placeholder.markdown(ai_response)
        
    # Ajout de la réponse de l'assistant à l'historique
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
