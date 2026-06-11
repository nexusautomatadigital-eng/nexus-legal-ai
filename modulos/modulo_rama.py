import time
import hashlib

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

# ==========================================
# CONSULTAR RAMA
# ==========================================

def consultar_rama(driver, numero_proceso):

    try:

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

            return None

        # =====================================
        # ESPERAR TABLA
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

        filas = driver.find_elements(

            By.XPATH,

            "//table//tr"

        )

        print(f"📄 Filas encontradas: {len(filas)}")

        if len(filas) < 2:

            return None

        fila = filas[1]

        texto = fila.text

        print(texto)

        lineas = texto.split("\n")

        if len(lineas) < 6:

            return None

        numero_actual = lineas[0]

        fecha_radicacion = lineas[1]

        fecha_actuacion = lineas[2]

        juzgado = lineas[3]

        demandante = lineas[4]

        demandado = lineas[5]

        demandante = demandante.replace(
            "DEMANDANTE:",
            ""
        ).replace(
            "Demandante:",
            ""
        ).strip()

        demandado = demandado.replace(
            "Demandado:",
            ""
        ).replace(
            "Demandado:",
            ""
        ).strip()

        #texto_hash = f"""
        #{fecha_actuacion}
        #{juzgado}
        #{demandante}
        #{demandado}
        #"""

        #nuevo_hash = hashlib.md5(
        #    texto_hash.encode()
        #).hexdigest()

        payload = {

            "numero_proceso": numero_actual,

            "fuente": "RAMA",

            "jurisdiccion": "ORDINARIA",

            "especialidad": "CIVIL",

            "despacho": juzgado,

            "metadata": {

                "fecha_radicacion": fecha_radicacion,

                "demandante": demandante,

                "demandado": demandado,

                "origen": "Rama Judicial",

                "sistema": "Consulta Procesos",

                 "fecha_consulta": time.strftime(
                    "%Y-%m-%d %H:%M:%S"

                )

            },

            "actuaciones": [

                {

                    "fecha_actuacion": fecha_actuacion,

                    "tipo_actuacion": "ULTIMA_ACTUACION",

                    "detalle": (

                        f"Demandante: {demandante} | "
                        f"Demandado: {demandado}"
                        
                    ),

                    "metadata": {

                        "fuente": "RAMA",

                        "origen": "Consulta Procesos Rama Judicial"

                    }

                }

            ],

            "documentos": []

        }

        return payload
    
        print()

        print("🔥 PAYLOAD RAMA V2")

        print(payload)    

    except Exception as e:

        print(f"❌ ERROR RAMA: {e}")

        return None
        