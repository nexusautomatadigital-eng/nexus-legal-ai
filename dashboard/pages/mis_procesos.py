import streamlit as st

from domain.proceso_service import ProcesoService
from dashboard.components.proceso_card import render_proceso_card

st.title("⚖️ Mis Procesos")

service = ProcesoService()

procesos = service.get_procesos()

for proceso in procesos:

    render_proceso_card(proceso)