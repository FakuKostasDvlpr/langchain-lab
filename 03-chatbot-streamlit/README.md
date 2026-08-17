# 03 · Chatbot con memoria

Primer proyecto con interfaz. Un chat que recuerda lo que se habló.

## Qué muestra

- Que **un LLM no tiene memoria**. Cada llamada a la API es independiente. La
  "memoria" es que le reenviamos la lista completa de mensajes anteriores.
- `st.session_state` como único estado que sobrevive a los reruns de Streamlit.
- Los tres tipos de mensaje de LangChain: `SystemMessage` (personalidad, no se
  muestra), `HumanMessage`, `AIMessage`.
- Manejo de errores que no corrompe el historial.

## Correr

```bash
streamlit run 03-chatbot-streamlit/app.py
```

## Las dos cosas que me trabaron

**Streamlit reejecuta el script entero en cada interacción.** Al principio guardaba
el historial en una lista normal y se borraba en cada mensaje. Por eso hay que
redibujar toda la conversación en cada rerun leyendo de `session_state`: la
pantalla se reconstruye desde cero cada vez.

**El orden de las operaciones importa cuando algo falla.** Si agrego la pregunta al
historial y la llamada al modelo tira error, queda una pregunta sin respuesta
guardada — y en el siguiente turno se le manda al modelo un historial inconsistente.
Por eso el `except` hace `pop()` del mensaje del usuario.
