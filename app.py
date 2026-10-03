import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="NovaChat AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stChatInput {
        position: fixed;
        bottom: 0;
        background-color: white;
        padding-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 NovaChat AI")
st.caption("Ton assistant ultra-intelligent, rapide et stylé")

# Mets ta vraie clé API Groq entre les guillemets ci-dessous :
api_key = "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"

system_prompt = {
    "role": "system", 
    "content": "Tu t'appelles NovaChat AI. Tu es un assistant virtuel extrêmement intelligent, cultivé, créatif et serviable, créé pour aider l'utilisateur. Réponds toujours de manière claire, structurée et détaillée en français. Ne dis jamais que tu es ChatGPT ou un modèle OpenAI."
}

if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

with st.sidebar:
    st.header("💬 Discussion")
    
    if st.button("➕ Nouvelle discussion", use_container_width=True):
        st.session_state.messages = [system_prompt]
        st.rerun()
        
    st.markdown("---")
    st.subheader("⚙️ Options & Médias")
    uploaded_file = st.file_uploader("Importer une image", type=["jpg", "jpeg", "png"])
    
    st.markdown("---")
    st.markdown("Propulsé par **NovaChat AI**")

if not api_key or api_key == "mets_ta_cle_groq_ici":
    st.warning("⚠️ Veuillez configurer votre clé API Groq dans le code source.")
else:
    client = Groq(api_key=api_key)

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Image importée", width=250)

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if user_prompt := st.chat_input("Envoyez un message à NovaChat..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("NovaChat réfléchit..."):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=st.session_state.messages,
                        model="openai/gpt-oss-20b",
                    )
                    response_text = chat_completion.choices[0].message.content
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    st.error(f"Une erreur est survenue : {e}")
