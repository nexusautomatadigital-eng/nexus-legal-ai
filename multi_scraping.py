import os
import time
import pandas as pd
import psycopg2
import hashlib
from utils.logger import *
from core.helpers import ahora
from dotenv import load_dotenv
from openai import OpenAI


from twilio.rest import Client

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from services.health_monitor import (
    actualizar_estado_fuente
)

# =========================================
# MODULOS NEXUS
# =========================================

from modulos.modulo_publicaciones import (
    consultar_publicaciones
)

from modulos.modulo_samai import (
    consultar_samai
)

from services.db import (
    save_proceso_v2,
    save_actuaciones_v2,
    save_documentos_v2,
    save_publicacion_v2,
    save_vigilancia,
    get_cliente_proceso,
    get_proceso_v2
)

# =========================================
# PERSISTENCIA NEXUS V2
# =========================================

def persistir_proceso(payload):

    if not payload:
        return None
    
    print("\n👤 BUSCANDO CLIENTE DEL PROCESO")

    cliente = get_cliente_proceso(

        payload.get(
            "numero_proceso_padre",

            payload.get("numero_proceso")

        )

    )

    print("CLIENTE ENCONTRADO:")

    print(cliente)

    if cliente:

        payload["cliente_id"] = cliente[0]

        payload["plan"] = cliente[4]

        payload["email"] = cliente[2]

        payload["whatsapp"] = cliente[3]

    proceso_id = save_proceso_v2(payload)

    # ==========================================
    # CREAR VIGILANCIA SOLO PARA EL PROCESO PADRE
    # ==========================================
    
    if (

        payload.get("cliente_id")

        and

        payload.get("fuente") != "PUBLICACIONES"

    ): 

        save_vigilancia(

            payload["cliente_id"],

            proceso_id

        )
   

    print(
        f"📌 PROCESO ID GENERADO: {proceso_id}"
    )

    if not proceso_id:
        return None

    save_actuaciones_v2(

        proceso_id=proceso_id,

        numero_proceso=payload.get(
            "numero_proceso"
        ),

        actuaciones=payload.get(
            "actuaciones",
            []
        ),

        fuente=payload.get(
            "fuente"
        )

    )

    save_documentos_v2(

        proceso_id=proceso_id,

        numero_proceso=payload.get(
            "numero_proceso"
        ),

        documentos=payload.get(
            "documentos",
            []
        ),

        fuente=payload.get(
            "fuente"
        )

    )

    return proceso_id

# =========================================
# LOAD ENV
# =========================================

load_dotenv()

# =========================================
# CONFIG
# =========================================

header("INICIANDO NEXUS ENGINE")

# =========================================
# VARIABLES ENTORNO DB
# =========================================

DB_HOST = os.getenv("DB_HOST")

DB_NAME = os.getenv("DB_NAME")

DB_USER = os.getenv("DB_USER")

DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_PORT = os.getenv("DB_PORT")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# =========================================
# OPENAI CLIENT
# =========================================

print("OPENAI:", OPENAI_API_KEY)

client = OpenAI(
    api_key=OPENAI_API_KEY
)

# =========================================
# POSTGRESQL
# =========================================

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT,
    sslmode="require"
)

cursor = conn.cursor()

# =========================================
# CHROME OPTIONS
# =========================================

chrome_options = Options()

chrome_options.add_argument("--headless=new")

chrome_options.add_argument("--no-sandbox")

chrome_options.add_argument("--disable-dev-shm-usage")

chrome_options.add_argument("--disable-gpu")

chrome_options.add_argument("--window-size=1920,1080")

chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# =========================================
# NAVEGADOR
# =========================================

driver = webdriver.Chrome(

    service=Service(
        ChromeDriverManager().install()
    ),

    options=chrome_options

)

driver.set_page_load_timeout(120)

# =========================================
# LEER PROCESOS SUPABASE
# =========================================

query = """

SELECT

    p.id,
    p.numero_proceso,
    p.hash_consulta,
    p.ultima_actuacion,
    p.fecha_ultima_actuacion,
    p.fuente,
    p.especialidad,
    p.cliente_id,

    c.nombre AS cliente,
    c.email,
    c.whatsapp,
    c.plan

FROM procesos_v2 p

JOIN clientes c

    ON c.id = p.cliente_id

WHERE p.activo = TRUE

ORDER BY p.created_at DESC

LIMIT 20


"""

