import time

print("🔥🔥🔥 MODULO_SAMAI CORRECTO CARGADO")
print(__file__)

import json

import hashlib

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.action_chains import ActionChains

# ==========================================
# EXTRAER DOCUMENTOS SAMAI
# ==========================================

def extraer_documentos_samai(driver):

    documentos = []

    pdf_urls = []

    try:

        links = driver.find_elements(
            By.TAG_NAME,
            "a"
        )

        for link in links:

            try:

                texto = (
                    link.text or ""
                ).strip()

                href = link.get_attribute(
                    "href"
                )

                if not href:

                    continue

                # ==================================
                # URL PUBLICA PDF
                # ==================================

                if (
                    "DescargarProvidencia" in href
                    or "tokendoc=" in href
                ):

                    pdf_urls.append(
                        href
                    )

                # ==================================
                # DOCUMENTOS EXPEDIENTE
                # ==================================

                if (
                    "Expediente Digital" in texto
                    or "ED_" in texto
                ):

                    lineas = texto.split("\n")

                    nombre_doc = ""

                    tamano_doc = ""

                    if len(lineas) >= 2:

                       nombre_doc = lineas[1]

                    if len(lineas) >= 3:

                        tamano_doc = lineas[2]

                    documento = {

                        "nombre": nombre_doc,

                        "tipo_documento":
                        "EXPEDIENTE",

                        "tamano":
                        tamano_doc,

                        "url_publica":
                        None,

                        "publico":
                        True

                    }

                    documentos.append(
                        documento
                    )

            except Exception as e:

                print(
                    f"❌ ERROR DOCUMENTO: {e}"
                )

        return {

            "documentos": documentos,

            "pdf_urls": pdf_urls

        }

    except Exception as e:

        print(                
            f"❌ ERROR DOCUMENTOS SAMAI: {e}"
        )

        return {

            "documentos": [],

            "pdf_urls": []

        }
# ==========================================
# GENERAR PAYLOAD SAMAI
# ==========================================

def generar_payload_samai(

    radicado,
    actuaciones,
    documentos,
    pdf_urls

):

    try:

        # ======================================
        # HASH
        # ======================================

        texto_hash = ""

        for act in actuaciones:

            texto_hash += (
                act.get(
                    "fecha_actuacion",
                    ""
                )
            )

            texto_hash += (
                act.get(
                    "tipo_actuacion",
                        ""
                )
            )

        for doc in documentos:

            texto_hash += (
                doc.get(
                    "nombre",
                    ""
                )
            )

        nuevo_hash = hashlib.md5(

            texto_hash.encode()

        ).hexdigest()

        # ======================================
        # PAYLOAD NEXUS
        # ======================================

        payload = {

            # ======================================
            # CORE ENTERPRISE
            # ======================================

            "numero_proceso": str(radicado).strip(),

            "fuente": "SAMAI",

            "jurisdiccion":
            "CONTENCIOSO ADMINISTRATIVO",

            "especialidad":
            "ADMINISTRATIVO",

            "despacho":
            "JUZGADO ADMINISTRATIVO",

            "estado_proceso":
            "ACTIVO",

            "fecha_consulta":
            time.strftime("%Y-%m-%d %H:%M:%S"),

            "hash_consulta":
            nuevo_hash,

            # ======================================
            # ACTUACIONES
            # ======================================

            "actuaciones":
            actuaciones,

            # ======================================
            # DOCUMENTOS
            # ======================================

            "documentos":
            documentos,

            "pdf_urls":
            pdf_urls,

            # ======================================
            # METADATA FLEXIBLE
            # ======================================

            "metadata": {

                "origen":
                "Consejo de Estado",

                "sistema":
                "SAMAI",

                "radicado_original":
                str(radicado),

                "cantidad_actuaciones":
                len(actuaciones),

                "cantidad_documentos":
                len(documentos)

            }

        }

        print("🔥 PAYLOAD SAMAI FINAL:")
        print(payload)

        return payload

    except Exception as e:

        print(
            f"❌ ERROR PAYLOAD SAMAI: {e}"
        )

        return None

# ==========================================
# EXTRAER ACTUACIONES SAMAI
# ==========================================

