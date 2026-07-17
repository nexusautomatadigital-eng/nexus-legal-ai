import streamlit as st


def render_actions(actions):

    st.subheader("🚨 Acciones recomendadas")

    if not actions:

        st.success("No existen acciones pendientes.")

        return

    for action in actions:

        with st.container(border=True):

            c1, c2 = st.columns([5,1])

            with c1:

                st.markdown(
                    f"""
### {action["icon"]} {action["titulo"]}

{action["descripcion"]}

**Cliente**

{action["cliente"]}

**Proceso**

{action["proceso"]}
"""
                )

            with c2:

                st.button(

                    "Abrir",

                    key=action["id"]

                )