import streamlit as st
from datetime import datetime


def render(user_name: str):

    hora = datetime.now().hour

    if hora < 12:
        saludo = "Buenos días"
    elif hora < 18:
        saludo = "Buenas tardes"
    else:
        saludo = "Buenas noches"

    ahora = datetime.now().strftime("%H:%M")

    st.markdown(
        f"""
# 👋 {saludo}, {user_name}

Nexus revisó automáticamente tus procesos.

🕒 Última actualización: **{ahora}**
"""
    )

    st.divider()