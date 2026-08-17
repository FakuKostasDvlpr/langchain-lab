"""04 - Chatbot avanzado: streaming, configuracion en vivo y prompt template.

Suma tres cosas sobre el ejercicio 03:

1. Streaming: `cadena.stream()` devuelve la respuesta por pedazos en vez de
   esperar a que el modelo termine. Baja mucho la latencia percibida.
2. Panel de configuracion: modelo, temperatura y personalidad editables sin
   reiniciar la app.
3. El historial entra como texto dentro de un `PromptTemplate`, en vez de ir
   como lista de mensajes. Sirve para ver la diferencia entre las dos formas
   de dar contexto (ver README).

Correr con:  streamlit run 04-chatbot-avanzado/app.py
"""

import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

MODELOS = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]

st.set_page_config(page_title="Chatbot avanzado", page_icon="🤖", layout="centered")
st.title("🤖 Chatbot avanzado")
st.caption("LangChain + Streamlit · streaming y configuración en vivo")

if not os.getenv("GOOGLE_API_KEY"):
    st.error("Falta `GOOGLE_API_KEY`. Copiá `.env.example` a `.env` y completala.")
    st.stop()

with st.sidebar:
    st.header("⚙️ Configuración")

    modelo_default = os.getenv("GEMINI_MODEL", MODELOS[0])
    indice = MODELOS.index(modelo_default) if modelo_default in MODELOS else 0

    modelo = st.selectbox("Modelo", MODELOS, index=indice)
    temperatura = st.slider(
        "Temperatura", 0.0, 1.0, 0.5, 0.1,
        help="0 = respuestas predecibles · 1 = más creativas y variables",
    )
    personalidad = st.text_area(
        "Personalidad del asistente",
        value="Sos un asistente útil y amigable. Respondés claro y conciso, en español.",
        height=100,
    )

    st.divider()
    if st.button("🗑️ Nueva conversación", use_container_width=True):
        st.session_state.mensajes = []
        st.rerun()

# El modelo se reconstruye en cada rerun, asi que toma los valores del sidebar
# apenas se mueven los controles.
chat_model = ChatGoogleGenerativeAI(model=modelo, temperature=temperatura)

plantilla = PromptTemplate(
    input_variables=["personalidad", "historial", "mensaje"],
    template=(
        "{personalidad}\n\n"
        "Historial de la conversación:\n"
        "{historial}\n\n"
        "Usuario: {mensaje}\n"
        "Asistente: "
    ),
)

cadena = plantilla | chat_model

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


def formatear_historial(mensajes) -> str:
    """Convierte la lista de mensajes en texto plano para el prompt.

    Sin esto, meter la lista directo en el template la renderiza con el repr de
    Python (`[HumanMessage(content=...)]`), que el modelo interpreta mal.
    """
    if not mensajes:
        return "(todavía no hay mensajes previos)"
    lineas = []
    for m in mensajes:
        rol = "Asistente" if isinstance(m, AIMessage) else "Usuario"
        lineas.append(f"{rol}: {m.content}")
    return "\n".join(lineas)


for msg in st.session_state.mensajes:
    rol = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(rol):
        st.markdown(msg.content)

pregunta = st.chat_input("Escribí tu mensaje...")

if pregunta:
    # El historial se captura ANTES de sumar la pregunta actual: el mensaje nuevo
    # va en su propia variable del template, no duplicado dentro del historial.
    historial = formatear_historial(st.session_state.mensajes)

    with st.chat_message("user"):
        st.markdown(pregunta)

    try:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            respuesta_completa = ""

            for chunk in cadena.stream(
                {
                    "personalidad": personalidad,
                    "historial": historial,
                    "mensaje": pregunta,
                }
            ):
                respuesta_completa += chunk.content
                placeholder.markdown(respuesta_completa + "▌")  # cursor de "escribiendo"

            placeholder.markdown(respuesta_completa)

        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=respuesta_completa))

    except Exception as e:
        st.error(f"Error al generar la respuesta: {e}")
        st.info("Revisá que la API key sea válida y que el modelo elegido esté disponible.")
