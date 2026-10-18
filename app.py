import streamlit as st
from google import genai

# Configuration de la page Streamlit
st.set_page_config(
    page_title="NovaChat AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 🎨 DESIGN CSS AVANCÉ (Style Gemini & ChatGPT combinés)
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
        padding: 1rem 1.2rem;
        border-radius: 14px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        line-height: 1.6;
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

    /* En-tête personnalisé */
    .chat-header {
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 1px solid #333538;
        margin-bottom: 2rem;
    }
    .chat-header h1 {
        font-size: 2.5rem;
        background: linear-gradient(90deg, #4285F4, #9B72CF, #D96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .chat-header p {
        color: #8e918f;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# En-tête visuel de l'application
st.markdown("""
    <div class="chat-header">
        <h1>NovaChat AI</h1>
        <p>L'alliance parfaite de la précision et de l'élégance</p>
    </div>
""", unsafe_allow_html=True)

# Barre latérale (Sidebar) pour les paramètres et options
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=65)
    st.title("NovaChat Control")
    st.markdown("---")
    
    # Choix du modèle
    model_choice = st.selectbox(
        "Modèle IA", 
        ["gemini-1.5-flash", "gemini-1.5-pro"],
        help="Sélectionne la version du modèle Google GenAI"
    )
    
    st.markdown("---")
    
    # Bouton pour effacer l'historique
    if st.button("🗑️ Nouvelle conversation", type="primary", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Bonjour ! Je suis NovaChat. Comment puis-je vous aider aujourd'hui ?"}
        ]
        st.rerun()
        
    st.markdown("""
        <div style='position: fixed; bottom: 20px; color: #8e918f; font-size: 0.8rem;'>
            Propulsé par Google GenAI & Streamlit<br>
            Design personnalisé v2.0
        </div>
    """, unsafe_allow_html=True)

# Initialisation de l'historique des messages dans la session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour ! Je suis NovaChat. Comment puis-je vous aider aujourd'hui ?"}
    ]

# Affichage de l'historique des messages de la conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Gestion de la saisie utilisateur et appel API
if prompt := st.chat_input("Posez votre question à NovaChat..."):
    # Ajout du message utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Génération de la réponse de l'IA avec le client Google GenAI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("✨ *NovaChat réfléchit...*")
        
        try:
            # 🔑 Insère ta clé API Google AI Studio ci-dessous
            my_api_key = "AQ.Ab8RN6LEzcBmRad1ux4EtqOfMazvNzjpHUrqvYaGZ2To23o8Rw" 
            
            client = genai.Client(api_key=my_api_key)
            
            # Appel API avec consignes expertes (style Gemini + ChatGPT)
            response = client.models.generate_content(
                model=model_choice,
                contents=prompt,
                config={
                    'system_instruction': (
                        "Tu es NovaChat, un assistant virtuel de pointe développé par Julien Kanga. "
                        "Tu combines la structure claire et rigoureuse de ChatGPT avec la fluidité et l'intelligence de Gemini. "
                        "Utilise systématiquement des listes à puces, du texte en gras pour les notions clés, et structure "
                        "tes explications de manière claire, professionnelle et détaillée."
                    )
                }
            )
            ai_response = response.text
        except Exception as e:
            ai_response = f"⚠️ Une erreur est survenue lors de la communication avec l'API : `{e}`"
            
        message_placeholder.markdown(ai_response)
        
    # Ajout de la réponse de l'assistant à l'historique
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
