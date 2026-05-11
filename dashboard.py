import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# ======================================
# CONFIG PAGINA
# ======================================

st.set_page_config(
    page_title="Nexus Legal AI",
    layout="wide"
)

# ======================================
# CONEXION POSTGRESQL
# ======================================

conn = psycopg2.connect(

    host=st.secrets["SUPABASE_HOST"],
    database=st.secrets["SUPABASE_DB"],
    user=st.secrets["SUPABASE_USER"],
    password=st.secrets["SUPABASE_PASSWORD"],
    port=st.secrets["SUPABASE_PORT"],
    sslmode="require"

)

cursor = conn.cursor()

# ======================================
# LOGIN
# ======================================

st.sidebar.title("🔐 Login")

usuario = st.sidebar.text_input("Usuario")

password = st.sidebar.text_input(
    "Password",
    type="password"
)

# ======================================
# VALIDAR LOGIN
# ======================================

query_login = f"""

SELECT *

FROM clientes

WHERE usuario = '{usuario}'

AND password = '{password}'

"""

df_login = pd.read_sql(
    query_login,
    conn
)

if df_login.empty:

    st.warning("Ingrese credenciales")

    st.stop()

cliente_logueado = df_login.iloc[0]["nombre"]

plan_cliente = df_login.iloc[0]["plan"]

st.sidebar.success(
    f"Bienvenido {cliente_logueado}"
)

# ======================================
# ADMIN
# ======================================

if usuario == "admin":

    st.title("⚙️ Panel Administrador")

    # ======================================
    # METRICAS
    # ======================================

    df_total_clientes = pd.read_sql(
        "SELECT * FROM clientes",
        conn
    )

    df_total_procesos = pd.read_sql(
        "SELECT * FROM procesos",
        conn
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Clientes",
            len(df_total_clientes)
        )

    with col2:

        st.metric(
            "Procesos",
            len(df_total_procesos)
        )

    # ======================================
    # CLIENTES
    # ======================================

    st.subheader("👥 Clientes")

    st.dataframe(
        df_total_clientes,
        use_container_width=True
    )

    # ======================================
    # CREAR CLIENTE
    # ======================================

    st.subheader("➕ Crear Cliente")

    with st.form("crear_cliente"):

        nuevo_nombre = st.text_input("Nombre")

        nuevo_usuario = st.text_input("Usuario")

        nuevo_password = st.text_input(
            "Password",
            type="password"
        )

        nuevo_plan = st.selectbox(
            "Plan",
            ["BASICO", "PREMIUM", "GOLD"]
        )

        nuevo_email = st.text_input("Email")

        crear = st.form_submit_button(
            "Crear Cliente"
        )

        if crear:

            cursor.execute("""

            INSERT INTO clientes (

                nombre,
                usuario,
                password,
                plan,
                email

            )

            VALUES (%s, %s, %s, %s, %s)

            """, (

                nuevo_nombre,
                nuevo_usuario,
                nuevo_password,
                nuevo_plan,
                nuevo_email

            ))

            conn.commit()

            st.success("✅ Cliente creado")

            st.rerun()

    # ======================================
    # EDITAR CLIENTE
    # ======================================

    st.subheader("✏️ Editar Cliente")

    cliente_editar = st.selectbox(
        "Seleccionar cliente",
        df_total_clientes["usuario"]
    )

    datos_cliente = df_total_clientes[
        df_total_clientes["usuario"] == cliente_editar
    ].iloc[0]

    with st.form("editar_cliente"):

        edit_nombre = st.text_input(
            "Nombre",
            value=datos_cliente["nombre"]
        )

        edit_password = st.text_input(
            "Password",
            value=datos_cliente["password"]
        )

        edit_plan = st.selectbox(
            "Plan",
            ["BASICO", "PREMIUM", "GOLD"],
            index=[
                "BASICO",
                "PREMIUM",
                "GOLD"
            ].index(datos_cliente["plan"])
        )

        edit_email = st.text_input(
            "Email",
            value=datos_cliente["email"]
        )

        guardar = st.form_submit_button(
            "Guardar Cambios"
        )

        if guardar:

            cursor.execute("""

            UPDATE clientes

            SET

                nombre = %s,
                password = %s,
                plan = %s,
                email = %s

            WHERE usuario = %s

            """, (

                edit_nombre,
                edit_password,
                edit_plan,
                edit_email,
                cliente_editar

            ))

            conn.commit()

            st.success(
                "✅ Cliente actualizado"
            )

            st.rerun()

    # ======================================
    # ASIGNAR PROCESO
    # ======================================

    st.subheader("⚖️ Asignar Proceso")

    cliente_proceso = st.selectbox(
        "Cliente",
        df_total_clientes["nombre"],
        key="cliente_proceso"
    )

    with st.form("asignar_proceso"):

        nuevo_proceso = st.text_input(
            "Número Proceso"
        )

        asignar = st.form_submit_button(
            "Asignar"
        )

        if asignar:

            cursor.execute("""

            INSERT INTO procesos (

                cliente,
                numero_proceso

            )

            VALUES (%s, %s)

            """, (

                cliente_proceso,
                nuevo_proceso

            ))

            conn.commit()

            st.success(
                "✅ Proceso asignado"
            )

            st.rerun()

    # ======================================
    # VER PROCESOS
    # ======================================

    # ======================================
    # ACTUALIZAR PROCESOS
    # ======================================

    st.subheader("🔄 Actualizar Procesos")

    if st.button("Ejecutar Scraping Judicial"):

        import os

        resultado = os.system(
            "python multi_scraping.py"
        )

        if resultado == 0:

            st.success(
                "✅ Procesos actualizados"
            )

        else:

            st.error(
                "❌ Error ejecutando scraping"
            )

    st.subheader("📂 Procesos")

    st.dataframe(
        df_total_procesos,
        use_container_width=True
    )

# ======================================
# CLIENTE NORMAL
# ======================================

else:

    # ======================================
    # CONSULTAR PROCESOS
    # ======================================

    query = f"""

    SELECT *

    FROM procesos

    WHERE cliente = '{cliente_logueado}'

    ORDER BY id DESC

    """

    df = pd.read_sql(
        query,
        conn
    )

    st.title("⚖️ Nexus Legal AI")

    st.subheader(
        f"Procesos judiciales de {cliente_logueado}"
    )

    if df.empty:

        st.warning(
            "No existen procesos registrados"
        )

        st.stop()

    # ======================================
    # METRICAS
    # ======================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Procesos",
            len(df)
        )

    with col2:

        st.metric(
            "Última actuación",
            str(df.iloc[0]["fecha_actuacion"])
        )

    with col3:

        st.metric(
            "Plan",
            plan_cliente
        )

    # ======================================
    # TABLA
    # ======================================

    st.subheader("📂 Procesos")

    st.dataframe(
        df,
        use_container_width=True
    )

    # ======================================
    # FILTRO JUZGADO
    # ======================================

    st.subheader("🔎 Filtrar Juzgado")

    juzgados = df["juzgado"].dropna().unique()

    if len(juzgados) > 0:

        juzgado_select = st.selectbox(
            "Seleccione juzgado",
            juzgados
        )

        df_juzgado = df[
            df["juzgado"] == juzgado_select
        ]

        st.dataframe(
            df_juzgado,
            use_container_width=True
        )

# ======================================
# CERRAR CONEXION
# ======================================

conn.close()