import streamlit as st

# ============================================
# CONFIG
# ============================================

st.set_page_config(
    page_title="Nexus Legal AI",
    layout="wide"
)

# ============================================
# CSS GLOBAL
# ============================================

st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #f5f7fb;
    font-family: Arial;
}

/* HERO */
.hero {
    background: linear-gradient(135deg,#0f172a,#111827);
    padding: 60px;
    border-radius: 20px;
    color: white;
}

.hero-title {
    font-size: 52px;
    font-weight: bold;
}

.hero-sub {
    font-size: 22px;
    color: #d1d5db;
}

/* CARDS */
.card {
    background: #0f172a;
    padding: 30px;
    border-radius: 20px;
    color: white;
    min-height: 420px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.2);
}

.plan-title {
    font-size: 34px;
    font-weight: bold;
}

.price {
    font-size: 48px;
    font-weight: bold;
    color: #22d3ee;
}

.feature {
    margin-top: 15px;
    font-size: 18px;
}

.center {
    text-align:center;
}

.section-title {
    font-size: 38px;
    font-weight: bold;
    margin-top: 40px;
    margin-bottom: 20px;
}

.footer {
    text-align:center;
    color: gray;
    margin-top: 50px;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# HERO
# ============================================

st.markdown("""
<div class="hero">

<div class="hero-title">
⚖️ Nexus Legal AI
</div>

<br>

<div class="hero-sub">
Automatización judicial con Inteligencia Artificial
</div>

<br>

<div style="font-size:20px;">
Monitorea procesos judiciales automáticamente,
recibe alertas en tiempo real y análisis jurídico con IA.
</div>

</div>
""", unsafe_allow_html=True)

# ============================================
# BENEFICIOS
# ============================================

st.markdown("""
<div class="section-title">
🔥 ¿Qué hace Nexus?
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("""
    <div class="card">

    <h2>⚖️ Monitoreo Judicial</h2>

    <br>

    <p class="feature">
    Consulta automática de procesos judiciales 24/7.
    </p>

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="card">

    <h2>🧠 Inteligencia Artificial</h2>

    <br>

    <p class="feature">
    Resúmenes jurídicos automáticos con IA.
    </p>

    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="card">

    <h2>📲 Alertas Inteligentes</h2>

    <br>

    <p class="feature">
    WhatsApp y correo automático ante cambios judiciales.
    </p>

    </div>
    """, unsafe_allow_html=True)

# ============================================
# PLANES
# ============================================

st.markdown("""
<div class="section-title">
💎 Planes
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

# ============================================
# FREE
# ============================================

with c1:

    st.markdown("""
    <div class="card">

    <div class="plan-title" style="color:#4ade80;">
    🟢 FREE
    </div>

    <br>

    <div class="price">
    GRATIS
    </div>

    <br>

    <div class="feature">✅ 1 proceso judicial</div>
    <div class="feature">✅ Dashboard judicial</div>
    <div class="feature">✅ IA básica</div>
    <div class="feature">✅ Prueba gratuita</div>

    </div>
    """, unsafe_allow_html=True)

    st.button(
        "🚀 Probar Gratis",
        key="free"
    )

# ============================================
# BASICO
# ============================================

with c2:

    st.markdown("""
    <div class="card">

    <div class="plan-title" style="color:#60a5fa;">
    🔵 BASICO
    </div>

    <br>

    <div class="price">
    $29.900
    </div>

    <br>

    <div class="feature">✅ Hasta 5 procesos</div>
    <div class="feature">✅ Historial completo</div>
    <div class="feature">✅ Alertas email</div>

    </div>
    """, unsafe_allow_html=True)

    st.button(
        "💳 Suscribirme",
        key="basico"
    )

# ============================================
# PREMIUM
# ============================================

with c3:

    st.markdown("""
    <div class="card">

    <div class="plan-title" style="color:#facc15;">
    🟡 PREMIUM
    </div>

    <br>

    <div class="price">
    $59.900
    </div>

    <br>

    <div class="feature">✅ Hasta 20 procesos</div>
    <div class="feature">✅ WhatsApp automático</div>
    <div class="feature">✅ IA avanzada</div>

    </div>
    """, unsafe_allow_html=True)

    st.button(
        "💳 Suscribirme",
        key="premium"
    )

# ============================================
# GOLD
# ============================================

with c4:

    st.markdown("""
    <div class="card">

    <div class="plan-title" style="color:#c084fc;">
    🟣 GOLD
    </div>

    <br>

    <div class="price">
    $99.900
    </div>

    <br>

    <div class="feature">✅ Hasta 100 procesos</div>
    <div class="feature">✅ IA Jurídica</div>
    <div class="feature">✅ Prioridad máxima</div>

    </div>
    """, unsafe_allow_html=True)

    st.button(
        "💳 Suscribirme",
        key="gold"
    )

# ============================================
# CTA FINAL
# ============================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.success(
    "🚀 Empieza hoy con Nexus Legal AI"
)

# ============================================
# LOGIN
# ============================================

st.page_link(
    "dashboard.py",
    label="Ingresar al Dashboard"
)

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div class="footer">

Nexus Legal AI © 2026

</div>
""", unsafe_allow_html=True)