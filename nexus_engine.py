import os
import pandas as pd
from services.db import (
    get_connection,
    save_proceso_v2,
    save_actuaciones_v2,
    save_documentos_v2
)

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from modulos.modulo_rama import consultar_rama
from modulos.modulo_samai import consultar_samai
from modulos.modulo_publicaciones import (
    consultar_publicaciones,
    extraer_detalle_publicacion
)

# ==========================================
# PERSISTENCIA CENTRAL NEXUS V2
# ==========================================

def persistir_payload(payload):

    if not payload:

        return None

    proceso_id = save_proceso_v2(
        payload
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

# ==========================================
# LOAD ENV
# ==========================================

load_dotenv()

print("🚀 NEXUS ENGINE V2")

# ==========================================
# DB CONFIG
# ==========================================

DB_HOST = os.getenv("DB_HOST")

DB_NAME = os.getenv("DB_NAME")

DB_USER = os.getenv("DB_USER")

DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_PORT = os.getenv("DB_PORT")

# ==========================================
# CONEXION DB
# ==========================================

conn = get_connection()


# ==========================================
# CHROME
# ==========================================

chrome_options = Options()

chrome_options.add_argument("--headless")

chrome_options.add_argument("--no-sandbox")

chrome_options.add_argument("--disable-dev-shm-usage")

chrome_options.add_argument("--disable-gpu")

chrome_options.add_argument("--window-size=1920,1080")

chrome_options.add_argument(
    "user-agent=Mozilla/5.0"
)

driver = webdriver.Chrome(

    service=Service(
        ChromeDriverManager().install()
    ),

    options=chrome_options

)

# ==========================================
# LEER PROCESOS
# ==========================================

query = """

SELECT *

FROM procesos

ORDER BY id DESC

"""

df = pd.read_sql(query, conn)

print(df)

# ==========================================
# LOOP PROCESOS
# ==========================================

for _, row in df.iterrows():

    try:

        numero_proceso = row["numero_proceso"]

        cliente = row["cliente"]

        fuente = row["fuente"]

        print(f"\n🔎 Cliente: {cliente}")

        print(f"⚖️ Proceso: {numero_proceso}")

        # ======================================
        # RAMA JUDICIAL
        # ======================================

        if fuente is None or fuente == "RAMA":

            resultado = consultar_rama(
                driver,
                numero_proceso
            )

            if resultado:

                print("🔥 PAYLOAD RAMA")
                print(resultado)

                persistir_payload(
                    resultado
                )

                print("\n===== PARAMETROS PUBLICACIONES =====")

                print("JUZGADO:", juzgado)

                print("ESPECIALIDAD:", especialidad_detectada)

                print("DEPARTAMENTO:", departamento_detectado)

                print("MUNICIPIO:", municipio_detectado)

                resultado_publicaciones = consultar_publicaciones(
                               

                    driver,
                    conn,

                    juzgado="JUZGADO 004 CIVIL DEL CIRCUITO",

                    especialidad="CIVIL",

                    departamento="BOYACA",

                    municipio="TUNJA"

                )

                if resultado_publicaciones:

                    print(
                        f"📄 PUBLICACIONES ENCONTRADAS: "
                        f"{len(resultado_publicaciones)}"
                    )

                    for payload in resultado_publicaciones:
                        

                        persistir_payload(
                            payload
                        )

        # ======================================
        # SAMAI
        # ======================================

        if fuente == "SAMAI":

            print("🚀 CONSULTANDO SAMAI")

            resultado_samai = consultar_samai(

                driver,
                numero_proceso

            )

            if resultado_samai:

                print(resultado_samai)

                cursor = conn.cursor()

                cursor.execute("""

                UPDATE procesos

                SET

                    fecha_consulta = NOW(),
                    ultima_revision = NOW(),
                    fuente = %s,
                    hash_consulta = %s,
                    estado = 'ACTUALIZADO'

                WHERE numero_proceso = %s

                """, (

                    resultado_samai["fuente"],
                    resultado_samai["hash"],
                    numero_proceso

                ))

                conn.commit()

                print("✅ SAMAI ACTUALIZADO")        

        # ======================================
        # PUBLICACIONES PROCESALES
        # ======================================

        if fuente == "PUBLICACIONES":

            resultado_publicaciones = consultar_publicaciones(

                driver,

                juzgado="JUZGADO 004 CIVIL DEL CIRCUITO",

                especialidad="CIVIL",

                departamento="BOYACA",

                municipio="TUNJA"

            )

            if resultado_publicaciones:

                print(
                    f"📄 PUBLICACIONES ENCONTRADAS: "
                    f"{len(resultado_publicaciones)}"
                )

                print("🚨 INICIANDO PERSISTENCIA")

                for payload in resultado_publicaciones:

                    persistir_payload(
                        payload
                    )

                print("🚨 PERSISTENCIA FINALIZADA")            

    except Exception as e:

        print(f"❌ ERROR PROCESO: {e}")

        continue

driver.quit()

conn.close()

print("\n✅ NEXUS ENGINE FINALIZADO")