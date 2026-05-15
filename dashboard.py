import streamlit as st
import pandas as pd
import psycopg2
import bcrypt
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# =========================================
# CONFIG
# =========================================

st.set_page_config(
    page_title="Nexus Legal AI",
    layout="wide"
)

# =========================================
# CSS
# =========================================

st.markdown("""

<style>

.block-container{
    padding-top:2rem;
}

.plan-card{
    border:1px solid #2d2d2d;
    padding:25px;
    border-radius:15px;
    background:#111827;
    color:white;
    min-height:420px;
}

.plan-title{
    font-size:28px;
    font-weight:bold;
}

.plan-price{
    font-size:38px;
    color:#00d4ff;
    font-weight:bold;
}

.plan-free{
    color:#00ff88;
}

.plan-premium{
    color:#ffd700;
}

.plan-gold{
    color:#d946ef;
}

</style>

""", unsafe_allow_html=True)

# =========================================
# SESSION
# =========================================

if "logueado" not in st.session_state:
    st.session_state.logueado = False

if "pagina" not in st.session_state:
    st.session_state.pagina = "landing"

if "plan_seleccionado" not in st.session_state:
    st.session_state.plan_seleccionado = "FREE"

# =========================================
# AUTO LOGOUT
# =========================================

TIMEOUT_MINUTOS = 30

if "ultima_actividad" not in st.session_state:
    st.session_state.ultima_actividad = datetime.now()

else:

    diferencia = datetime.now() - st.session_state.ultima_actividad

    if diferencia > timedelta(minutes=TIMEOUT_MINUTOS):

        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.warning("⚠️ Sesión expirada por inactividad")
        st.rerun()

st.session_state.ultima_actividad = datetime.now()

# =========================================
# DATABASE
# =========================================

conn = psycopg2.connect(
    host=st.secrets["SUPABASE_HOST"],
    database=st.secrets["SUPABASE_DB"],
    user=st.secrets["SUPABASE_USER"],
    password=st.secrets["SUPABASE_PASSWORD"],
    port=st.secrets["SUPABASE_PORT"],
    sslmode="require"
)

cursor = conn.cursor()

# =========================================
# WOMPI LINKS
# =========================================

WOMPI_BASICO = "https://checkout.wompi.co/l/MB3i06"
WOMPI_PREMIUM = "https://checkout.wompi.co/l/gfCbqa"
WOMPI_GOLD = "https://checkout.wompi.co/l/F8UqPA"

# =========================================
# LIMITES PLANES
# =========================================

LIMITES = {
    "FREE": 1,
    "BASICO": 5,
    "PREMIUM": 20,
    "GOLD": 100
}

# =========================================
# SIDEBAR
# =========================================

st.sidebar.title("⚖️ Nexus Legal AI")

# =========================================
# LANDING
# =========================================

