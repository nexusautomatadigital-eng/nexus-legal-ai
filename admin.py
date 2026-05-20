import streamlit as st
import psycopg2
import pandas as pd
import os

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Nexus Admin",
    layout="wide"
)

# ==========================================
# DB
# ==========================================

conn = psycopg2.connect(

    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")

)

# ==========================================
# LOGIN
# ==========================================

st.title("⚖️ Nexus Admin")

usuario = st.text_input("Usuario")
password = st.text_input("Password", type="password")

if st.button("Ingresar"):

    query = f"""

    SELECT *

    FROM admins

    WHERE usuario = '{usuario}'
    AND password = '{password}'

    """

    df_admin = pd.read_sql(query, conn)

    if len(df_admin) > 0:

        st.success("Bienvenido Admin")

        # =====================================
        # CLIENTES
        # =====================================

        df_clientes = pd.read_sql("""

        SELECT *

        FROM clientes

        ORDER BY id DESC

        """, conn)

        st.subheader("Clientes Nexus")

        st.dataframe(df_clientes)

    else:

        st.error("Credenciales incorrectas")