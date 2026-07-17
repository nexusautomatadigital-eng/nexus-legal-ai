import streamlit as st

from domain.proceso_service import ClienteService

from components.proceso_card import render_cliente_card


st.title("👥 Gestión de Clientes")

service = ClienteService()

clientes = service.get_clientes()

busqueda = st.text_input(
    "Buscar cliente"
)

for cliente in clientes:

    if busqueda.lower() in cliente["nombre"].lower():

        render_proceso_card(cliente)