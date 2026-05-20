import streamlit as st

# ==========================================
# CONFIG
# ==========================================

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

/* HERO */

.hero-title {
    font-size: 60px;
    font-weight: bold;
    color: white;
}

.hero-subtitle {
    font-size: 24px;
    color: #cbd5e1;
    line-height: 1.6;
}

/* CARDS */

.card {
    background: #111827;
    padding: 30px;
    border-radius: 20px;
    color: white;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.3);
    min-height: 220px;
}

/* PLANES */

.plan-card {
    background: #1e293b;
    padding: 30px;
    border-radius: 20px;
    color: white;
    text-align: center;
    min-height: 480px;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.3);
}

.plan-title {
    font-size: 34px;
    font-weight: bold;
}

.price {
    font-size: 48px;
    font-weight: bold;
    color: #22d3ee;
    margin-top: 20px;
    margin-bottom: 20px;
}

.feature {
    margin-top: 15px;
    font-size: 18px;
}

/* CTA */

.big-button {
    background: #22c55e;
    color: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}

/* FOOTER */

.footer {
    text-align:center;
    color: gray;
    margin-top: 60px;
    margin-bottom: 20px;
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
    recibe alertas en tiempo real y análisis jurídico
    con inteligencia artificial.

    </div>
    """, unsafe_allow_html=True)

    st.write("")
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

    <br>

    Consulta automática de procesos judiciales 24/7.

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="card">

    <h3>🤖 Inteligencia Artificial</h3>

    <br>

    Resúmenes jurídicos automáticos con IA.

    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="card">

    <h3>📲 Alertas Inteligentes</h3>

    <br>

    WhatsApp y correo automático
    ante cambios judiciales.

    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PLANES
# ==========================================

st.write("")
st.write("")

st.subheader("💎 Planes")

col1, col2, col3, col4 = st.columns(4)

# ==========================================
# FREE
# ==========================================

with col1:

    st.markdown("""
    <div class="plan-card">

    <div class="plan-title" style="color:#4ade80;">
    🟢 FREE
    </div>

    <div class="price">
    GRATIS
    </div>

    <div class="feature">✅ 1 proceso judicial</div>

    <div class="feature">✅ Dashboard judicial</div>

    <div class="feature">✅ IA básica</div>

    <div class="feature">✅ Prueba gratuita</div>

    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "🚀 Probar Gratis",
        "https://nexus-legal-ai-fnblthpbbqn48bw2u9y9yh.streamlit.app/"
    )

# ==========================================
# BASICO
# ==========================================

with col2:

    st.markdown("""
    <div class="plan-card">

    <div class="plan-title" style="color:#60a5fa;">
    🔵 BASICO
    </div>

    <div class="price">
    $29.900
    </div>

    <div class="feature">✅ Hasta 5 procesos</div>

    <div class="feature">✅ Historial completo</div>

    <div class="feature">✅ Alertas email</div>

    </div>
    """, unsafe_allow_html=True)

    st.button(
        "💳 Suscribirme",
        key="basico"
    )

# ==========================================
# PREMIUM
# ==========================================

with col3:

    st.markdown("""
    <div class="plan-card">

    <div class="plan-title" style="color:#facc15;">
    🟡 PREMIUM
    </div>

    <div class="price">
    $59.900
    </div>

    <div class="feature">✅ Hasta 20 procesos</div>

    <div class="feature">✅ WhatsApp automático</div>

    <div class="feature">✅ IA avanzada</div>

    </div>
    """, unsafe_allow_html=True)

    st.button(
        "💳 Suscribirme",
        key="premium"
    )

# ==========================================
# GOLD
# ==========================================

with col4:

    st.markdown("""
    <div class="plan-card">

    <div class="plan-title" style="color:#c084fc;">
    🟣 GOLD
    </div>

    <div class="price">
    $99.900
    </div>

    <div class="feature">✅ Hasta 100 procesos</div>

    <div class="feature">✅ IA Jurídica</div>

    <div class="feature">✅ Prioridad máxima</div>

    </div>
    """, unsafe_allow_html=True)

    st.button(
        "💳 Suscribirme",
        key="gold"
    )

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
    "https://nexus-legal-ai-fnblthpbbqn48bw2u9y9yh.streamlit.app/"
)

# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">

Nexus Legal AI © 2026

</div>
""", unsafe_allow_html=True)