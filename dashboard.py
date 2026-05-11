import streamlit as st
import pandas as pd
import psycopg2
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
# SIDEBAR
# ======================================

st.sidebar.title("⚖️ Nexus Legal AI")

menu = st.sidebar.selectbox(

    "Seleccione",

    ["Login", "Crear Cuenta"]

)

# ======================================
# CREAR CUENTA
# ======================================

if menu == "Crear Cuenta":

    st.title("📝 Crear Cuenta")

    with st.form("registro"):

        nuevo_nombre = st.text_input("Nombre Completo")

        nuevo_usuario = st.text_input("Usuario")

        nuevo_password = st.text_input(
            "Password",
            type="password"
        )

        nuevo_email = st.text_input("Email")

        nuevo_whatsapp = st.text_input(
            "WhatsApp"
        )

        crear = st.form_submit_button(
            "Crear Cuenta"
        )

        if crear:

            # VALIDAR USUARIO EXISTENTE

            cursor.execute("""

            SELECT *

            FROM clientes

            WHERE usuario = %s

            """, (nuevo_usuario,))

            existe = cursor.fetchone()

            if existe:

                st.error(
                    "❌ Usuario ya existe"
                )

            else:

                cursor.execute("""

                INSERT INTO clientes (

                    nombre,
                    usuario,
                    password,
                    email,
                    whatsapp,
                    plan

                )

                VALUES (%s, %s, %s, %s, %s, %s)

                """, (

                    nuevo_nombre,
                    nuevo_usuario,
                    nuevo_password,
                    nuevo_email,
                    nuevo_whatsapp,
                    "BASICO"

                ))

                conn.commit()

                st.success(
                    "✅ Cuenta creada correctamente"
                )

                st.info(
                    "Ahora puede iniciar sesión"
                )

    st.stop()

# ======================================
# LOGIN
# ======================================

usuario = st.sidebar.text_input(
    "Usuario"
)

password = st.sidebar.text_input(
    "Password",
    type="password"
)

if not usuario or not password:

    st.warning("Ingrese credenciales")

    st.stop()

# ======================================
# LOGIN SQL
# ======================================

cursor.execute("""

SELECT *

FROM clientes

WHERE usuario = %s

AND password = %s

""", (

    usuario,
    password

))

resultado = cursor.fetchone()

if not resultado:

    st.error("❌ Usuario inválido")

    st.stop()

# ======================================
# DATOS CLIENTE
# ======================================

cliente_logueado = resultado[1]
usuario_logueado = resultado[2]
plan_cliente = resultado[4]

st.sidebar.success(
    f"Bienvenido {cliente_logueado}"
)

st.sidebar.info(
    f"Plan: {plan_cliente}"
)

# ======================================
# ADMIN
# ======================================

if usuario == "admin":

    st.title("⚙️ Panel Administrador")

    # ======================================
    # CONSULTAS
    # ======================================

    df_clientes = pd.read_sql(

        "SELECT * FROM clientes ORDER BY id DESC",

        conn

    )

    df_procesos = pd.read_sql(

        "SELECT * FROM procesos ORDER BY id DESC",

        conn

    )

    # ======================================
    # METRICAS
    # ======================================

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Clientes",
            len(df_clientes)
        )

    with col2:

        st.metric(
            "Procesos",
            len(df_procesos)
        )

    # ======================================
    # CLIENTES
    # ======================================

    st.subheader("👥 Clientes")

    st.dataframe(
        df_clientes,
        use_container_width=True
    )

    # ======================================
    # EDITAR CLIENTE
    # ======================================

    st.subheader("✏️ Editar Cliente")

    cliente_editar = st.selectbox(

        "Seleccione Cliente",

        df_clientes["usuario"]

    )

    datos_cliente = df_clientes[

        df_clientes["usuario"] == cliente_editar

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

        df_clientes["nombre"],

        key="cliente_proceso"

    )

    with st.form("asignar_proceso"):

        nuevo_proceso = st.text_input(
            "Número de proceso"
        )

        asignar = st.form_submit_button(
            "Asignar Proceso"
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
    # PROCESOS
    # ======================================

    st.subheader("📂 Procesos")

    st.dataframe(

        df_procesos,

        use_container_width=True

    )

# ======================================
# CLIENTE NORMAL
# ======================================

else:

    st.title("⚖️ Nexus Legal AI")

    st.subheader(
        f"Procesos judiciales de {cliente_logueado}"
    )

    # ======================================
    # AUTO AGREGAR PROCESO
    # ======================================

    st.subheader("➕ Agregar Proceso")

    with st.form("nuevo_proceso_cliente"):

        nuevo_proceso_cliente = st.text_input(
            "Número proceso judicial"
        )

        agregar = st.form_submit_button(
            "Agregar Proceso"
        )

        if agregar:

            cursor.execute("""

            INSERT INTO procesos (

                cliente,
                numero_proceso

            )

            VALUES (%s, %s)

            """, (

                cliente_logueado,
                nuevo_proceso_cliente

            ))

            conn.commit()

            st.success(
                "✅ Proceso agregado"
            )

            st.rerun()

    # ======================================
    # CONSULTAR PROCESOS
    # ======================================

    query = """

    SELECT *

    FROM procesos

    WHERE cliente = %s

    ORDER BY id DESC

    """

    df = pd.read_sql(

        query,

        conn,

        params=(cliente_logueado,)

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

    st.subheader("🔎 Filtrar por Juzgado")

    juzgados = df["juzgado"].dropna().unique()

    if len(juzgados) > 0:

        juzgado_select = st.selectbox(

            "Seleccione Juzgado",

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