import streamlit as st


def render_kpi(title, value, icon="📊", color="#2563EB"):

    st.markdown(

        f"""
<div class="kpi-card" style="border-left-color:{color};">

<div class="kpi-title">
{icon} {title}
</div>

<div class="kpi-value">
{value}
</div>

</div>
""",

        unsafe_allow_html=True,

    )