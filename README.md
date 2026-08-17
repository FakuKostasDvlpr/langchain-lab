# 🧪 LangChain Lab

Recorrido práctico de aprendizaje de **LangChain**, desde la primera llamada a un
LLM hasta un chatbot con memoria, streaming y configuración en vivo.

Cada carpeta es un ejercicio autocontenido con su propio README explicando el
concepto, cómo correrlo y qué se me rompió en el camino.

**Stack:** Python 3.14 · LangChain 0.3 · Google Gemini · Streamlit

---

## Ejercicios

| | Ejercicio | Concepto |
|---|---|---|
| 01 | [Hola mundo](01-hola-mundo/) | Primera llamada a un LLM. `invoke()`, `AIMessage`, `temperature`. |
| 02 | [Prompt templates](02-prompt-templates/) | `PromptTemplate` y composición con LCEL (`\|`). |
| 03 | [Chatbot con memoria](03-chatbot-streamlit/) | Interfaz en Streamlit, `session_state`, historial de conversación. |
| 04 | [Chatbot avanzado](04-chatbot-avanzado/) | Streaming, panel de configuración, historial vía prompt template. |

📓 **[Aprendizajes y problemas resueltos](docs/aprendizajes.md)** — bitácora de los
bugs que me encontré y qué saqué de cada uno.

---

## Puesta en marcha

```bash
git clone https://github.com/FakuKostasDvlpr/langchain-lab.git
cd langchain-lab

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Después, la API key (se saca gratis en [Google AI Studio](https://aistudio.google.com/apikey)):

```bash
cp .env.example .env      # en Windows: copy .env.example .env
# editar .env y completar GOOGLE_API_KEY
```

Y a correr:

```bash
python 01-hola-mundo/hola_mundo.py
python 02-prompt-templates/prompt_template.py
streamlit run 03-chatbot-streamlit/app.py
streamlit run 04-chatbot-avanzado/app.py
```

---

## Tests

Las apps de Streamlit se testean con `AppTest`, el framework oficial: corre la app
con el runtime real, sin servidor ni navegador.

```bash
pip install -r requirements-dev.txt
pytest -v
```

Lo que cubren: que si falta la API key el usuario vea un **mensaje claro y no un
stack trace** (el modo de falla más probable en un deploy público), que `st.stop()`
frene antes de renderizar el chat, y que con credenciales la app arranque limpia.

---

## Deploy

El chatbot avanzado está pensado para desplegarse en
[Streamlit Community Cloud](https://share.streamlit.io):

- **Entrypoint:** `04-chatbot-avanzado/app.py`
- **Dependencias:** `requirements.txt` en la raíz (Cloud lo encuentra solo)
- **Secret:** cargar `GOOGLE_API_KEY = "..."` en *Advanced settings → Secrets*

El código resuelve la credencial desde `os.environ` (local, vía `.env`) o desde
`st.secrets` (Cloud), sin ramas por entorno ni configuración duplicada.

---

## Conceptos que cubre

- **Chat models** y la interfaz uniforme de LangChain (`invoke`, `stream`).
- **LCEL**: componer prompt → modelo → parser con el operador `|`.
- **Memoria conversacional**: por qué un LLM no recuerda nada y qué implica
  reenviar el contexto completo en cada llamada.
- **Streaming** de respuestas y su impacto en la latencia percibida.
- **Estado en Streamlit**: qué sobrevive a los reruns y qué no.
- **Manejo de secretos** con `.env` y verificación temprana de configuración.
- **Testing de apps de Streamlit** con `AppTest`, sin servidor ni navegador.

---

## Notas sobre este repo

- Es un repo de **aprendizaje**, no una librería. El código prioriza que se
  entienda por encima de la abstracción: hay repetición deliberada entre
  ejercicios para que cada uno se lea solo.
- Los ejercicios vienen de un curso, pero están reescritos, arreglados y
  documentados por mí. Los bugs que traía el material original y cómo los
  resolví están en [`docs/aprendizajes.md`](docs/aprendizajes.md).
- El material PDF del curso no se incluye por ser contenido de terceros.

---

**Facundo Costas** · [GitHub](https://github.com/FakuKostasDvlpr)
