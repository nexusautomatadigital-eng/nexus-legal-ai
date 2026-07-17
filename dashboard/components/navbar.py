import streamlit as st

from datetime import datetime


def render_navbar():

    st.markdown("# ⚖️ Nexus Command Center")

    st.caption("AI Legal Operations Platform")

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:

        st.success("🟢 Motor Online")

    with col2:

        st.info("Última actualización")

    with col3:

        st.write(datetime.now().strftime("%H:%M:%S"))

    st.divider()