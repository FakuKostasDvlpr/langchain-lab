"""03 - Chatbot con memoria de conversacion.

El salto respecto de los ejercicios anteriores: el modelo por si solo no recuerda
nada entre llamadas. La "memoria" es simplemente que le mandamos la lista completa
de mensajes previos en cada invoke().

Streamlit reejecuta el script entero en cada interaccion, asi que una lista comun
se perderia. `st.session_state` es lo unico que sobrevive entre reruns.

Correr con:  streamlit run 03-chatbot-streamlit/app.py
"""

import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

MODELO = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

st.set_page_config(page_title="Chatbot con LangChain", page_icon="💬")
st.title("💬 Chatbot con memoria")
st.caption(f"LangChain + Streamlit + {MODELO}")

def obtener_api_key() -> str | None:
    """Busca la API key en los dos lugares donde puede estar.

    Local: variable de entorno, cargada del .env por load_dotenv().
    Streamlit Cloud: panel de Secrets, accesible via st.secrets.

    Acceder a st.secrets sin que exista un secrets.toml lanza excepcion, por eso
    va en try. Asi el mismo codigo corre en los dos lados sin ramas por entorno.
    """
    if clave := os.getenv("GOOGLE_API_KEY"):
        return clave
    try:
        return st.secrets["GOOGLE_API_KEY"]
    except Exception:
        return None


api_key = obtener_api_key()
if not api_key:
    st.error(
        "Falta `GOOGLE_API_KEY`. En local: copiá `.env.example` a `.env` y completala. "
        "En Streamlit Cloud: cargala en *Settings → Secrets*."
    )
    st.stop()

chat_model = ChatGoogleGenerativeAI(
    model=MODELO, temperature=0.7, google_api_key=api_key
)

# Historial persistente entre reruns de Streamlit.
# El SystemMessage define la personalidad y se manda al modelo, pero no se muestra.
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        SystemMessage(content="Sos un asistente amable y conciso. Respondes en español.")
    ]

# Redibujar la conversacion previa (Streamlit parte de cero en cada rerun).
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        continue
    rol = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(rol):
        st.markdown(msg.content)

pregunta = st.chat_input("Escribí tu mensaje...")

if pregunta:
    st.session_state.mensajes.append(HumanMessage(content=pregunta))
    with st.chat_message("user"):
        st.markdown(pregunta)

    try:
        # Se manda TODO el historial: ahí está la memoria.
        respuesta = chat_model.invoke(st.session_state.mensajes)
        st.session_state.mensajes.append(respuesta)
        with st.chat_message("assistant"):
            st.markdown(respuesta.content)
    except Exception as e:
        # Si falla, saco el mensaje del usuario para no dejar el historial
        # con una pregunta que nunca tuvo respuesta.
        st.session_state.mensajes.pop()
        st.error(f"Error al generar la respuesta: {e}")

if len(st.session_state.mensajes) > 1 and st.button("🗑️ Nueva conversación"):
    del st.session_state.mensajes
    st.rerun()
