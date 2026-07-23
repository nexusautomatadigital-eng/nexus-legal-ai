import streamlit as st


def render_priority_card(prioridad):

    if prioridad is None:

        st.info("✅ No existen prioridades para hoy.")
        return

    st.markdown(
        f"""
<div style="
background: linear-gradient(135deg,#FFF8E1,#FFFDF8);
border-left:10px solid #F59E0B;
border-radius:18px;
padding:30px;
margin-top:10px;
margin-bottom:20px;
box-shadow:0 8px 24px rgba(0,0,0,.08);
">

<div style="font-size:26px;font-weight:700;margin-bottom:25px;">
⚠ PRIORIDAD DEL DÍA
</div>

<div style="font-size:14px;color:#777;">
EXPEDIENTE
</div>

<div style="
font-size:28px;
font-weight:700;
margin-bottom:25px;
color:#111827;
">
{prioridad.numero_proceso}
</div>

<div style="
font-size:22px;
font-weight:600;
margin-bottom:10px;
color:#DC2626;
">
{prioridad.evento}
</div>

<div style="
font-size:18px;
margin-bottom:30px;
color:#374151;
">
{prioridad.accion}
</div>

<div style="
background:#FFFFFF;
border-radius:12px;
padding:15px;
border:1px solid #E5E7EB;
margin-bottom:20px;
">

<b>Estado</b><br>

Impacto:
<b>{prioridad.impacto}</b>

</div>

</div>
""",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.button(
            "📂 Abrir expediente",
            use_container_width=True,
            type="primary"
        )