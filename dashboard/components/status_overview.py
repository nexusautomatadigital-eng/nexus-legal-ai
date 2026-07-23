import streamlit as st


def render(
    criticos: int,
    importantes: int,
    estables: int,
):

    c1, c2, c3 = st.columns(3)

    with c1:
        st.error(f"🔴 {criticos}\n\nAsuntos críticos")

    with c2:
        st.warning(f"🟠 {importantes}\n\nAsuntos importantes")

    with c3:
        st.success(f"🟢 {estables}\n\nProcesos estables")

    st.divider()