import streamlit as st
import pandas as pd
import psycopg2

# ======================================
# CONFIG
# ======================================

st.set_page_config(
    page_title="Admin Nexus Legal AI",
    layout="wide"
)

# ======================================
# CONEXION POSTGRESQL
# ======================================

conn = psycopg2.connect(

    host="aws-1-us-west-1.pooler.supabase.com",
    database="postgres",
    user="postgres.xnreltwbbledefdygwmc",
    password="n%&GvQFDyL-!2+8",
    port="5432"

)

cursor = conn.cursor()

# ======================================
# LOGIN ADMIN
# ======================================

st.sidebar.title("🔐 Admin Login")

admin_user = st.sidebar.text_input(
    "Usuario Admin"
)

admin_pass = st.sidebar.text_input(
    "Password Admin",
    type="password"
)

# ======================================
# VALIDAR ADMIN
# ======================================

if admin_user != "admin" or admin_pass != "admin123":

    st.warning("Ingrese credenciales admin")

    st.stop()

st.sidebar.success("Admin conectado")

# ======================================
# TITULO
# ======================================

st.title("⚖️ Panel Administrador")

# ======================================
# METRICAS
# ======================================

df_total = pd.read_sql(
    "SELECT * FROM procesos",
    conn
)

df_clientes = pd.read_sql(
    "SELECT * FROM clientes",
    conn
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Total Clientes",
        len(df_clientes)
    )

with col2:

    st.metric(
        "Total Procesos",
        len(df_total)
    )

# ======================================
# CREAR CLIENTE
# ======================================

st.subheader("➕ Crear Cliente")

nombre = st.text_input("Nombre Cliente")

usuario = st.text_input("Usuario")

password = st.text_input(
    "Password",
    type="password"
)

plan = st.selectbox(
    "Plan",
    ["BASICO", "PREMIUM"]
)

if st.button("Crear Cliente"):

    cursor.execute("""

    INSERT INTO clientes (

        nombre,
        usuario,
        password,
        plan

    )

    VALUES (%s, %s, %s, %s)

    """, (

        nombre,
        usuario,
        password,
        plan

    ))

    conn.commit()

    st.success("✅ Cliente creado")

# ======================================
# VER CLIENTES
# ======================================

st.subheader("👥 Clientes")

df_clientes = pd.read_sql(
    "SELECT * FROM clientes",
    conn
)

st.dataframe(
    df_clientes,
    use_container_width=True
)

# ======================================
# VER PROCESOS
# ======================================

st.subheader("📂 Procesos")

df_procesos = pd.read_sql(
    "SELECT * FROM procesos",
    conn
)

st.dataframe(
    df_procesos,
    use_container_width=True
)

# ======================================
# CERRAR CONEXION
# ======================================

conn.close()