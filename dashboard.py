import streamlit as st
import pandas as pd
import psycopg2
import bcrypt
from dotenv import load_dotenv

load_dotenv()

# ======================================
# CONFIG
# ======================================

st.set_page_config(
    page_title="Nexus Legal AI",
    layout="wide"
)

# ======================================
# EVITAR AUTOCOMPLETE CHROME
# ======================================

st.markdown("""

<style>

input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {

    transition: background-color 5000s ease-in-out 0s;
    -webkit-text-fill-color: black !important;

}

</style>

""", unsafe_allow_html=True)

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

st.sidebar.markdown("### 🔐 Iniciar Sesión")

# ======================================
# NAVEGACION
# ======================================

if "pagina" not in st.session_state:
    st.session_state.pagina = "login"

col1, col2 = st.sidebar.columns(2)

with col1:

    if st.button("Login"):

        st.session_state.pagina = "login"

with col2:

    if st.button("Registro"):

        st.session_state.pagina = "registro"

nuevo_usuario = (
    st.session_state.pagina == "registro"
)

# ======================================
# REGISTRO
# ======================================

if nuevo_usuario:

    st.title("📝 Crear Cuenta")

    with st.form("registro"):

        nuevo_nombre = st.text_input(
            "Nombre Completo"
        )

        nuevo_usuario_input = st.text_input(
            "Usuario"
        )

        nuevo_password = st.text_input(
            "Password",
            type="password"
        )

        nuevo_email = st.text_input(
            "Email"
        )

        nuevo_whatsapp = st.text_input(
            "WhatsApp"
        )

        crear = st.form_submit_button(
            "Crear Cuenta"
        )

        if crear:

            cursor.execute("""

            SELECT id

            FROM clientes

            WHERE usuario = %s

            """, (

                nuevo_usuario_input,

            ))

            existe = cursor.fetchone()

            if existe:

                st.error(
                    "❌ Usuario ya existe"
                )

            else:

                # ======================================
                # HASH PASSWORD
                # ======================================

                password_hash = bcrypt.hashpw(
                    nuevo_password.encode(),
                    bcrypt.gensalt()
                ).decode()

                # ======================================
                # INSERTAR
                # ======================================

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
                    nuevo_usuario_input,
                    password_hash,
                    nuevo_email,
                    nuevo_whatsapp,
                    "BASICO"

                ))

                conn.commit()

                st.success(
                    "✅ Cuenta creada correctamente"
                )

                st.info(
                    "🔐 Ahora inicia sesión."
                )

                st.session_state.pagina = "login"

                st.rerun()

    st.stop()

# ======================================
# LOGIN
# ======================================

usuario = st.sidebar.text_input(
    "Usuario",
    key="login_usuario"
)

password = st.sidebar.text_input(
    "Password",
    type="password",
    key="login_password"
)

if not usuario or not password:

    st.stop()

# ======================================
# BUSCAR USUARIO
# ======================================

cursor.execute("""

SELECT *

FROM clientes

WHERE usuario = %s

""", (

    usuario,

))

resultado = cursor.fetchone()

# ======================================
# VALIDAR LOGIN
# ======================================

if not resultado:

    st.error(
        "❌ Usuario inválido"
    )

    st.stop()

password_guardado = resultado[2]

# ======================================
# VALIDAR PASSWORD
# ======================================

password_correcto = False

# ======================================
# PASSWORD ANTIGUA
# ======================================

if not password_guardado.startswith("$2b$"):

    if password == password_guardado:

        password_correcto = True

        nuevo_hash = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        cursor.execute("""

        UPDATE clientes

        SET password = %s

        WHERE usuario = %s

        """, (

            nuevo_hash,
            usuario

        ))

        conn.commit()

# ======================================
# PASSWORD BCRYPT
# ======================================

else:

    password_correcto = bcrypt.checkpw(

        password.encode(),

        password_guardado.encode()

    )

# ======================================
# PASSWORD INCORRECTO
# ======================================

if not password_correcto:

    st.error(
        "❌ Password incorrecto"
    )

    st.stop()

# ======================================
# DATOS CLIENTE
# ======================================

cliente_logueado = resultado[3]

email_cliente = resultado[4]

whatsapp_cliente = resultado[5]

plan_cliente = resultado[6]

# ======================================
# SIDEBAR INFO
# ======================================

st.sidebar.success(
    f"Bienvenido {cliente_logueado}"
)

st.sidebar.info(
    f"Plan: {plan_cliente}"
)

# ======================================
# LOGOUT
# ======================================

if st.sidebar.button("Cerrar Sesión"):

    st.session_state.clear()

    st.rerun()

# ======================================
# ADMIN
# ======================================

if usuario == "admin":

    st.title("⚙️ Panel Administrador")

    df_clientes = pd.read_sql(
        "SELECT * FROM clientes ORDER BY id DESC",
        conn
    )

    df_procesos = pd.read_sql(
        "SELECT * FROM procesos ORDER BY id DESC",
        conn
    )

    st.subheader("👥 Clientes")

    st.dataframe(
        df_clientes,
        use_container_width=True
    )

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
    # AGREGAR PROCESO
    # ======================================

    st.subheader("➕ Agregar Proceso")

    with st.form(
        "nuevo_proceso",
        clear_on_submit=True
    ):

        nuevo_proceso_cliente = st.text_input(
            "Número proceso judicial"
        )

        agregar = st.form_submit_button(
            "Agregar Proceso"
        )

        if agregar:

            cursor.execute("""

            SELECT id

            FROM procesos

            WHERE cliente = %s

            AND numero_proceso = %s

            """, (

                cliente_logueado,
                nuevo_proceso_cliente

            ))

            proceso_existente = cursor.fetchone()

            if proceso_existente:

                st.warning(
                    "⚠️ El proceso ya existe"
                )

            else:

                cursor.execute("""

                INSERT INTO procesos (

                    cliente,
                    email,
                    whatsapp,
                    plan,
                    numero_proceso

                )

                VALUES (%s, %s, %s, %s, %s)

                """, (

                    cliente_logueado,
                    email_cliente,
                    whatsapp_cliente,
                    plan_cliente,
                    nuevo_proceso_cliente

                ))

                conn.commit()

                st.success(
                    "✅ Proceso agregado correctamente"
                )

                st.rerun()

    # ======================================
    # CONSULTAR PROCESOS
    # ======================================

    df = pd.read_sql("""

    SELECT *

    FROM procesos

    WHERE cliente = %s

    ORDER BY id DESC

    """, conn, params=(cliente_logueado,))

    if df.empty:

        st.warning(
            "No existen procesos registrados"
        )

        st.stop()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Procesos",
            len(df)
        )

    with col2:

        ultima_fecha = df.iloc[0]["fecha_actuacion"]

        if ultima_fecha is None:

            ultima_fecha = "Sin actualizar"

        st.metric(
            "Última actuación",
            str(ultima_fecha)
        )

    with col3:

        st.metric(
            "Plan",
            plan_cliente
        )

    st.subheader("📂 Procesos")

    st.dataframe(
        df,
        use_container_width=True
    )

# ======================================
# CERRAR CONEXION
# ======================================

conn.close()