from services.db import get_connection

from services.hash_service import (
    generar_hash_actuacion
)

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from modulos.modulo_samai import consultar_samai

print("🚨 MONITOR CARGADO")

def existe_alerta(hash_actuacion):

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""

            select id

            from alertas_v2

            where hash_actuacion = %s

            limit 1

        """, (

            hash_actuacion,

        ))

        resultado = cur.fetchone()

        return resultado is not None

    finally:

        cur.close()
        conn.close()

def crear_alerta(

    proceso_id,
    hash_actuacion,
    titulo,
    mensaje,
    fuente="SAMAI"

):

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""

            insert into alertas_v2 (

                proceso_id,
                fuente,
                tipo_alerta,
                hash_actuacion,
                titulo,
                mensaje,
                canal,
                enviada,
                leida

            )

            values (

                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                false,
                false

            )

        """, (

            proceso_id,
            fuente,
            "NUEVA_ACTUACION",
            hash_actuacion,
            titulo,
            mensaje,
            "DASHBOARD"

        ))

        conn.commit()

        print("🚨 ALERTA CREADA")

    finally:

        cur.close()
        conn.close()


def verificar_novedades():

    print("🚀 VERIFICANDO NOVEDADES")

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""

            select
                id,
                numero_proceso,
                fuente

            from procesos_v2

            order by created_at desc

            limit 20

        """)

        procesos = cur.fetchall()

        print(f"📂 PROCESOS ENCONTRADOS: {len(procesos)}")

        for proceso in procesos:

            proceso_id = proceso[0]
            numero_proceso = proceso[1]
            fuente = proceso[2]

            print(f"🔍 MONITOREANDO {numero_proceso}")

            if fuente == "SAMAI":

                chrome_options = Options()

                driver = webdriver.Chrome(

                    service=Service(
                        ChromeDriverManager().install()
                    ),

                    options=chrome_options

                )

                try:

                    resultado = consultar_samai(

                        driver,

                        numero_proceso

                    )

                    print("✅ CONSULTA FINALIZADA")

                    if resultado:

                        actuaciones = resultado.get(
                            "actuaciones",
                            []
                        )

                        print(
                            f"📌 ACTUACIONES RECIBIDAS: "
                            f"{len(actuaciones)}"
                        )

                        for actuacion in actuaciones:

                            hash_actuacion = generar_hash_actuacion(

                                numero_proceso,

                                actuacion

                            )

                            procesar_actuacion(

                                proceso_id,

                                actuacion,

                                hash_actuacion

                            )

                finally:

                    driver.quit()
                    

    except Exception as e:

        print(f"❌ ERROR MONITOR: {e}")

    finally:

        cur.close()
        conn.close()

def procesar_actuacion(
    proceso_id,
    actuacion,
    hash_actuacion
):

    if existe_alerta(hash_actuacion):

        print(
            f"⚠️ ALERTA YA EXISTE: "
            f"{hash_actuacion}"
        )

        return

    titulo = actuacion.get(
        "tipo_actuacion",
        "Nueva actuación"
    )

    mensaje = actuacion.get(
        "detalle",
        ""
    )[:500]

    crear_alerta(

        proceso_id=proceso_id,

        hash_actuacion=hash_actuacion,

        titulo=titulo,

        mensaje=mensaje

    )



