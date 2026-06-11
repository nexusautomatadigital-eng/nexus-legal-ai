import streamlit as st
import pandas as pd
import psycopg2
import bcrypt
import time
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
from services.db import (
    get_connection,
    get_vigilancias_cliente
)

from services.db import (

    get_connection,
    get_vigilancias_cliente,

    get_total_vigilancias,
    get_total_alertas,
    get_total_actuaciones,
    get_total_documentos

)

conn.close()

load_dotenv()

print("\n🔥 SECRETS DISPONIBLES")
print(st.secrets.keys())



# =========================================
# CONFIG
# =========================================

st.set_page_config(    
    
    page_title="Nexus Legal AI",
    layout="wide"
)

# ==========================================
# SESSION STATE
# ==========================================

if "login" not in st.session_state:

    st.session_state.login = False

if "cliente_id" not in st.session_state:

    st.session_state.cliente_id = None

if "usuario" not in st.session_state:

    st.session_state.usuario = None

      
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

if "primer_proceso" not in st.session_state:
    st.session_state.primer_proceso = False

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
    "GOLD": 999999
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

        ✅ Procesos ilimitados<br><br>
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
                st.session_state.cliente_id = resultado[0]
                
                st.success(
                    f"CLIENTE ID: {st.session_state.cliente_id}"
                )
                st.session_state.usuario = resultado[1]
                st.session_state.nombre = resultado[3]
                st.session_state.email = resultado[4]
                st.session_state.whatsapp = resultado[5]
                st.session_state.plan = resultado[6]

                st.success("✅ Bienvenido a Nexus Legal AI")
                time.sleep(1)

                st.rerun()

            else:

                st.sidebar.error(
                    "❌ Password incorrecto"
                )

    st.stop()

# =========================================
# HERO NEXUS
# =========================================

st.markdown("""

<div style="
background:linear-gradient(135deg,#0f172a,#1e293b);
padding:25px;
border-radius:20px;
margin-bottom:25px;
color:white;
">

<h1 style="margin:0;">
⚖️ Nexus Legal AI
</h1>

<h3 style="color:#93c5fd;">
Centro de Vigilancia Procesal Inteligente
</h3>

<p style="font-size:18px;">

Monitoreamos automáticamente:
<br><br>
✅ Rama Judicial
<br>
✅ SAMAI
<br>
✅ Publicaciones Procesales
<br><br>
🚨 Detectamos cambios

📄 Seguimos actuaciones

📎 Monitoreamos documentos

📲 Notificamos por Email y WhatsApp

</p>

</div>

""", unsafe_allow_html=True)

# =========================================
# DASHBOARD
# =========================================

# =========================================
# VALIDACIÓN SEGURIDAD
# =========================================

if "logueado" not in st.session_state:

    st.warning("Debe iniciar sesión")
    st.stop()

if st.session_state.logueado == False:

    st.warning("Debe iniciar sesión")
    st.stop()

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
# BIENVENIDA FREE
# =========================================