df_procesos = pd.read_sql(
    query,
    conn
)

print(df_procesos)

print("\n🚀 TOTAL PENDIENTES")
print(len(df_procesos))

#print("\n🚀 ESTADOS")
#print(df_procesos["estado"].value_counts())

# =========================================
# VALIDAR PROCESOS
# =========================================

if df_procesos.empty:

    print("❌ No existen procesos")

    conn.close()

    driver.quit()

    exit()

# =========================================
# LOOP PROCESOS
# =========================================

for _, row in df_procesos.iterrows():

    proceso_id = row["id"]

    cliente = row["cliente"]

    email = row["email"]

    whatsapp = ''.join(
        filter(str.isdigit, str(row["whatsapp"]))
    )

    plan = str(row["plan"]).upper()

    numero_proceso = row["numero_proceso"]

    fecha_guardada = row["fecha_ultima_actuacion"]

    hash_anterior = row["hash_consulta"]

    primer_escaneo = False

    if pd.isna(hash_anterior):
        primer_escaneo = True

    print(f"\n🔎 Consultando: {cliente}")

    print(f"⚖️ Proceso: {numero_proceso}")

    for intento in range(3):

        try:

            # =====================================
            # ACTUALIZAR ESTADO
            # =====================================

            # Temporalmente deshabilitado durante la migración a V2
            #cursor.execute("""

            #UPDATE procesos

            #SET estado = 'CONSULTANDO'

            #WHERE id = %s

            #""", (

                #proceso_id,

            #))

            #conn.commit()
            
            print("🔄 ESTADO CONSULTANDO")
            print("ID:", proceso_id)

            # =====================================
            # ABRIR RAMA JUDICIAL
            # =====================================

            try:

                driver.get(
                    "https://consultaprocesos.ramajudicial.gov.co/"
                )

            except Exception as e:

                print("❌ Timeout Rama Judicial")
                print(e)

                actualizar_estado_fuente(

                    "RAMA",

                    "ERROR",

                    f"Timeout: {str(e)[:200]}"

                )

                print("⏭️ Se omite estado REINTENTAR (V2)")

                continue

                

            driver.maximize_window()

            time.sleep(5)

            # =====================================
            # CLICK RADICACION
            # =====================================

            cards = driver.find_elements(
               By.CLASS_NAME,
               "v-card"
            )

            cards[0].click()

            time.sleep(3)

            # =====================================
            # TODOS LOS PROCESOS
            # =====================================

            todos = driver.find_element(

                By.XPATH,

                "//*[contains(text(),'Todos los Procesos')]"

            )

            todos.click()

            time.sleep(2)

            # =====================================
            # CAMPO PROCESO
            # =====================================

            campo = driver.find_element(

                By.XPATH,

                "//input[contains(@placeholder,'Ingrese los 23 dígitos')]"

            )

            campo.clear()

            campo.send_keys(str(numero_proceso))

            time.sleep(2)

            # =====================================
            # BOTON CONSULTAR
            # =====================================

            botones = driver.find_elements(
                By.TAG_NAME,
                "button"
            )

            for boton in botones:

                if "CONSULTAR" in boton.text:

                    boton.click()

                    break

            # =====================================
            # VALIDAR RESULTADO
            # =====================================

            if "no generó resultados" in driver.page_source:

                print("❌ Proceso no encontrado")

                print("⏭️ Se omite estado ERROR (V2)")
                continue

            # =====================================
            # ESPERAR TABLA
            # =====================================

            # =====================================
            # ESPERAR RESULTADOS
            # =====================================

            WebDriverWait(driver, 40).until(

                EC.presence_of_element_located(

                    (
                        By.XPATH,
                        "//table"
                    )

                )

            )

            time.sleep(5)

            # =====================================
            # BUSCAR FILAS
            # =====================================

            filas = driver.find_elements(

                By.XPATH,

                "//table//tr"

            )

            print(f"📄 Filas encontradas: {len(filas)}")

            # =====================================
            # VALIDAR FILAS
            # =====================================

            if len(filas) < 2:

                print("❌ No se encontraron resultados")

                continue



            print(f"📄 Filas encontradas: {len(filas)}")

            if len(filas) < 2:

                print("❌ Sin datos")

                continue

            # =====================================
            # EXTRAER DATOS
            # =====================================

            fila = filas[1]

            texto = fila.text

            print(texto)

            lineas = texto.split("\n")

            if len(lineas) < 6:

                print("❌ Datos incompletos")

                continue

            numero_actual = lineas[0]

            fecha_radicacion = lineas[1]

            fecha_actuacion = lineas[2]

            juzgado = lineas[3]

            juzgado_upper = juzgado.upper()

            # ==========================
            # ESPECIALIDAD
            # ==========================

            if "ADMINISTRATIVO" in juzgado_upper:

                especialidad_detectada = "ADMINISTRATIVO"

            elif "CIVIL" in juzgado_upper:

                especialidad_detectada = "CIVIL"

            elif "PENAL" in juzgado_upper:

                especialidad_detectada = "PENAL"

            elif "LABORAL" in juzgado_upper:

                especialidad_detectada = "LABORAL"

            else:

                especialidad_detectada = "CIVIL"

            # ==========================
            # MUNICIPIO / DEPARTAMENTO
            # ==========================

            municipio_detectado = ""

            departamento_detectado = ""

            if "(" in juzgado and ")" in juzgado:

                departamento_detectado = (
                    juzgado
                    .split("(")[1]
                    .replace(")", "")
                    .strip()
                )

                texto_sin_parentesis = (
                    juzgado.split("(")[0]
                )

                partes = texto_sin_parentesis.split(" DE ")

                if len(partes) > 1:

                    municipio_detectado = partes[-1].strip()

            print("ESPECIALIDAD:", especialidad_detectada)

            print("MUNICIPIO:", municipio_detectado)

            print("DEPARTAMENTO:", departamento_detectado)
                                    
            demandante = lineas[4]

            demandado = lineas[5]

            print("⏭️ Se omite actualización de fuente_rama (V2)")
            print("ID:", proceso_id)

            actualizar_estado_fuente(

                "RAMA",

                "OK",

                f"Proceso {numero_actual} consultado"

            )

            payload_rama = {

                "numero_proceso": numero_actual,

                "fuente": "RAMA",

                "jurisdiccion": "ORDINARIA",
                                
                "especialidad": especialidad_detectada,

                "despacho": juzgado,

                "estado_proceso": "ACTIVO",

                "metadata": {

                    "fecha_radicacion": fecha_radicacion,

                    "demandante": demandante,

                    "demandado": demandado,

                    "municipio": municipio_detectado,

                    "departamento": departamento_detectado,

                    "fecha_consulta": str(ahora())

                },

                "actuaciones": [

                    {

                        "fecha_actuacion": fecha_actuacion,

                        "tipo_actuacion": "ULTIMA_ACTUACION",

                        "detalle": f"Demandante: {demandante} | Demandado: {demandado}"

                    }

                ],

                "documentos": []

            }

            debug("\n===== PAYLOAD RAMA =====")
            debug(payload_rama)
            debug("========================\n")

            header("PERSISTIENDO RAMA V2")

            persistir_proceso(payload_rama)

            print("✅ RAMA PERSISTIDA")
        
            texto_hash = f"""
            {fecha_actuacion}
            {juzgado}
            {demandante}
            {demandado}
            """

            nuevo_hash = hashlib.md5(
                texto_hash.encode()
            ).hexdigest()

            # =====================================
            # IA RESUMEN OPENAI
            # =====================================

            try:

                respuesta_ai = client.chat.completions.create(

                    model="gpt-4.1-mini",

                    messages=[

                        {
                            "role": "system",

                            "content": """

                            Eres un asistente jurídico colombiano.

                            Analiza actuaciones judiciales y explica:

                            - qué ocurrió
                            - qué significa
                            - qué puede pasar después

                            Responde de forma clara y profesional.
                            """

                        },

                        {
                            "role": "user",

                            "content": f"""

                            Analiza este proceso judicial:

                            Número proceso:
                            {numero_actual}

                            Juzgado:
                            {juzgado}

                            Demandante:
                            {demandante}

                            Demandado:
                            {demandado}

                            Última actuación:
                            {fecha_actuacion}

                            """
                        }

                    ],

                    temperature=0.3

                )

                resumen_ia = respuesta_ai.choices[0].message.content

            except Exception as e:

                print("❌ Error OpenAI:", e)

                resumen_ia = f"""

                Nueva actuación detectada para el proceso
                {numero_actual}.

                Última actuación:
                {fecha_actuacion}

                """

            # =====================================
            # DETECTAR CAMBIOS REALES
            # =====================================

            cambio_detectado = False

            # PRIMER ESCANEO
            if pd.isna(hash_anterior):

                cambio_detectado = True

            # CAMBIO REAL
            elif str(hash_anterior) != str(nuevo_hash):

                cambio_detectado = True

            print("DEBUG PLAN:", plan)
            print("DEBUG PRIMER:", primer_escaneo)
            print("DEBUG CAMBIO:", cambio_detectado)   
            

            # =====================================
            # ACTUALIZAR PROCESO
            # =====================================

            estado_proceso = "SIN CAMBIOS"

            if cambio_detectado:
                estado_proceso = "NUEVA ACTUACION"


            cursor.execute("""

            UPDATE procesos

            SET

                fecha_actuacion = %s,
                juzgado = %s,
                demandante = %s,
                demandado = %s,
                resumen_ia = %s,
                hash_consulta = %s,           
                estado = %s,
                fecha_consulta = NOW(),           
                ultima_revision = NOW()

            WHERE id = %s

            """, (

                fecha_actuacion,
                juzgado,
                demandante,
                demandado,
                resumen_ia,
                nuevo_hash,
                estado_proceso,
                proceso_id

            ))

            conn.commit()

            print("✅ Proceso actualizado")

            # =====================================
            # CONSULTA PUBLICACIONES
            # =====================================

            try:

                header("CONSULTANDO PUBLICACIONES")

                resultado_publicaciones = consultar_publicaciones(

                    driver,

                    conn,

                    juzgado,
                     
                    especialidad_detectada,

                    departamento_detectado,

                    municipio_detectado

                )

                if isinstance(resultado_publicaciones, list):

                    for payload in resultado_publicaciones:

                        payload["numero_proceso_padre"] = numero_proceso

                elif isinstance(resultado_publicaciones, dict):

                    warning("Estado Publicaciones")

                    print("Fuente :", resultado_publicaciones.get("fuente"))

                    print("Estado :", resultado_publicaciones.get("estado"))

                    print("Detalle:", resultado_publicaciones.get("detalle"))

                    actualizar_estado_fuente(

                        "PUBLICACIONES",

                        resultado_publicaciones.get("estado"),

                        resultado_publicaciones.get("detalle")

                    )

                header("DEBUG PUBLICACIONES")

                if resultado_publicaciones:

                    info(type(resultado_publicaciones))

                    if isinstance(resultado_publicaciones, list):
                        print("TOTAL:", len(resultado_publicaciones))

                    else:
                        info(resultado_publicaciones)

                else:

                    warning("PUBLICACIONES VACIAS")

                if isinstance(resultado_publicaciones, list) and resultado_publicaciones:

                    total_publicaciones = len(resultado_publicaciones)

                    actualizar_estado_fuente(

                        "PUBLICACIONES",

                        "OK",

                        f"{len(resultado_publicaciones)} publicaciones"

                    )

                    header("PRIMER PAYLOAD")

                    info(resultado_publicaciones[0])

                    success(
                        f"PERSISTIENDO {len(resultado_publicaciones)} PUBLICACIONES"
                    )

                    for payload in resultado_publicaciones:

                        try:

                            header("NUEVA PUBLICACION")

                            info(f"Proceso Padre : {payload.get('numero_proceso_padre')}")

                            info(f"Publicación   : {payload.get('numero_proceso')}")

                            info(f"Artículo      : {payload.get('metadata', {}).get('article_id')}")

                            info(f"Fecha         : {payload.get('metadata', {}).get('fecha_publicacion')}")
                            
                            debug("======================================")

                            debug("\n==============================")
                            debug("PUBLICACION A PERSISTIR")
                            debug(payload)
                            debug("==============================")

                            proceso_v2 = get_proceso_v2(

                                payload.get("numero_proceso_padre")

                            )

                            info("PROCESO V2 ENCONTRADO")

                            info(proceso_v2)

                            if proceso_v2:

                                save_publicacion_v2(

                                    proceso_v2[0],

                                    payload

                                )

                                success("PUBLICACION REGISTRADA")

                            else:

                                warning("No existe proceso padre")
                                                       
                        except Exception as e:

                            exception(e)


            except Exception as e:

                error("ERROR PUBLICACIONES")

                exception(e)

                actualizar_estado_fuente(

                    "PUBLICACIONES",

                    "ERROR",

                    str(e)[:500]

                )


            # =====================================
            # CONSULTA SAMAI
            # =====================================

            try:

                header("CONSULTANDO SAMAI")

                resultado_samai = consultar_samai(

                    driver,

                    numero_proceso

                )

                print("\n===== DEBUG SAMAI =====")

                print(
                    "TIPO:",
                    type(resultado_samai)

                )

                if resultado_samai:

                    print(
                        "CLAVES:",
                        resultado_samai.keys()
                    )

                    print(
                        "ACTUACIONES:",
                        len(
                            resultado_samai.get(
                                "actuaciones",
                                []
                            )
                        )
                    )

                    actualizar_estado_fuente(

                       "SAMAI",

                       "OK",

                       f"Actuaciones: {len(resultado_samai.get('actuaciones', []))}"

                    )


                    print(
                        "DOCUMENTOS:",
                        len(
                            resultado_samai.get(
                                "documentos",
                                []
                            )
                        )
                    )

                    
                    if len(
                        resultado_samai.get(
                            "actuaciones",
                            []
                        )
                    ) > 0:

                        persistir_proceso(
                            resultado_samai
                        )

                        print(
                            "✅ SAMAI PERSISTIDO"
                        )

                    else:

                        print(
                            "⚠️ SAMAI SIN RESULTADOS"
                        )

                else:

                    print(
                        "⚠️ SAMAI VACIO"
                    )             

            except Exception as e:

                print(
                    "❌ ERROR SAMAI"
                )

                print(e)

                actualizar_estado_fuente(

                    "SAMAI",

                    "ERROR",

                    str(e)[:500]

                )                        
            
            # =====================================
            # ENVIAR ALERTAS
            # =====================================

            if cambio_detectado and (
                plan != "FREE" or primer_escaneo
            ):

                print("🚨 CAMBIO DETECTADO")

                mensaje = f"""

🚨 Nexus Legal AI

Proceso:
{numero_actual}

Nueva actuación:
{fecha_actuacion}

Juzgado:
{juzgado}

Ingrese al dashboard para revisar detalles.

"""

                # =================================
                # WHATSAPP
                # =================================

                try:

                    twilio_client.messages.create(

                        from_='whatsapp:+14155238886',

                        body=mensaje,

                        to=f'whatsapp:+{whatsapp}'

                    )

                    print("📲 WhatsApp enviado")

                except Exception as e:

                    print("❌ Error WhatsApp:", e)

                # =================================
                # EMAIL
                # =================================

                try:

                    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(

                        to=[{
                            "email": email,
                            "name": cliente
                        }],

                        sender={
                            "email": "nexusautomata.digital@gmail.com",
                            "name": "Nexus Legal AI"
                        },

                        subject="🚨 Nueva actuación judicial",

                        html_content=f"""

                        <h2>🚨 Nexus Legal AI</h2>

                        <p><b>Proceso:</b> {numero_actual}</p>

                        <p><b>Fecha actuación:</b> {fecha_actuacion}</p>

                        <p><b>Juzgado:</b> {juzgado}</p>

                        <p>Ingrese al dashboard para revisar.</p>

                        """

                    )

                    api_instance.send_transac_email(
                        send_smtp_email
                    )

                    print("📧 Email enviado")

                except Exception as e:

                    print("❌ Error Email:", e)

            if not cambio_detectado:

                print("✅ Sin cambios")

            break

        except Exception as e:

            print(f"❌ Error proceso {numero_proceso}")

            print(e)

            try:

                driver.save_screenshot(
                    f"error_{proceso_id}.png"
                )

            except Exception as screenshot_error:

                print("❌ No fue posible guardar screenshot")
                print(screenshot_error)

            try:

                conn.rollback()

            except:
                pass

            print(f"🔁 Reintentando ({intento+1}/3)...")

            time.sleep(5)

            if intento < 2:
                continue

            

            print("⏭️ Se omite estado REINTENTAR (V2)")

            

            

# =========================================
# FINALIZAR
# =========================================

driver.quit()

conn.close()

print("\n✅ NEXUS ENGINE FINALIZADO\n")