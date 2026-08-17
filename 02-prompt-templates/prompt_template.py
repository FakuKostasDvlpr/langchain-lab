"""02 - Prompt templates y LCEL.

Dos conceptos:

1. `PromptTemplate` separa la *forma* del prompt de los *datos* que lo llenan.
   En vez de pegar strings con f-strings desparramados por el codigo, el prompt
   queda en un solo lugar y las variables se inyectan al invocar.

2. LCEL (LangChain Expression Language): el operador `|` encadena componentes.
   `plantilla | chat` arma un pipeline "datos -> prompt renderizado -> modelo".
   Cada eslabon recibe la salida del anterior.

Correr con:  python 02-prompt-templates/prompt_template.py
"""

import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

MODELO = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

chat = ChatGoogleGenerativeAI(model=MODELO, temperature=0.7)

plantilla = PromptTemplate(
    input_variables=["nombre", "idioma"],
    template=(
        "Sos un asistente breve y amigable.\n"
        "Saluda al usuario en {idioma}, en una sola oracion.\n"
        "Nombre del usuario: {nombre}\n"
        "Asistente: "
    ),
)

# El pipeline: dict -> PromptTemplate -> ChatGoogleGenerativeAI -> AIMessage
cadena = plantilla | chat

for datos in [
    {"nombre": "Carlos", "idioma": "espanol"},
    {"nombre": "Ana", "idioma": "italiano"},
]:
    resultado = cadena.invoke(datos)
    print(f"{datos['nombre']} ({datos['idioma']}): {resultado.content}")