if total_procesos == 0:

    st.info("""

    ⚖️ Bienvenido a Nexus Legal AI

    Agrega tu primer proceso judicial.

    Nexus buscará automáticamente en:

    ✓ Rama Judicial

    ✓ Publicaciones Procesales

    ✓ SAMAI

    ✓ Fuentes futuras

    Luego activará la vigilancia automática.

    """)


    
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

    numero_proceso = numero_proceso.strip()

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
                        numero_proceso,
                        estado

                    )

                    VALUES (%s,%s,%s,%s,%s,%s)

                    """, (

                        cliente_logueado,
                        email_cliente,
                        whatsapp_cliente,
                        plan_cliente,
                        numero_proceso,
                        "PENDIENTE"

                    ))

                    conn.commit()

                    st.session_state.primer_proceso = True



                    placeholder = st.empty()

                    with placeholder.container():

                        st.info("""
                    🤖 Nexus está analizando tu proceso.

                    ⏳ Consultando Rama Judicial

                    ⏳ Consultando Publicaciones Procesales

                    ⏳ Consultando SAMAI

                    ⏳ Generando historial procesal

                    Tiempo estimado: 30 a 60 segundos.
                    """)

                    # ======================================
                    # DISPARAR NEXUS ENGINE INMEDIATO
                    # ======================================

                    try:

                        print("🚀 INICIANDO DISPATCH")

                        github_token = st.secrets["GITHUB_TOKEN"]
                        print("TOKEN OK")

                        github_user = st.secrets["GITHUB_USER"]
                        print("USER OK")

                        github_repo = st.secrets["GITHUB_REPO"]
                        print("REPO OK")

                    except Exception as e:

                        print("ERROR:", e)

                    try:

                        print("🚀 INICIANDO DISPATCH GITHUB")

                        github_token = st.secrets["GITHUB_TOKEN"]

                        github_user = st.secrets["GITHUB_USER"]

                        github_repo = st.secrets["GITHUB_REPO"]

                        print("USER:", github_user)

                        print("REPO:", github_repo)

                        url = f"https://api.github.com/repos/{github_user}/{github_repo}/actions/workflows/nexus_engine.yml/dispatches"

                        headers = {

                            "Authorization": f"Bearer {github_token}",

                            "Accept": "application/vnd.github+json"

                        }

                        data = {

                            "ref": "main"

                        }

                        response = requests.post(

                            url,

                            headers=headers,

                            json=data

                        )

                        if response.status_code == 204:

                            st.success(
                                "🚀 Nexus Engine iniciado correctamente"
                            )

                            st.info("""
                            🔎 Nexus está procesando el expediente.

                            La consulta puede tardar entre 30 y 90 segundos.

                            Puede seguir navegando mientras Nexus recopila información de:

                            ✓ Rama Judicial

                            ✓ Publicaciones Procesales

                            ✓ SAMAI

                            ✓ Historial Procesal
                            """)

                        else:

                            st.error(
                                f"Error GitHub: {response.status_code}"
                            )

                        print("GitHub Status:", response.status_code)

                        print("GitHub Response:", response.text)

                    except Exception as e:

                        print("ERROR GITHUB:", e)

                        st.error(
                            f"Error GitHub Actions: {e}"
                        )
                    
                    #try:

                        #github_token = st.secrets["GITHUB_TOKEN"]

                        #github_user = st.secrets["GITHUB_USER"]

                        #github_repo = st.secrets["GITHUB_REPO"]

                        #url = f"https://api.github.com/repos/{github_user}/{github_repo}/actions/workflows/nexus_engine.yml/dispatches"

                        #headers = {
                            #"Authorization": f"Bearer {github_token}",
                            #"Accept": "application/vnd.github+json"
                        #}

                        #data = {
                            #"ref": "main"
                        #}

                        #response = requests.post(
                            #url,
                            #headers=headers,
                            #json=data
                        #)

                        #print("GitHub Status:", response.status_code)

                        #print("GitHub Response:", response.text)

                        #if response.status_code in [200, 201, 204]:

                            #st.info("""

                            #🚀 Motor Nexus activado

                            #El monitoreo comenzará en unos minutos.

                            #""")

                        #else:

                            #st.warning("""

                            #⚠️ El proceso fue registrado.

                            #Nexus realizará la revisión en el siguiente ciclo automático.

                        #""")

                        #print("GitHub Status:", response.status_code)

                    #except Exception as e:

                        #st.error(f"Error GitHub Actions: {e}")

                    #st.rerun()

# =========================================
# CONSULTAR PROCESOS
# =========================================

df = pd.read_sql("""                 
                
SELECT *
FROM procesos
WHERE cliente = %s
ORDER BY id DESC

""", conn, params=(cliente_logueado,))

print("ESTADO DF")
print(
    df[["id","estado"]]
)

conn.close()

# =========================================
# DASHBOARD VACIO
# =========================================

if df.empty:

    st.warning(
        "No existen procesos registrados"
    )

