# Aprendizajes y problemas resueltos

Bitácora de las cosas que se rompieron y qué aprendí arreglándolas. Está acá
porque los errores enseñan más que el código que anda a la primera.

---

## 1. `NameError: ChatOpenAI is not defined`

**Dónde:** el chatbot con sidebar (hoy `04-chatbot-avanzado/app.py`).

**Síntoma:** la app crasheaba al abrirse, sin renderizar nada.

**Causa:** el ejercicio venía de un material escrito para OpenAI y lo estaba
adaptando a Gemini. Cambié el import de arriba (`ChatGoogleGenerativeAI`) pero
quedaron sin migrar la instanciación (`ChatOpenAI(...)`) y la lista de modelos
del selectbox (`gpt-3.5-turbo`, `gpt-4`, `gpt-4o-mini`).

**Arreglo:** unificar todo en el proveedor de Google — instanciación y lista de
modelos válidos de Gemini.

**Lo que me llevo:** al migrar de proveedor hay que buscar *todas* las
referencias, no solo el import. LangChain abstrae la interfaz (`invoke`,
`stream` funcionan igual en cualquier proveedor), pero los nombres de clase y
los IDs de modelo son específicos de cada uno. La abstracción hace que el
código *parezca* portable y esconde justamente estos tres puntos de acople.

---

## 2. El historial se borraba en cada mensaje

**Dónde:** los dos chatbots.

**Causa:** Streamlit **reejecuta el script completo** en cada interacción del
usuario. Cualquier variable de Python normal se reinicializa. No es un bug del
framework: es su modelo de ejecución.

**Arreglo:** `st.session_state` para el historial, y redibujar la conversación
entera en cada rerun leyendo desde ahí.

**Lo que me llevo:** en Streamlit hay que pensar en "¿qué sobrevive al rerun?"
antes de escribir la lógica, no después.

---

## 3. El modelo no recordaba nada, aunque yo guardaba el historial

**Causa:** confundí guardar el historial *en la app* con dárselo *al modelo*.
Un LLM no tiene estado: cada request a la API es independiente. Guardar los
mensajes en `session_state` sirve para dibujarlos en pantalla; para que el
modelo los "recuerde" hay que **reenviárselos completos** en cada llamada.

**Lo que me llevo:** toda "memoria" de un chatbot es reenvío de contexto. De ahí
sale el problema real: la ventana de contexto es finita y cada token reenviado
se paga. Las estrategias de memoria (ventana deslizante, resumen del historial,
recuperación selectiva) existen para administrar eso.

---

## 4. El historial se renderizaba como `repr` de Python

**Dónde:** `04-chatbot-avanzado/app.py`.

**Síntoma:** el modelo respondía cosas raras o mencionaba "HumanMessage".

**Causa:** pasar la lista de objetos `Message` directo a una variable de
`PromptTemplate`. El template hace interpolación de strings, así que insertaba
literalmente `[HumanMessage(content='hola'), AIMessage(content='...')]`.

**Arreglo:** una función `formatear_historial()` que serializa a
`Usuario: ... / Asistente: ...`.

**Lo que me llevo:** `PromptTemplate` espera **texto**. Si necesito pasar
estructura, la serialización es responsabilidad mía y define qué entiende el
modelo. Cuando el contexto es una conversación, conviene el otro camino: pasar
la lista de mensajes directo al modelo (ejercicio 03), que es el formato nativo
de la API de chat.

---

## 5. La API key y el orden de las líneas

`ChatGoogleGenerativeAI` no recibe la key como parámetro: la lee de la variable
de entorno `GOOGLE_API_KEY`. Si `load_dotenv()` se ejecuta *después* de
instanciar el modelo, falla con un error de autenticación que no da ninguna
pista de que el problema es el orden.

**Lo que me llevo:** configuración implícita por entorno = errores que no
apuntan a su causa. Por eso las apps de este repo chequean explícitamente que
la variable exista y muestran un mensaje claro antes de intentar nada.
