import streamlit as st


def render(data):

    st.markdown("# 👋 Buenos días")

    st.caption(
        f"Última sincronización: {data['last_sync']}"
    )

    st.success(
        "Nexus terminó de revisar automáticamente todos tus procesos."
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "🔴 Críticos",
            data["critical"]
        )

    with c2:

        st.metric(
            "🟠 Importantes",
            data["important"]
        )

    with c3:

        st.metric(
            "🟢 Estables",
            data["stable"]
        )

    st.info(
        f"⏱ Tiempo estimado de revisión: {data['estimated_time']} minutos"
    )

    st.markdown("---")

    st.subheader("🤖 Resumen Ejecutivo")

    st.write(data["summary"])