else:

    # =====================================
    # AUTO REFRESH NEXUS
    # =====================================

    procesos_pendientes = len(

        df[
            df["estado"].isin([ 
                "PENDIENTE",
                "CONSULTANDO"
            ])        
        ]
    )

    if procesos_pendientes > 0:

        st.warning(
            f"🟡 Nexus procesando {procesos_pendientes} expediente(s)"
        )

        st.info("""
        ⏳ Nexus está consultando:

        ✓ Rama Judicial
        ✓ Publicaciones Procesales
        ✓ SAMAI

        La información se actualizará automáticamente.
        """)

        

        st_autorefresh(
            interval=15000,
            key="nexus_refresh"
        )

    else:

        st.success(
            "🟢 Todos los expedientes están actualizados"
        )

    # =====================================
    # KPI NEXUS
    # =====================================

    total_vigilancias = get_total_vigilancias()

    total_alertas = get_total_alertas()

    total_actuaciones = get_total_actuaciones()

    total_documentos = get_total_documentos()

    # =========================================
    # KPI CLIENTE
    # =========================================

    procesos_cliente = len(df)

    cambios_detectados = len(
        df[
            df["estado"].isin(
                [
                    "NUEVA ACTUACION",
                    "ACTUALIZADO"
                ]
            )
        ]
    )

    ultima_revision = "Sin revisión"

    if not df.empty:

        ultima_revision = df.iloc[0]["fecha_consulta"]
        ultima_revision = ultima_revision.strftime(
            "%d-%m-%Y %H:%M"
        )

    estado_general = "🟢 Activo"

    # =========================================
    # KPI PREMIUM
    # =========================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(f"""

        <div style="
        background:#111827;
        padding:25px;
        border-radius:18px;
        text-align:center;
        color:white;
        ">

        <h3>⚖️</h3>

        <h2>{procesos_cliente}</h2>

        <p>Procesos Vigilados</p>

        </div>

        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""

        <div style="
        background:#111827;
        padding:25px;
        border-radius:18px;
        text-align:center;
        color:white;
        ">

        <h3>🚨</h3>

        <h2>{cambios_detectados}</h2>

        <p>Cambios Detectados</p>

        </div>

        """, unsafe_allow_html=True)

    from datetime import datetime

    fecha_formateada = "Sin revisión"
                    
    if ultima_revision:
        try:
            fecha_formateada = pd.to_datetime( 
                ultima_revision
            ).strftime("%d/%m/%Y %H:%M")
        except:
            pass

    with col3:

        st.markdown(f"""

        <div style="
        background:#111827;
        padding:25px;
        border-radius:18px;
        text-align:center;
        color:white;
        ">

        <h3>📄</h3>
                           
        <h2>{fecha_formateada}</h2>

        <p>Última Revisión Nexus</p>

        </div>

        """, unsafe_allow_html=True)

    with col4:

        st.markdown(f"""

        <div style="
        background:#111827;
        padding:25px;
        border-radius:18px;
        text-align:center;
        color:white;
        ">

        <h3>📎</h3>

        <h2>{estado_general}</h2>

        <p>Estado Nexus</p>

        </div>

        """, unsafe_allow_html=True)


    
    # =====================================
    # METRICAS
    # =====================================

    #col1, col2, col3 = st.columns(3)

    #with col1:

        #st.metric(
            #"Total Procesos",
            #len(df)
        #)

    #with col2:

        #ultima_fecha = df.iloc[0]["fecha_actuacion"]

        #if ultima_fecha is None:
            #ultima_fecha = "Sin actualizar"

        #st.metric(
            #"Última actuación",
            #Cstr(ultima_fecha)
        #)

    #with col3:

        #st.metric(
            #"Plan",
            #plan_cliente
        #)

    # =====================================
    # DASHBOARD PROCESOS PRO
    # =====================================

    st.subheader(
        "⚖️ Centro de Vigilancia Procesal"
    )

    st.caption(
        "Monitoreo inteligente de procesos judiciales, actuaciones, documentos y alertas."
    )

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

        rama = "🟢" if row.get("fuente_rama") else "⚪"

        publicaciones = "🟢" if row.get("fuente_publicaciones") else "⚪"

        samai = "🟢" if row.get("fuente_samai") else "⚪"

        pdfs = row.get("pdfs_encontrados", 0)       

        components.html(f"""

        <div style="
            background:#111827;
            padding:25px;
            border-radius:18px;
            margin-bottom:20px;
            border:1px solid #1f2937;
            box-shadow:0 0 15px rgba(0,0,0,0.25);
            color:white;
            font-family:Arial;
        ">
        <div style="
        background:#0f172a;
        padding:10px;
        border-radius:12px;
        margin-bottom:15px;
        ">

        🟢 Monitoreo Activo

        </div>

        <h3>
        ⚖️ Expediente Judicial Monitoreado
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

        <p style="color:#9ca3af; font-size:13px;">
        🤖 Última revisión automática Nexus:
        {row["fecha_consulta"]}
        </p>

        <p>
        📅 <b>Último movimiento detectado:</b>
        {fecha_actuacion}
        </p>

        <p>
        🏛️ <b>Juzgado:</b><br>
        {juzgado}
        </p>

        <p>
        👤 <b>Demandante</b><br>
        {demandante.replace("Demandante:", "").strip()}
        </p>

        <p>
        ⚖️ <b>Demandado</b><br>
        {demandado.replace("Demandado:", "").strip()}
        </p>

        <hr>

        <p><b>🔎 Fuentes Monitoreadas</b></p>

        <p>{rama} Rama Judicial</p>

        <p>{publicaciones} Publicaciones Procesales</p>

        <p>{samai} SAMAI</p>

        <p>📄 PDFs encontrados: {pdfs}</p>

        <p>
        ⚪ IA Jurídica
        </p>

        <div style="
        background:#1f2937;
        padding:15px;
        border-radius:12px;
        margin-top:15px;
        ">

        <b>🧠 Análisis Nexus AI</b>

        <br><br>

        {resumen_ia}

        </div>

        </div>

        """, height=700, scrolling=True)

# =========================================
# VIGILANCIAS V2
# =========================================

# DESACTIVADO TEMPORALMENTE

#st.markdown("---")

#st.subheader(
    #"📌 Mis Vigilancias (V2)"
#)

#vigilancias = get_vigilancias_cliente(

    #st.session_state.cliente_id

#)

#if not vigilancias:

    #st.info(
        #"No existen vigilancias activas."
    #)

#else:

    #for v in vigilancias:

        #vigilancia_id = v[0]

        #estado = v[1]

        #numero_proceso = v[2]

        #fuente = v[3]

        #especialidad = v[4]

        #despacho = v[5]

        #ultima_actuacion = v[6]

        #fecha_ultima_actuacion = v[7]

        #ultima_revision = v[8]

        # =====================================
        # VALIDACIONES
        # =====================================

        #if not ultima_actuacion:

            #ultima_actuacion = "Sin información"

        #if not fecha_ultima_actuacion:

            #fecha_ultima_actuacion = "Sin información"

        #if not ultima_revision:

            #ultima_revision = "Sin revisión"

    
        #with st.container(border=True):

            #st.write(
                #f"📄 Proceso: {numero_proceso}"
            #)

            #st.write(
                #f"📡 Fuente: {fuente}"
            #)

            #st.write(
                #f"⚖️ Especialidad: {especialidad}"
            #)

            #st.write(
                #f"🏛️ Despacho: {despacho}"
            #)

            #st.write(
                #f"📅 Última actuación: {fecha_ultima_actuacion}"
            #)

            #st.write(
                #f"📄 Actuación: {ultima_actuacion}"
            #)

            #st.write(
                #f"🤖 Última revisión Nexus: {ultima_revision}"
            #)

            #st.write(
                #f"✅ Estado: {estado}"
            #)

            #st.caption(
                #vigilancia_id
            #)        

# =========================================
# FOOTER
# =========================================

#st.markdown("---")

#st.caption(
    #"Nexus Legal AI © 2026 - Automatización Judicial Inteligente"
#)

# =========================================
# CLOSE DB
# =========================================

# conn.close()