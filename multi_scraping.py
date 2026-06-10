import os
import time
import pandas as pd
import psycopg2
import hashlib
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

# =========================================
# LOAD ENV
# =========================================

load_dotenv()

# =========================================
# CONFIG
# =========================================

print("\n🚀 INICIANDO NEXUS ENGINE\n")

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

driver.set_page_load_timeout(60)

# =========================================
# LEER PROCESOS SUPABASE
# =========================================

query = """

SELECT *

FROM procesos

WHERE estado = 'PENDIENTE'

ORDER BY id DESC

LIMIT 20

"""


#query = """

#SELECT *

#FROM procesos

#ORDER BY id DESC

#"""

df_procesos = pd.read_sql(
    query,
    conn
)

print(df_procesos)

print("\n🚀 TOTAL PENDIENTES")
print(len(df_procesos))

print("\n🚀 ESTADOS")
print(df_procesos["estado"].value_counts())

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

    fecha_guardada = row["fecha_actuacion"]

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

            cursor.execute("""

            UPDATE procesos

            SET estado = 'CONSULTANDO'

            WHERE id = %s

            """, (

                proceso_id,

            ))

            conn.commit()

            # =====================================
            # ABRIR RAMA JUDICIAL
            # =====================================

            driver.get(
                "https://consultaprocesos.ramajudicial.gov.co/"
            )

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

            print("✅ Consulta ejecutada")

            time.sleep(10)

            # =====================================
            # VALIDAR RESULTADO
            # =====================================

            if "no generó resultados" in driver.page_source:

                print("❌ Proceso no encontrado")

                cursor.execute("""

                UPDATE procesos

                SET estado = 'ERROR'

                WHERE id = %s

                """, (

                    proceso_id,

                ))

                conn.commit()

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

            demandante = lineas[4]

            demandado = lineas[5]

            cursor.execute("""

            UPDATE procesos

            SET fuente_rama = TRUE

            WHERE id = %s

            """, (

                proceso_id,

            ))

            print("ROWCOUNT:", cursor.rowcount)

            conn.commit()

            print("✅ FUENTE RAMA ACTUALIZADA")
            print("ID:", proceso_id)
        
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

            driver.save_screenshot(
                f"error_{proceso_id}.png"
            )

            conn.rollback()

            print(f"❌ Error proceso {numero_proceso}")

            print(e)

            print(f"🔁 Reintentando ({intento+1}/3)...")

            time.sleep(5)

            if intento < 2:
                continue

            cursor.execute("""

            UPDATE procesos

            SET estado = 'ERROR'

            WHERE id = %s

            """, (

                proceso_id,

            ))

            conn.commit()

# =========================================
# FINALIZAR
# =========================================

driver.quit()

conn.close()

print("\n✅ NEXUS ENGINE FINALIZADO\n")