import streamlit as st

from domain.proceso_service import ProcesoService
from dashboard.components.proceso_card import render_proceso_card


def render_mis_procesos(cliente_id):

    st.title("📂 Mis Procesos")

    service = ProcesoService()

    procesos = service.get_procesos(cliente_id)

    for proceso in procesos:

        render_proceso_card(proceso)