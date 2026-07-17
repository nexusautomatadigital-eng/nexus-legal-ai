import streamlit as st


def render_proceso_card(proceso):

    st.container(border=True)

    st.markdown(
        f"""
### ⚖️ {proceso.numero}

**Health:** {proceso.health.score}

**Estado:** {proceso.health.estado}

---

👤 {proceso.cliente}

📰 Publicaciones: {proceso.actividad.publicaciones}

⚖️ Actuaciones: {proceso.actividad.actuaciones}

📄 Documentos: {proceso.actividad.documentos}

---

Prioridad: {proceso.health.prioridad}

Riesgo: {proceso.health.riesgo}

---

💡 {proceso.health.recomendacion}
"""
    )

    st.button(
        "📂 Abrir Expediente",
        key=proceso.id
    )