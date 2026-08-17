# 02 · Prompt templates y LCEL

Dejar de armar prompts con f-strings sueltos y empezar a componer.

## Qué muestra

- `PromptTemplate` separa la **forma** del prompt de los **datos** que lo llenan.
  El prompt vive en un solo lugar; las variables se inyectan al invocar.
- **LCEL** (LangChain Expression Language): el operador `|` encadena componentes.
  `plantilla | chat` construye el pipeline `dict → prompt renderizado → modelo`.
- La cadena se reutiliza con distintos inputs sin reescribir nada.

## Correr

```bash
python 02-prompt-templates/prompt_template.py
```

## Por qué importa el `|`

Cada eslabón de una cadena LCEL implementa la misma interfaz (`invoke`, `stream`,
`batch`). Eso significa que la cadena entera hereda esos métodos: si más adelante
agrego un parser de salida al final (`plantilla | chat | parser`), el resto del
código que la llama no cambia. Es el mismo patrón de composición que un pipe de Unix.
