import streamlit as st


def render_priority_card(prioridad):

    st.markdown(
f"""
<div style="
background:#FFF8E7;
border-left:8px solid #F59E0B;
border-radius:16px;
padding:24px;
margin-bottom:25px;
box-shadow:0 4px 12px rgba(0,0,0,.08);
">

<h3 style="margin-top:0;">
🚨 PRIORIDAD DEL DÍA
</h3>

<p><b>Cliente:</b> {prioridad.cliente}</p>

<p><b>Proceso:</b> {prioridad.numero_proceso}</p>

<p><b>Evento:</b> {prioridad.evento}</p>

<p><b>Fecha:</b> {prioridad.fecha}</p>

<p><b>Fuente:</b> {prioridad.fuente}</p>

<hr>

<b>Acción recomendada</b>

<br><br>

{prioridad.accion}

</div>
""",
        unsafe_allow_html=True,
    )