def extraer_actuaciones_samai(driver):

    
    actuaciones = []

    try:

        filas = driver.find_elements(
            By.XPATH,
            "//table//tr"
        )

        for i, fila in enumerate(filas):

            try:

                columnas = fila.find_elements(
                    By.TAG_NAME,
                    "td"
                )

                datos = []

                for col in columnas:

                    texto = col.text.strip()

                    if texto != "":

                        datos.append(texto)

                if len(datos) < 7:

                    continue

                actuacion = {

                    "fecha_registro": datos[0],

                    "fecha_actuacion": datos[1],

                    "tipo_actuacion": datos[2],

                    "detalle": datos[3],

                    "estado": datos[4],

                    "anexos": datos[5],

                    "indice": datos[6]

                }

                actuaciones.append(
                    actuacion
                )

            except Exception as e:

                print(
                    f"❌ ERROR FILA ACTUACION: {e}"
                )

        return actuaciones

    except Exception as e:

        print(
            f"❌ ERROR ACTUACIONES SAMAI: {e}"
        )

        return []

# ==========================================
# CONSULTAR SAMAI
# ==========================================

def consultar_samai(driver, radicado):

    try:

        actuaciones = []

        documentos = []

        pdf_urls = []

        print("🔎 CONSULTANDO SAMAI")

        url = "https://samai.consejodeestado.gov.co/Vistas/Casos/procesos.aspx"

        driver.get(url)

        driver.maximize_window()

        driver.implicitly_wait(10)

        time.sleep(8)

        # ======================================
        # VALIDAR CARGA
        # ======================================

        WebDriverWait(driver, 30).until(

            EC.presence_of_element_located(
                (
                    By.TAG_NAME,
                    "body"
                )
            )

        )

        print("✅ PORTAL SAMAI CARGADO")

        print("TITULO:", driver.title)

        print("URL:", driver.current_url)

        # ======================================
        # INPUTS
        # ======================================

        inputs = driver.find_elements(
            By.TAG_NAME,
            "input"
        )

        print(f"🔎 INPUTS ENCONTRADOS: {len(inputs)}")

        for i, inp in enumerate(inputs):

            try:

                tipo = inp.get_attribute("type")

                nombre = inp.get_attribute("name")

                placeholder = inp.get_attribute("placeholder")

                value = inp.get_attribute("value")

                print(
                    f"{i} | type={tipo} | "
                    f"name={nombre} | "
                    f"placeholder={placeholder} | "
                    f"value={value}"
                )

            except Exception as e:

                print(f"ERROR INPUT: {e}")

        # ======================================
        # BUTTONS
        # ======================================

        botones = driver.find_elements(
            By.TAG_NAME,
            "button"
        )

        print(f"🔘 BOTONES: {len(botones)}")

        for i, btn in enumerate(botones):

            try:

                print(
                    f"{i} | {btn.text}"
                )

            except Exception as e:

                print(f"ERROR BUTTON: {e}")

        # ======================================
        # LINKS
        # ======================================

        links = driver.find_elements(
            By.TAG_NAME,
            "a"
        )

        print(f"🔗 LINKS ENCONTRADOS: {len(links)}")

        for i, link in enumerate(links):

            try:

                texto = link.text.strip()

                href = link.get_attribute("href")

                onclick = link.get_attribute("onclick")

                print(
                    f"{i} | "
                    f"TEXTO={texto} | "
                    f"HREF={href} | "
                    f"ONCLICK={onclick}"
                )

            except Exception as e:

                print(f"ERROR LINK: {e}")

        # ======================================
        # TABLAS
        # ======================================

        tablas = driver.find_elements(
            By.TAG_NAME,
            "table"
        )

        print(f"📄 TABLAS ENCONTRADAS: {len(tablas)}")

        # ======================================
        # FORMS
        # ======================================

        forms = driver.find_elements(
            By.TAG_NAME,
            "form"
        )

        print(f"🧩 FORMS ENCONTRADOS: {len(forms)}")

        for i, form in enumerate(forms):

            try:

                action = form.get_attribute("action")

                method = form.get_attribute("method")

                print(
                    f"{i} | ACTION={action} | METHOD={method}"
                )

            except Exception as e:

                print(f"ERROR FORM: {e}")

        # ======================================
        # SELECTS
        # ======================================

        selects = driver.find_elements(
            By.TAG_NAME,
            "select"
        )

        print(f"📋 SELECTS ENCONTRADOS: {len(selects)}")

        for i, select in enumerate(selects):

            try:

                nombre = select.get_attribute("name")

                select_id = select.get_attribute("id")

                print(
                    f"\nSELECT {i}"
                )

                print(
                    f"NAME={nombre}"
                )

                print(
                    f"ID={select_id}"
                )

                options = select.find_elements(
                    By.TAG_NAME,
                    "option"
                )

                print(
                    f"OPTIONS={len(options)}"
                )

                for j, option in enumerate(options):

                    texto = option.text.strip()

                    value = option.get_attribute("value")

                    print(
                        f"{j} | "
                        f"TEXTO={texto} | "
                        f"VALUE={value}"
                    )

            except Exception as e:

                print(f"ERROR SELECT: {e}")

        # ======================================
        # BUSQUEDA POR RADICADO
        # ======================================

        print("🔎 INICIANDO BUSQUEDA RADICADO")

        # ======================================
        # RADIO RADICADO
        # ======================================

        radio_radicado = driver.find_element(

            By.XPATH,

            "//input[@value='FW_Rbtradicado']"

        )

        driver.execute_script(
            "arguments[0].click();",
            radio_radicado
        )

        time.sleep(2)

        print("✅ RADIO RADICADO SELECCIONADO")

        
        # ======================================
        # SELECT CORPORACION
        # ======================================

        select_corporacion = Select(

            driver.find_element(
                By.ID,
                "FW_LstCorporacion"
            )

        )

        select_corporacion.select_by_value(
            "1500133"
        )

        driver.execute_script("""

            arguments[0].dispatchEvent(
                new Event('change', { bubbles: true })
            );

        """, driver.find_element(By.ID, "FW_LstCorporacion"))

        print(
            "✅ CORPORACION SELECCIONADA"
        )

        time.sleep(3)

        # ======================================
        # INPUT CRITERIO
        # ======================================

        campo = driver.find_element(

            By.NAME,

            "FW_Txtcriterios"

        )

        campo.clear()

        campo.send_keys(str(radicado))


        driver.execute_script("""

            arguments[0].dispatchEvent(
                new Event('input', { bubbles: true })
            );

            arguments[0].dispatchEvent(
                new Event('change', { bubbles: true })
            );

            arguments[0].dispatchEvent(
                new Event('blur', { bubbles: true })
            );

        """, campo)

        print(f"✅ RADICADO INGRESADO: {radicado}")

        time.sleep(2)

        # ======================================
        # DEBUG BOTONES HTML
        # ======================================

        botones = driver.find_elements(
            By.TAG_NAME,
            "button"
        )

        print("===================================")

        print("HTML BOTONES")

        print("===================================")

        for i, btn in enumerate(botones):

            try:

                html = btn.get_attribute(
                    "outerHTML"
                )

                print(f"\nBOTON {i}")

                print(html)

            except Exception as e:

                print(e)

        # ======================================
        # CLICK HUMANO REAL
        # ======================================

        boton_buscar = WebDriverWait(driver, 30).until(

            EC.element_to_be_clickable(
                (
                    By.ID,
                    "FW_buscarnormal"
                )
            )

        )

        # ======================================
        # SCROLL
        # ======================================

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            boton_buscar
        )

        time.sleep(2)

        print("🚀 EJECUTANDO ACTION CHAINS CLICK")

        acciones = ActionChains(driver)

        acciones.move_to_element(
            boton_buscar
        ).pause(1).click().perform()

        print("✅ ACTION CLICK EJECUTADO")

        time.sleep(20)

        # ======================================
        # DEBUG RESULTADO
        # ======================================

        print("===================================")

        print("URL FINAL:")

        print(driver.current_url)

        print("===================================")

        print("TITULO FINAL:")

        print(driver.title)

        print("===================================")

        print("HTML RESULTADO:")

        print(driver.page_source[:5000])

        print("===================================")

        print("CANVAS PDF")

        print("===================================")

        canvas = driver.find_elements(
            By.TAG_NAME,
            "canvas"
        )

        print(f"TOTAL CANVAS: {len(canvas)}")

        for i, c in enumerate(canvas):

            try:

                print(f"\nCANVAS {i}")

                print(c.get_attribute("outerHTML")[:500])

            except Exception as e:

                print(e)

        print("===================================")

        print("EMBEDS")

        print("===================================")

        embeds = driver.find_elements(
            By.TAG_NAME,
            "embed"
        )

        print(f"TOTAL EMBEDS: {len(embeds)}")

        for i, emb in enumerate(embeds):

            try:

                print(f"\nEMBED {i}")

                print(emb.get_attribute("src"))

            except Exception as e:

                print(e)

        print("===================================")

        print("OBJECT PDF")

        print("===================================")

        objetos = driver.find_elements(
            By.TAG_NAME,
            "object"
        )

        print(f"TOTAL OBJECTS: {len(objetos)}")

        for i, obj in enumerate(objetos):

            try:

                print(f"\nOBJECT {i}")

                print(obj.get_attribute("data"))

            except Exception as e:

                print(e)


        # ======================================
        # BOTONES VER
        # ======================================

        botones_ver = driver.find_elements(

            By.XPATH,

            "//button[contains(., 'Ver')]"

        )

        print(
            f"👁️ BOTONES VER: {len(botones_ver)}"
        )

        for i, boton in enumerate(botones_ver):

            try:

                html = boton.get_attribute(
                "outerHTML"
               )

                print(f"\nBOTON VER {i}")

                print(html)

                # ======================================
                # ABRIR EXPEDIENTE
                # ======================================

                print("🚀 ABRIENDO EXPEDIENTE")

                driver.execute_script(f"""

                    goprocs_gestion(
                        '{radicado}',
                        '1500133',
                        '1'
                   );

                """)

                print("✅ FUNCION EXPEDIENTE EJECUTADA")

                time.sleep(15)

                # ======================================
                # CAPTCHA
                # ======================================

                spans = driver.find_elements(
                    By.TAG_NAME,
                    "span"
                )

                captcha_partes = []

                for span in spans:

                    try:

                        texto = span.text.strip()

                        if not texto:
                            continue

                        texto_limpio = texto.replace(
                            " ",
                            ""
                        )

                        if texto_limpio.isdigit():

                            captcha_partes.append(
                                texto_limpio
                            )

                        elif (
                             texto_limpio.isalpha()
                            and len(texto_limpio) <= 4
                        ):

                            captcha_partes.append(
                                texto_limpio
                            )

                    except:
                        pass

                captcha_codigo = ""

                for parte in captcha_partes:

                    captcha_codigo += parte.replace(
                        " ",
                        ""
                    )

                print(f"✅ CAPTCHA: {captcha_codigo}")

                # ======================================
                # INPUT CAPTCHA
                # ======================================

                input_captcha = None

                inputs = driver.find_elements(
                    By.TAG_NAME,
                    "input"
                )

                for inp in inputs:

                    try:

                        tipo = inp.get_attribute("type")

                        value = inp.get_attribute("value")

                        displayed = inp.is_displayed()

                        enabled = inp.is_enabled()

                        if (
                            tipo == "text"
                            and displayed
                            and enabled
                            and value == ""
                        ):

                            input_captcha = inp

                            break

                    except:
                        pass

                if input_captcha:

                    input_captcha.clear()

                    input_captcha.send_keys(
                        captcha_codigo
                    )

                    print(
                        "✅ CAPTCHA INGRESADO"
                    )

                # ======================================
                # CONTINUAR
                # ======================================

                boton_continuar = WebDriverWait(driver, 20).until(

                    EC.element_to_be_clickable(
                        (
                            By.ID,
                            "MainContent_CmdNoRobot"
                        )
                    )

                )

                driver.execute_script(
                    "arguments[0].click();",
                    boton_continuar
                )

                print("✅ CONTINUAR EJECUTADO")

                time.sleep(10)

                # ======================================
                # ACTUACIONES
                # ======================================

                actuaciones = extraer_actuaciones_samai(
                    driver
                )

                print(
                    f"✅ ACTUACIONES EXTRAIDAS: {len(actuaciones)}"
                )

                # ======================================
                # DOCUMENTOS
                # ======================================

                url_docs = (
                    "https://samai.consejodeestado.gov.co/"
                    "PaginasTransversales/"
                    "DocumentosExpediente.aspx"
                    f"?numproceso={radicado}"
                    "&corporacion=1500133"
                )

                driver.get(url_docs)

                time.sleep(10)

                resultado_docs = extraer_documentos_samai(
                    driver
                )

                documentos = resultado_docs[
                    "documentos"
                ]

                pdf_urls = resultado_docs[
                    "pdf_urls"
                ]

                print(
                    f"✅ DOCUMENTOS EXTRAIDOS: {len(documentos)}"
                )

                print(
                    f"✅ PDF URLS EXTRAIDAS: {len(pdf_urls)}"
                )

                break

            except Exception as e:

                print(
                    f"❌ ERROR BLOQUE EXPEDIENTE: {e}"
                )

        # ======================================
        # PAYLOAD FINAL
        # ======================================

        payload = generar_payload_samai(

            radicado,

            actuaciones,

            documentos,

            pdf_urls

        )

        print("===================================")

        print("PAYLOAD FINAL SAMAI")

        print("===================================")

        print(payload)

        # ======================================
        # NEXUS V2
        # ======================================
        #
        # La persistencia fue centralizada
        # en nexus_engine.py mediante:
        #
        # persistir_payload(payload)
        #
        # Este módulo únicamente construye
        # y retorna el payload.
        #
        
        print("✅ PAYLOAD SAMAI GENERADO")

        return payload

    except Exception as e:

        print(f"❌ ERROR SAMAI GENERAL: {e}")

        return None