# 04 · Chatbot avanzado

Misma base que el 03, con streaming, configuración en vivo y prompt template.

## Qué muestra

- **Streaming** con `cadena.stream()`: la respuesta aparece token a token en vez
  de esperar a que el modelo termine. Cambia la latencia percibida por completo.
- **Configuración en caliente**: modelo, temperatura y personalidad editables
  desde el sidebar, sin reiniciar la app.
- El historial inyectado como **texto dentro de un `PromptTemplate`**, para
  contrastar con el enfoque del ejercicio 03.

## Correr

```bash
streamlit run 04-chatbot-avanzado/app.py
```

## Dos formas de dar contexto (y cuál conviene)

| | Ejercicio 03 | Ejercicio 04 |
|---|---|---|
| Cómo | Lista de `Message` al `invoke()` | Historial serializado a texto en el prompt |
| Ventaja | El modelo distingue roles de forma nativa | Control total del formato del prompt |
| Desventaja | Menos control del prompt final | El modelo puede confundir historial con instrucciones |

En producción usaría el enfoque del **03** (lista de mensajes): es el formato
nativo de la API de chat y evita ambigüedad de roles. El 04 está acá porque es
el patrón que se ve en muchos tutoriales y quería entender por qué es peor.

## El bug que traía este ejercicio

La versión original de clase declaraba un selectbox con modelos de OpenAI y
llamaba a `ChatOpenAI(...)` — pero el único import era `ChatGoogleGenerativeAI`.
El archivo crasheaba con `NameError` apenas se abría, antes de renderizar nada.
Detalle completo en [`docs/aprendizajes.md`](../docs/aprendizajes.md).
