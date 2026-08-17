"""Tests de las apps de Streamlit con el framework AppTest.

`AppTest` corre la app con el runtime real de Streamlit sin levantar servidor ni
navegador, asi que verifica cosas que no se ven ejecutando el script a mano:
que `st.stop()` frene de verdad, que los widgets se rendericen, y que la app no
lance excepciones crudas.

Lo importante que cubren: si falta la API key, el usuario tiene que ver un
mensaje claro, NO un stack trace. Es el modo de falla mas probable en un deploy
publico (olvidarse de cargar el secret).

Correr con:  pytest -v
"""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

RAIZ = Path(__file__).resolve().parent.parent

APPS = [
    RAIZ / "03-chatbot-streamlit" / "app.py",
    RAIZ / "04-chatbot-avanzado" / "app.py",
]

IDS = [ruta.parent.name for ruta in APPS]


@pytest.fixture
def sin_api_key(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)


@pytest.fixture
def con_api_key(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "clave-falsa-para-tests")


@pytest.mark.parametrize("app", APPS, ids=IDS)
def test_sin_api_key_muestra_error_amigable(app, sin_api_key):
    """Sin credenciales la app avisa con st.error, no revienta."""
    at = AppTest.from_file(str(app), default_timeout=30).run()

    assert not at.exception, f"excepcion cruda en pantalla: {at.exception}"
    assert at.error, "deberia mostrar un mensaje de error explicando que falta la key"
    assert "GOOGLE_API_KEY" in at.error[0].value


@pytest.mark.parametrize("app", APPS, ids=IDS)
def test_sin_api_key_no_renderiza_el_chat(app, sin_api_key):
    """st.stop() tiene que frenar antes de dibujar la interfaz."""
    at = AppTest.from_file(str(app), default_timeout=30).run()

    assert not at.chat_input, "el chat no deberia existir sin credenciales"


@pytest.mark.parametrize("app", APPS, ids=IDS)
def test_con_api_key_renderiza_el_chat(app, con_api_key):
    """Con credenciales la app arranca limpia y muestra el input de chat.

    No se llama al modelo: solo se verifica que la app se construya sin errores.
    """
    at = AppTest.from_file(str(app), default_timeout=30).run()

    assert not at.exception, f"la app fallo al arrancar: {at.exception}"
    assert not at.error, f"error inesperado: {[e.value for e in at.error]}"
    assert at.chat_input, "deberia renderizar el input de chat"


def test_historial_arranca_vacio(con_api_key):
    """El chatbot basico parte sin mensajes de usuario en pantalla."""
    at = AppTest.from_file(str(APPS[0]), default_timeout=30).run()

    assert not at.chat_message, "no deberia haber mensajes en una sesion nueva"
