import streamlit as st

st.set_page_config(
    page_title="Nexus Legal AI",
    layout="wide"
)

# ==========================================
# CSS PREMIUM
# ==========================================

st.markdown("""

<style>

.main {
    background-color: #0f172a;
}

.hero-title {
    font-size: 60px;
    font-weight: bold;
    color: white;
}

.hero-subtitle {
    font-size: 24px;
    color: #cbd5e1;
}

.card {
    background: #111827;
    padding: 30px;
    border-radius: 20px;
    color: white;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.3);
}

.plan-card {
    background: #1e293b;
    padding: 25px;
    border-radius: 20px;
    color: white;
    text-align: center;
}

.big-button {
    background: #22c55e;
    color: white;
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
}

</style>

""", unsafe_allow_html=True)

# ==========================================
# HERO
# ==========================================

col1, col2 = st.columns([2,1])

with col1:

    st.markdown("""
    <div class="hero-title">
    ⚖️ Nexus Legal AI
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-subtitle">
    Automatización judicial inteligente con IA.
    <br><br>
    Monitorea procesos judiciales automáticamente,
    recibe alertas en tiempo real y análisis jurídico con inteligencia artificial.
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.link_button(
        "🚀 Probar Gratis",
        "https://nexus-legal-ai.streamlit.app/"
    )

with col2:

    st.image(
        "https://images.unsplash.com/photo-1589829545856-d10d557cf95f",
        use_container_width=True
    )

# ==========================================
# BENEFICIOS
# ==========================================

st.write("")
st.write("")
st.subheader("🔥 ¿Qué hace Nexus?")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("""
    <div class="card">
    <h3>⚖️ Monitoreo Judicial</h3>

    Consulta automática de procesos judiciales 24/7.
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="card">
    <h3>🤖 Inteligencia Artificial</h3>

    Resúmenes jurídicos automáticos con IA.
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="card">
    <h3>📲 Alertas Inteligentes</h3>

    WhatsApp y correo automático ante cambios judiciales.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PLANES
# ==========================================

st.write("")
st.write("")
st.subheader("💎 Planes")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("""
    <div class="plan-card">
    <h2>FREE</h2>

    1 proceso judicial

    Alertas básicas

    Email + WhatsApp

    <h1>$0</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="plan-card">
    <h2>BÁSICO</h2>

    5 procesos

    IA Jurídica

    Prioridad media

    <h1>$39.000</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="plan-card">
    <h2>PREMIUM</h2>

    Procesos ilimitados

    IA avanzada

    Alertas prioritarias

    <h1>$99.000</h1>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# CTA FINAL
# ==========================================

st.write("")
st.write("")
st.write("")

st.markdown("""
<div class="big-button">
🚀 Empieza hoy con Nexus Legal AI
</div>
""", unsafe_allow_html=True)

st.write("")

st.link_button(
    "Ingresar al Dashboard",
    "https://nexus-legal-ai.streamlit.app/"
)