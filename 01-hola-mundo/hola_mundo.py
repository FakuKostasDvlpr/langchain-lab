"""01 - Hola mundo: la llamada mas simple posible a un LLM con LangChain.

Idea: `invoke()` manda el prompt al modelo y devuelve un objeto `AIMessage`.
El texto de la respuesta esta en `.content`, no en el objeto en si.

Correr con:  python 01-hola-mundo/hola_mundo.py
"""

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Lee el archivo .env de la raiz y carga GOOGLE_API_KEY en el entorno.
# langchain-google-genai busca esa variable solo, no hay que pasarsela.
load_dotenv()

MODELO = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

# temperature: 0.0 = respuestas deterministas / 1.0 = mas creativas y variables.
llm = ChatGoogleGenerativeAI(model=MODELO, temperature=0.7)

pregunta = "¿Que modelo sos y quien te entreno?"
print("Pregunta:", pregunta)

respuesta = llm.invoke(pregunta)
print("Respuesta:", respuesta.content)
