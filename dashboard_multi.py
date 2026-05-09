import streamlit as st
import pandas as pd
import sqlite3

# ======================================
# CONFIG
# ======================================

st.set_page_config(
    page_title="Nexus Legal AI",
    layout="wide"
)

# ======================================
# USUARIOS DEMO
# ======================================

usuarios = {

    "juan": {
        "password": "1234",
        "cliente": "Juan"
    },

    "ana": {
        "password": "5678",
        "cliente": "Ana"
    }

}

# ======================================
# LOGIN
# ======================================

st.title("🔐 Nexus Legal AI")

usuario = st.text_input("Usuario")

password = st.text_input(
    "Contraseña",
    type="password"
)

# ======================================
# BOTON LOGIN
# ======================================

if st.button("Ingresar"):

    if usuario in usuarios:

        if password == usuarios[usuario]["password"]:

            st.success("✅ Acceso correcto")

            cliente_logueado = usuarios[usuario]["cliente"]

            # ======================================
            # SQLITE
            # ======================================

            conn = sqlite3.connect("procesos.db")

            query = f"""

            SELECT *

            FROM procesos

            WHERE cliente = '{cliente_logueado}'

            """

            df = pd.read_sql_query(query, conn)

            conn.close()

            # ======================================
            # TITULO
            # ======================================

            st.title(
                f"⚖️ Procesos de {cliente_logueado}"
            )

            # ======================================
            # METRICAS
            # ======================================

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Procesos",
                    len(df)
                )

            with col2:

                st.metric(
                    "Última actuación",
                    df["fecha_actuacion"].max()
                )

            # ======================================
            # TABLA
            # ======================================

            st.subheader("📂 Procesos")

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.error("❌ Contraseña incorrecta")

    else:

        st.error("❌ Usuario no existe")