if not st.session_state.logueado:

    st.title("⚖️ Nexus Legal AI")

    st.subheader(
        "Automatización judicial con Inteligencia Artificial"
    )

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    # =====================================
    # FREE
    # =====================================

    with col1:

        st.markdown("""
        <div class="plan-card">

        <div class="plan-title plan-free">
        🟢 FREE
        </div>

        <br>

        <div class="plan-price">
        GRATIS
        </div>

        <br>

        ✅ 1 proceso judicial<br><br>
        ✅ Dashboard judicial<br><br>
        ✅ IA básica<br><br>
        ✅ Prueba gratuita<br><br>

        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Probar Gratis"):

            st.session_state.plan_seleccionado = "FREE"
            st.session_state.pagina = "registro"

            st.rerun()

    # =====================================
    # BASICO
    # =====================================

    with col2:

        st.markdown("""
        <div class="plan-card">

        <div class="plan-title">
        🔵 BASICO
        </div>

        <br>

        <div class="plan-price">
        $29.900
        </div>

        <br>

        ✅ Hasta 5 procesos<br><br>
        ✅ Historial completo<br><br>
        ✅ Alertas email<br><br>

        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            "💳 Suscribirme",
            WOMPI_BASICO
        )

    # =====================================
    # PREMIUM
    # =====================================

    with col3:

        st.markdown("""
        <div class="plan-card">

        <div class="plan-title plan-premium">
        🟡 PREMIUM
        </div>

        <br>

        <div class="plan-price">
        $59.900
        </div>

        <br>

        ✅ Hasta 20 procesos<br><br>
        ✅ WhatsApp automático<br><br>
        ✅ IA avanzada<br><br>

        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            "💳 Suscribirme",
            WOMPI_PREMIUM
        )

    # =====================================
    # GOLD
    # =====================================

    with col4:

        st.markdown("""
        <div class="plan-card">

        <div class="plan-title plan-gold">
        🟣 GOLD
        </div>

        <br>

        <div class="plan-price">
        $99.900
        </div>

        <br>

        ✅ Hasta 100 procesos<br><br>
        ✅ IA Jurídica<br><br>
        ✅ Prioridad máxima<br><br>

        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            "💳 Suscribirme",
            WOMPI_GOLD
        )

    st.markdown("---")

    # =====================================
    # LOGIN
    # =====================================

    st.sidebar.subheader("🔐 Iniciar Sesión")

    usuario_login = st.sidebar.text_input(
        "Usuario"
    )

    password_login = st.sidebar.text_input(
        "Password",
        type="password"
    )

    ingresar = st.sidebar.button(
        "Ingresar"
    )

    # =====================================
    # REGISTRO FREE
    # =====================================

    if st.session_state.pagina == "registro":

        st.markdown("---")

        st.header("📝 Crear Cuenta")

        with st.form("registro"):

            nombre = st.text_input(
                "Nombre Completo"
            )

            usuario = st.text_input(
                "Usuario"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            email = st.text_input(
                "Email"
            )

            whatsapp = st.text_input(
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

                """, (usuario,))

                existe = cursor.fetchone()

                if existe:

                    st.error(
                        "❌ Usuario ya existe"
                    )

                else:

                    password_hash = bcrypt.hashpw(
                        password.encode(),
                        bcrypt.gensalt()
                    ).decode()

                    cursor.execute("""

                    INSERT INTO clientes (

                        nombre,
                        usuario,
                        password,
                        email,
                        whatsapp,
                        plan

                    )

                    VALUES (%s,%s,%s,%s,%s,%s)

                    """, (

                        nombre,
                        usuario,
                        password_hash,
                        email,
                        whatsapp,
                        st.session_state.plan_seleccionado

                    ))

                    conn.commit()

                    st.success(
                        "✅ Cuenta creada correctamente"
                    )

                    time.sleep(2)

                    st.session_state.pagina = "landing"

                    st.rerun()

    # =====================================
    # LOGIN
    # =====================================

    if ingresar:

        cursor.execute("""

        SELECT *
        FROM clientes
        WHERE usuario = %s

        """, (usuario_login,))

        resultado = cursor.fetchone()

        if not resultado:

            st.sidebar.error(
                "❌ Usuario inválido"
            )

        else:

            password_guardado = resultado[2]

            password_correcto = bcrypt.checkpw(

                password_login.encode(),
                password_guardado.encode()

            )

            if password_correcto:

                st.session_state.logueado = True

                st.session_state.usuario = resultado[1]
                st.session_state.nombre = resultado[3]
                st.session_state.email = resultado[4]
                st.session_state.whatsapp = resultado[5]
                st.session_state.plan = resultado[6]

                st.rerun()

            else:

                st.sidebar.error(
                    "❌ Password incorrecto"
                )

    st.stop()

# =========================================
# DASHBOARD
# =========================================

cliente_logueado = st.session_state.nombre
plan_cliente = st.session_state.plan
email_cliente = st.session_state.email
whatsapp_cliente = st.session_state.whatsapp

# =========================================
# SIDEBAR LOGUEADO
# =========================================

st.sidebar.success(
    f"Bienvenido {cliente_logueado}"
)

st.sidebar.info(
    f"Plan: {plan_cliente}"
)

# =========================================
# CONTADOR PLAN
# =========================================

cursor.execute("""

SELECT COUNT(*)
FROM procesos
WHERE cliente = %s

""", (cliente_logueado,))

total_procesos = cursor.fetchone()[0]

limite_plan = LIMITES.get(
    plan_cliente,
    1
)

st.sidebar.metric(
    "Procesos usados",
    f"{total_procesos}/{limite_plan}"
)

# =========================================
# UPGRADE
# =========================================

st.sidebar.markdown("---")

st.sidebar.subheader("🚀 Mejorar Plan")

if plan_cliente == "FREE":

    st.sidebar.link_button(
        "🔵 BASICO",
        WOMPI_BASICO
    )

    st.sidebar.link_button(
        "🟡 PREMIUM",
        WOMPI_PREMIUM
    )

    st.sidebar.link_button(
        "🟣 GOLD",
        WOMPI_GOLD
    )

elif plan_cliente == "BASICO":

    st.sidebar.link_button(
        "🟡 PREMIUM",
        WOMPI_PREMIUM
    )

    st.sidebar.link_button(
        "🟣 GOLD",
        WOMPI_GOLD
    )

elif plan_cliente == "PREMIUM":

    st.sidebar.link_button(
        "🟣 GOLD",
        WOMPI_GOLD
    )

# =========================================
# LOGOUT
# =========================================

st.sidebar.markdown("---")

if st.sidebar.button("Cerrar Sesión"):

    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.rerun()

# =========================================
# TITULO
# =========================================

st.title("⚖️ Nexus Legal AI")

st.subheader(
    f"Procesos judiciales de {cliente_logueado}"
)

# =========================================
# AGREGAR PROCESO
# =========================================

st.subheader("➕ Agregar Proceso")

with st.form(
    "nuevo_proceso",
    clear_on_submit=True
):

    numero_proceso = st.text_input(
        "Número proceso judicial"
    )

    agregar = st.form_submit_button(
        "Agregar Proceso"
    )

    if agregar:

        if not numero_proceso.strip():

            st.warning(
                "⚠️ Ingrese un proceso"
            )

        else:

            if total_procesos >= limite_plan:

                st.error(
                    f"❌ Tu plan {plan_cliente} permite máximo {limite_plan} procesos"
                )

            else:

                cursor.execute("""

                SELECT id
                FROM procesos
                WHERE cliente = %s
                AND numero_proceso = %s

                """, (

                    cliente_logueado,
                    numero_proceso

                ))

                existe = cursor.fetchone()

                if existe:

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

                    VALUES (%s,%s,%s,%s,%s)

                    """, (

                        cliente_logueado,
                        email_cliente,
                        whatsapp_cliente,
                        plan_cliente,
                        numero_proceso

                    ))

                    conn.commit()

                    st.success(
                        "✅ Proceso agregado correctamente"
                    )

                    st.rerun()

# =========================================
# CONSULTAR PROCESOS
# =========================================

df = pd.read_sql("""

SELECT *
FROM procesos
WHERE cliente = %s
ORDER BY id DESC

""", conn, params=(cliente_logueado,))

# =========================================
# DASHBOARD VACIO
# =========================================

if df.empty:

    st.warning(
        "No existen procesos registrados"
    )

else:

    # =====================================
    # METRICAS
    # =====================================

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

    # =====================================
    # DASHBOARD PROCESOS PRO
    # =====================================

    st.subheader("📂 Mis Procesos Judiciales")

    for _, row in df.iterrows():

        estado = row["estado"]

        color_estado = "#22c55e"

        if estado == "PENDIENTE":
            color_estado = "#facc15"

        elif estado == "ERROR":
            color_estado = "#ef4444"

        elif estado == "ACTUALIZADO":
            color_estado = "#22c55e"

        fecha_actuacion = row["fecha_actuacion"]

        if fecha_actuacion is None:
            fecha_actuacion = "Sin actualizar"

        juzgado = row["juzgado"]

        if juzgado is None:
            juzgado = "No disponible"

        demandante = row["demandante"]

        if demandante is None:
            demandante = "No disponible"

        demandado = row["demandado"]

        if demandado is None:
            demandado = "No disponible"

        resumen_ia = row["resumen_ia"]

        if resumen_ia is None:
            resumen_ia = """
            Nexus AI aún no ha generado resumen jurídico.
            """

    st.markdown(f"""

    <div style="
        background:#111827;
        padding:25px;
        border-radius:18px;
        margin-bottom:20px;
        border:1px solid #1f2937;
        box-shadow:0 0 15px rgba(0,0,0,0.25);
    ">

    <h3 style="color:white;">
    ⚖️ Proceso Judicial
    </h3>

    <p style="
        color:#60a5fa;
        font-size:18px;
        font-weight:bold;
    ">
    {row["numero_proceso"]}
    </p>

    <div style="
        display:inline-block;
        background:{color_estado};
        color:white;
        padding:6px 12px;
        border-radius:12px;
        font-size:14px;
        font-weight:bold;
        margin-bottom:15px;
    ">
    {estado}
    </div>

    <hr>

    <p style="color:white;">
    📅 <b>Última actuación:</b><br>
    {fecha_actuacion}
    </p>

    <p style="color:white;">
    🏛️ <b>Juzgado:</b><br>
    {juzgado}
    </p>

    <p style="color:white;">
    👤 <b>Demandante:</b><br>
    {demandante}
    </p>

    <p style="color:white;">
    ⚖️ <b>Demandado:</b><br>
    {demandado}
    </p>

    <p style="
        color:#d1d5db;
        background:#1f2937;
        padding:15px;
        border-radius:12px;
    ">
    🤖 <b>Resumen IA:</b><br><br>
    {resumen_ia}
    </p>

    </div>

    """, unsafe_allow_html=True)

# =========================================
# FOOTER
# =========================================

st.markdown("---")

st.caption(
    "Nexus Legal AI © 2026 - Automatización Judicial Inteligente"
)

# =========================================
# CLOSE DB
# =========================================

conn.close()