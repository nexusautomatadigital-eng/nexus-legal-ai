from dataclasses import dataclass

import streamlit as st


@dataclass
class UserContext:
    cliente_id: int
    usuario: str
    nombre: str
    email: str
    whatsapp: str
    plan: str


class SessionService:

    @staticmethod
    def create_session(cliente):

        st.session_state.logueado = True
        st.session_state.cliente_id = cliente.id
        st.session_state.usuario = cliente.usuario
        st.session_state.nombre = cliente.nombre
        st.session_state.email = cliente.email
        st.session_state.whatsapp = cliente.whatsapp
        st.session_state.plan = cliente.plan

    @staticmethod
    def is_authenticated():

        return st.session_state.get("logueado", False)

    @staticmethod
    def get_context():

        if not SessionService.is_authenticated():
            return None

        return UserContext(
            cliente_id=st.session_state.cliente_id,
            usuario=st.session_state.usuario,
            nombre=st.session_state.nombre,
            email=st.session_state.email,
            whatsapp=st.session_state.whatsapp,
            plan=st.session_state.plan,
        )

    @staticmethod
    def logout():

        claves = [
            "logueado",
            "cliente_id",
            "usuario",
            "nombre",
            "email",
            "whatsapp",
            "plan",
        ]

        for clave in claves:
            st.session_state.pop(clave, None)