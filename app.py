import streamlit as st
from groq import Groq

st.set_page_config(page_title="NovaChat AI", page_icon="🤖", layout="centered")

st.title("🤖 NovaChat AI")
st.caption("Ton assistant IA intelligent, rapide et stylé")

# Mets ta clé API Groq entre les guillemets ci-dessous
api_key = "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"

if not api_key or api_key == "mets_ta_cle_groq_ici":
    st.warning("⚠️ Veuillez configurer votre clé API Groq.")
else:
    client = Groq(api_key=api_key)

    user_prompt = st.chat_input("Pose ta question à NovaChat...")

    if user_prompt:
        with st.chat_message("user"):
            st.write(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Réflexion en cours..."):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": user_prompt,
                            }
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    response_text = chat_completion.choices[0].message.content
                    st.write(response_text)
                except Exception as e:
                    st.error(f"Une erreur est survenue : {e}")
