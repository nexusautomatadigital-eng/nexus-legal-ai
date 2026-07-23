import streamlit as st


def render_sidebar(
    nombre_cliente,
    plan_cliente,
    total_procesos,
    limite_plan,
    wompi_basico,
    wompi_premium,
    wompi_gold,
):
    """
    Renderiza la barra lateral de Nexus Legal AI.
    """

    if "pagina" not in st.session_state:
        st.session_state.pagina = "inicio"

    st.sidebar.markdown("""
# ⚖ Nexus Legal AI

**Centro de Operaciones Jurídicas**
""")

    st.sidebar.divider()

    st.sidebar.markdown(
        f"### 👋 {nombre_cliente}"
    )

    st.sidebar.caption(
        f"Plan: {plan_cliente}"
    )

    st.sidebar.metric(
        "Procesos monitoreados",
        f"{total_procesos}/{limite_plan}"
    )

    st.sidebar.divider()

    # =========================================
    # NAVEGACIÓN
    # =========================================

    st.sidebar.markdown("### 🧭 Navegación")

    if st.sidebar.button(
        "🏠 Inicio",
        use_container_width=True
    ):    
        st.session_state.pagina = "inicio"
    

    if st.sidebar.button(
        "📂 Mis Procesos",
        use_container_width=True
    ):     
        st.session_state.pagina = "procesos"
    

    if st.sidebar.button(
        "🔔 Alertas",
        use_container_width=True
    ):    
        st.session_state.pagina = "alertas"
    

    if st.sidebar.button(
        "📄 Documentos",
        use_container_width=True
    ):    
        st.session_state.pagina = "documentos"
    

    if st.sidebar.button(
        "🤖 IA Jurídica",
        use_container_width=True
    ):

        st.session_state.pagina = "ia"
    

    st.sidebar.divider()
    

    # =========================================
    # UPGRADE
    # =========================================

    st.sidebar.subheader("🚀 Mejorar Plan")

    if plan_cliente == "FREE":

        st.sidebar.link_button(
            "🔵 BASICO",
            wompi_basico
        )

        st.sidebar.link_button(
            "🟡 PREMIUM",
            wompi_premium
        )

        st.sidebar.link_button(
            "🟣 GOLD",
            wompi_gold
        )

    elif plan_cliente == "BASICO":

        st.sidebar.link_button(
            "🟡 PREMIUM",
            wompi_premium
        )

        st.sidebar.link_button(
            "🟣 GOLD",
            wompi_gold
        )

    elif plan_cliente == "PREMIUM":

        st.sidebar.link_button(
            "🟣 GOLD",
            wompi_gold
        )

    st.sidebar.divider()

    
