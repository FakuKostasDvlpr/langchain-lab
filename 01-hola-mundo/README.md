# 01 · Hola mundo

Primera llamada a un modelo de lenguaje usando LangChain.

## Qué muestra

- Cómo instanciar un chat model (`ChatGoogleGenerativeAI`) apuntando a Gemini.
- Que `invoke()` devuelve un objeto `AIMessage`, no un string: el texto está en `.content`.
- Qué hace `temperature` (0.0 determinista → 1.0 creativa).

## Correr

```bash
python 01-hola-mundo/hola_mundo.py
```

Requiere un `.env` en la raíz con `GOOGLE_API_KEY` (ver `.env.example`).

## Detalle que me costó entender

`ChatGoogleGenerativeAI` nunca recibe la API key como parámetro. La lee sola de la
variable de entorno `GOOGLE_API_KEY`. Por eso `load_dotenv()` tiene que ejecutarse
**antes** de instanciar el modelo — si lo ponés después, falla con un error de
autenticación que no dice nada sobre el orden de las líneas.
