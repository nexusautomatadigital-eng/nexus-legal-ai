import streamlit as st


def render_proceso_card(cliente):

    with st.container(border=True):

        col1, col2 = st.columns([5, 1])

        with col1:

            st.markdown(f"## 👤 {cliente['nombre']}")

            st.caption(f"Plan: {cliente['plan']}")

            c1, c2 = st.columns(2)

            with c1:
                st.metric(
                    "Procesos",
                    cliente["procesos"]
                )

            with c2:
                st.metric(
                    "Publicaciones",
                    cliente["publicaciones"]
                )

        with col2:

            st.button(
                "Ver",
                key=f"cliente_{cliente['id']}"
            )

        st.divider()