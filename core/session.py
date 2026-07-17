import streamlit as st

from core.context import UserContext


class SessionService:

    KEY = "user_context"

    @classmethod
    def get_context(cls):

        if cls.KEY not in st.session_state:

            st.session_state[cls.KEY] = UserContext()

        return st.session_state[cls.KEY]