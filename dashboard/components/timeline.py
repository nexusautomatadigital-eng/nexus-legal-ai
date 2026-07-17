import streamlit as st


def render_timeline(events):

    st.subheader("🕒 Actividad Reciente")

    if not events:

        st.info("No existen eventos recientes.")

        return

    for event in events:

        st.markdown(
            f"""
<div style="
background:white;
padding:18px;
margin-bottom:12px;
border-radius:12px;
border-left:5px solid #2563EB;
box-shadow:0 2px 6px rgba(0,0,0,.05);
">

<b>{event["icon"]} {event["titulo"]}</b>

<br>

{event["cliente"]}

<br>

<small>{event["fecha"]}</small>

</div>
""",
            unsafe_allow_html=True
        )