import pandas as pd
import psycopg2
import time

from twilio.rest import Client

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ======================================
# LEER CLIENTES
# ======================================

df_clientes = pd.read_csv("clientes_procesos.csv")

print(df_clientes)

# ======================================
# CONEXION POSTGRESQL
# ======================================

conn = psycopg2.connect(

    host="aws-1-us-west-1.pooler.supabase.com",

    database="postgres",

    user="postgres.xnreltwbbledefdygwmc",

    password="n%&GvQFDyL-!2+8",

    port="5432",

    sslmode="require"

)

cursor = conn.cursor()

# ======================================
# CREAR TABLA
# ======================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS procesos (

    id SERIAL PRIMARY KEY,

    cliente TEXT,
    email TEXT,
    whatsapp TEXT,
    plan TEXT,

    numero_proceso TEXT,
    fecha_actuacion TEXT,
    juzgado TEXT,
    demandante TEXT,
    demandado TEXT,

    fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

conn.commit()

# ======================================
# CONFIG BREVO EMAIL
# ======================================

configuration = sib_api_v3_sdk.Configuration()

configuration.api_key['api-key'] = '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'

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(

    sib_api_v3_sdk.ApiClient(configuration)

)

# ======================================
# CONFIG TWILIO
# ======================================

account_sid = "ACc0d8988b16c736aeb6faa8731065d7fd"

auth_token = "9bc3b5b6e94027dcd7dad5ba692917f9"

twilio_client = Client(
    account_sid,
    auth_token
)

# ======================================
# NAVEGADOR
# ======================================

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

# ======================================
# LOOP CLIENTES
# ======================================

for _, row in df_clientes.iterrows():

    cliente = row["cliente"]
    email = row["email"]
    whatsapp = str(row["whatsapp"])
    plan = row["plan"]
    proceso = row["proceso"]

    print(f"\n🔎 Consultando: {cliente}")

    try:

        # ======================================
        # ABRIR PORTAL
        # ======================================

        driver.get(
            "https://consultaprocesos.ramajudicial.gov.co/"
        )

        time.sleep(5)

        # ======================================
        # CLICK NUMERO RADICACION
        # ======================================

        cards = driver.find_elements(By.CLASS_NAME, "v-card")

        cards[0].click()

        time.sleep(3)

        # ======================================
        # TODOS LOS PROCESOS
        # ======================================

        todos = driver.find_element(
            By.XPATH,
            "//*[contains(text(),'Todos los Procesos')]"
        )

        todos.click()

        time.sleep(2)

        # ======================================
        # ESCRIBIR PROCESO
        # ======================================

        campo = driver.find_element(

            By.XPATH,

            "//input[contains(@placeholder,'Ingrese los 23 dígitos')]"

        )

        campo.send_keys(str(proceso))

        time.sleep(2)

        # ======================================
        # CONSULTAR
        # ======================================

        botones = driver.find_elements(By.TAG_NAME, "button")

        for boton in botones:

            if "CONSULTAR" in boton.text:

                boton.click()

                break

        print("✅ Consulta ejecutada")

        time.sleep(5)

        # ======================================
        # VALIDAR PROCESO
        # ======================================

        if "no generó resultados" in driver.page_source:

            print(f"❌ Proceso no encontrado: {proceso}")

            continue

        # ======================================
        # ESPERAR TABLA
        # ======================================

        WebDriverWait(driver, 30).until(

            EC.presence_of_element_located(
                (By.TAG_NAME, "tr")
            )

        )

        filas = driver.find_elements(By.TAG_NAME, "tr")

        print(f"Filas encontradas: {len(filas)}")

        if len(filas) < 2:

            print(f"❌ Sin datos para: {proceso}")

            continue

        # ======================================
        # EXTRAER DATOS
        # ======================================

        fila = filas[1]

        texto = fila.text

        print(texto)

        lineas = texto.split("\n")

        if len(lineas) < 6:

            print(f"❌ Datos incompletos: {proceso}")

            continue

        numero_proceso = lineas[0]

        fecha_radicacion = lineas[1]

        fecha_actuacion = lineas[2]

        # ======================================
        # SOLO PARA PRUEBAS
        # ======================================

        fecha_actuacion = "2037-01-01"

        juzgado = lineas[3]

        demandante = lineas[4]

        demandado = lineas[5]

        # ======================================
        # CONSULTAR ULTIMA FECHA
        # ======================================

        cursor.execute("""

        SELECT fecha_actuacion

        FROM procesos

        WHERE numero_proceso = %s

        ORDER BY id DESC

        LIMIT 1

        """, (numero_proceso,))

        resultado = cursor.fetchone()

        # ======================================
        # DETECTAR CAMBIO
        # ======================================

        if resultado:

            fecha_anterior = resultado[0]

            if fecha_anterior != fecha_actuacion:

                print("🚨 CAMBIO DETECTADO")

                print("Anterior:", fecha_anterior)

                print("Nuevo:", fecha_actuacion)

                mensaje = f"""

🚨 Nexus Legal AI

Cliente: {cliente}

Proceso: {numero_proceso}

Nueva actuación detectada

Fecha: {fecha_actuacion}

"""

                # ======================================
                # ENVIAR WHATSAPP
                # ======================================

                try:

                    twilio_client.messages.create(

                        from_='whatsapp:+14155238886',

                        body=mensaje,

                        to=f'whatsapp:+{whatsapp}'

                    )

                    print("📲 WhatsApp enviado")

                except Exception as e:

                    print("❌ Error WhatsApp:", e)

                # ======================================
                # ENVIAR EMAIL
                # ======================================

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

                        <p><b>Cliente:</b> {cliente}</p>

                        <p><b>Proceso:</b> {numero_proceso}</p>

                        <p><b>Nueva actuación:</b> {fecha_actuacion}</p>

                        <p>Ingrese al dashboard para revisar detalles.</p>

                        """

                    )

                    api_instance.send_transac_email(
                        send_smtp_email
                    )

                    print("📧 Email enviado")

                except Exception as e:

                    print("❌ Error Email:", e)

            else:

                print("✅ Sin cambios")

        else:

            print("🆕 Proceso nuevo")

        # ======================================
        # GUARDAR REGISTRO
        # ======================================

        cursor.execute("""

        INSERT INTO procesos (

            cliente,
            email,
            whatsapp,
            plan,

            numero_proceso,
            fecha_actuacion,
            juzgado,
            demandante,
            demandado

        )

        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)

        """, (

            cliente,
            email,
            whatsapp,
            plan,

            numero_proceso,
            fecha_actuacion,
            juzgado,
            demandante,
            demandado

        ))

        conn.commit()

        print(f"✅ Guardado: {cliente}")

    except Exception as e:

        conn.rollback()

        print(f"❌ Error con {cliente}: {e}")

# ======================================
# CERRAR
# ======================================

conn.close()

driver.quit()

print("\n🚀 SISTEMA MULTICLIENTE FINALIZADO")