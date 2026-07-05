import time

import hashlib

import re

import json

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support.ui import Select

from selenium.webdriver.support import expected_conditions as EC


# ==========================================
# CONSULTAR PUBLICACIONES
# ==========================================

def consultar_publicaciones(

    driver,
    conn,
    juzgado,
    especialidad,
    departamento,
    municipio

):

    try:

        print("🔎 CONSULTANDO PUBLICACIONES")

        # ======================================
        # ABRIR PORTAL
        # ======================================

        url_publicaciones = (
            "https://publicacionesprocesales.ramajudicial.gov.co/"
        )

        publicaciones_payload = []

        for intento in range(3):

            print(f"🌐 Intento portal: {intento+1}")

            print("ANTES DRIVER.GET")

            # ======================================
            # LIMPIAR PESTAÑAS ANTERIORES
            # ======================================

            while len(driver.window_handles) > 1:

                driver.switch_to.window(
                    driver.window_handles[-1]
                )

                print("🗑️ Cerrando pestaña anterior")

                driver.close()

            driver.switch_to.window(
                driver.window_handles[0]
            )

            print("✅ Solo queda la pestaña principal")

            driver.execute_script("window.open('');")

            driver.switch_to.window(
                driver.window_handles[-1]
            )

            print("NUEVA PESTAÑA ABIERTA")

            #driver.get(url_publicaciones)

            driver.set_page_load_timeout(30)

            driver.get(url_publicaciones)

            print("PORTAL ABIERTO")

            print("DESPUES DRIVER.GET")

            print("PASO 1")
            
            time.sleep(8)

            print("PASO 2")

            html = driver.page_source.lower()

            print("PASO 3")

            if (

                "error inesperado del sistema" not in html
                and
                "unable to process template" not in html

            ):

                print("✅ Portal cargado correctamente")

                break

            print("⚠️ Portal con error interno")

            time.sleep(5)

            if (

                "error inesperado del sistema" in html
                or
                "unable to process template" in html

            ):

                print("❌ PORTAL RAMA INESTABLE")

                return {

                    "fuente": "PUBLICACIONES",

                    "estado": "INACTIVO",

                    "fecha_revision": time.strftime("%Y-%m-%d %H:%M:%S")

                }

        # ======================================
        # VALIDAR CARGA
        # ======================================

        time.sleep(10)

        selects = driver.find_elements(
            By.TAG_NAME,
            "select"
        )

        print(f"📋 Selects encontrados: {len(selects)}")

        print("✅ Portal publicaciones cargado")

        print(driver.current_url)

        print("🌐 HTML RECIBIDO OK")

        # ======================================
        # VALIDAR ERROR PORTAL
        # ======================================

        html = driver.page_source.lower()

        if (

            "error inesperado del sistema" in html
            or
            "unable to process template" in html

        ):

            print("🚨 PORTAL RAMA DEVOLVIO ERROR INTERNO")

            return None

        # ======================================
        # DEBUG TITULO
        # ======================================

        print("TITULO:", driver.title)

        # ======================================
        # DEBUG IFRAMES
        # ======================================

        iframes = driver.find_elements(
           By.TAG_NAME,
            "iframe"
        )

        print(f"🪟 Iframes encontrados: {len(iframes)}")

              
        # ======================================
        # DEBUG DIVS
        # ======================================

        # ======================================
        # BUSCAR INPUTS REALES
        # ======================================

        inputs = driver.find_elements(
            By.TAG_NAME,
            "input"
        )

        print(f"🔎 Inputs encontrados: {len(inputs)}")

        for i, inp in enumerate(inputs):

            try:

                tipo = inp.get_attribute("type")

                nombre = inp.get_attribute("name")

                placeholder = inp.get_attribute("placeholder")

                value = inp.get_attribute("value")

                print(
                    f"{i} | type={tipo} | name={nombre} | placeholder={placeholder} | value={value}"
                )

            except:

                pass

        divs = driver.find_elements(
            By.TAG_NAME,
            "div"
        )

        print(f"📦 Divs encontrados: {len(divs)}")

        # ======================================
        # BUSCAR SELECTS
        # ======================================

        selects = driver.find_elements(
            By.TAG_NAME,
            "select"
        )

        print(f"📋 Selects encontrados: {len(selects)}")

        if len(selects) == 0:

            print("❌ PORTAL NO CARGO SELECTS")

            return {
                "fuente": "PUBLICACIONES",

                "estado": "PORTAL_INDISPONIBLE",

                "fecha_revision": time.strftime("%Y-%m-%d %H:%M:%S")

            }                 
        
        for i, sel in enumerate(selects):

            try:

                print(

                    f"{i} | ID={sel.get_attribute('id')} | NAME={sel.get_attribute('name')}"

                )

            except:

                pass

        time.sleep(3)

        # ======================================
        # SELECCIONAR DEPARTAMENTO
        # ======================================

        select_departamento = Select(

            selects[1]
            
        )

        print("\n===== DEPARTAMENTOS DISPONIBLES =====")

        for opt in select_departamento.options:

            print(opt.text)
            

        select_departamento.select_by_visible_text(
            departamento
        )

        print("PASO 4")

        print("✅ Departamento seleccionado")

        print(
            "DEP SELECCIONADO:",
            select_departamento.first_selected_option.text
        )

        WebDriverWait(driver, 15).until(
            lambda d: len(
                Select(selects[2]).options
            ) > 1
        )

        time.sleep(5)
       
        # ======================================
        # SELECCIONAR MUNICIPIO
        # ======================================

        select_municipio = Select(

           selects[2]

        )

        print("\n===== MUNICIPIOS DISPONIBLES =====")

        for opt in select_municipio.options:

            print(opt.text)

        # ======================================
        # NORMALIZAR MUNICIPIOS
        # ======================================

        MUNICIPIOS_MAP = {

            "BOGOTÁ": "BOGOTÁ D.C.",

        }

        municipio = MUNICIPIOS_MAP.get(

            municipio,

            municipio

        )

        print(

            "MUNICIPIO NORMALIZADO:",

            municipio

        )

        select_municipio.select_by_visible_text(
            municipio
        )

        print("PASO 5")

        print("✅ Municipio seleccionado")
        
        print(
            "MUN SELECCIONADO:",
            select_municipio.first_selected_option.text
        )
       
        WebDriverWait(driver, 15).until(
            lambda d: len(
                Select(selects[5]).options
            ) > 1
        )        

        time.sleep(5)


        # ======================================
        # SELECCIONAR ENTIDAD
        # ======================================

        select_entidad = Select(

            selects[3]

        )

        print("\n===== ENTIDADES DISPONIBLES =====")

        for opt in select_entidad.options:

            print(
                opt.get_attribute("value"),
                "|",
                opt.text
            )

        #select_entidad.select_by_value("31")

        print("✅ Entidad seleccionada")

        time.sleep(5)

        # ======================================
        # SELECCIONAR ESPECIALIDAD
        # ======================================

        select_especialidad = Select(

            selects[4]

        )

        # ======================================
        # DEBUG OPCIONES ESPECIALIDAD
        # ======================================

        print("\n===== OPCIONES ESPECIALIDAD =====")

        for opcion in select_especialidad.options:

            print(opcion.text)

        print("===============================\n")

        # ======================================
        # NORMALIZAR ESPECIALIDAD
        # ======================================

        especialidad_portal = especialidad.upper()

        if especialidad_portal == "ADMINISTRATIVO":

            especialidad_portal = "ADMINISTRATIVA"

        print("Especialidad portal:", especialidad_portal)

        select_especialidad.select_by_visible_text(
            especialidad_portal
        )

        print("PASO 6")

        print("✅ Especialidad seleccionada")

        print(
            "ESP SELECCIONADA:",
            select_especialidad.first_selected_option.text
        )
        
        # ======================================
        # SELECCIONAR DESPACHO DINAMICO
        # ======================================

        # ======================================
        # ESPERAR DESPACHOS
        # ======================================

        print("⏳ Esperando carga de despachos...")

        print("\n========== SELECT DESPACHO ==========")

        selects = driver.find_elements(By.TAG_NAME, "select")

        print("TOTAL SELECTS:", len(selects))

        for i, sel in enumerate(selects):

            opciones = Select(sel).options

            print(
                f"SELECT {i} -> {len(opciones)} opciones"
            )

            for op in opciones[:10]:
                print("   ", op.text)

        print("=====================================\n")

        WebDriverWait(driver,30).until(

            lambda d: len(

                Select(

                    d.find_elements(By.TAG_NAME,"select")[5]

                ).options

            ) > 1

        )

        selects = driver.find_elements(
            By.TAG_NAME,
            "select"
        )

        select_despacho = Select(
            selects[5]
        )

        print("✅ Despachos cargados")

        juzgado_busqueda = juzgado.upper()

        if "(" in juzgado_busqueda:

            juzgado_busqueda = (
                juzgado_busqueda.split("(")[0]
                .strip()
            )

        print("JUZGADO NORMALIZADO:", juzgado_busqueda)
        
        despacho_encontrado = False

        print("\n========== DESPACHOS DISPONIBLES ==========\n")

        for opt in select_despacho.options:

            print(opt.text)

        print("\n===========================================\n")

        for opt in select_despacho.options:

            texto_opcion = opt.text.upper()

            print("COMPARANDO:")
            print("BUSCADO :", juzgado_busqueda)
            print("PORTAL  :", texto_opcion)

            if juzgado_busqueda in texto_opcion:

                opt.click()

                despacho_encontrado = True

                print("✅ DESPACHO ENCONTRADO:")

                print(opt.text)

                break

        if not despacho_encontrado:

            print(
                "❌ NO SE ENCONTRO DESPACHO"
            )

            print(
                "JUZGADO BUSCADO:",
                juzgado
            )       

            return []

        print("✅ Despacho seleccionado")

        time.sleep(5)             
              
        # ======================================
        # CLICK INPUT BUSCAR
        # ======================================

        boton_buscar = driver.find_element(

            By.XPATH,

            "//input[@value='Buscar']"

        )

        boton_buscar.click()

        print("🚀 Busqueda ejecutada")

        time.sleep(10)

        # ======================================
        # VALIDAR RESULTADOS
        # ======================================

        links = driver.find_elements(
            By.TAG_NAME,
            "a"
        )

        print(f"🔗 Links encontrados: {len(links)}")

        hrefs = []

        for link in links:

            try:

                texto = link.text.strip()

                href = link.get_attribute("href")

                if (

                    href
                    and
                    "articleId" in href
                    and
                    texto != "VER DETALLE"

                ):

                    hrefs.append(href)

            except:

                pass

        print(
            f"📄 PUBLICACIONES FILTRADAS: {len(hrefs)}"
        )

        for href in hrefs:

            try:

                print("\n🔥 PUBLICACION ENCONTRADA")

                print(f"LINK: {href}")

                detalle = extraer_detalle_publicacion(

                    driver,

                    href

                )

                if detalle:

                    publicaciones_payload.append(
                        detalle
                    )

            except Exception as e:

                print(
                    f"❌ ERROR DETALLE: {e}"
                )


                    # ======================================
                    # VALIDAR SI YA EXISTE
                    # ======================================

                    #if conn:

                        #cursor = conn.cursor()

                        #cursor.execute("""

                        #SELECT hash_publicacion

                        #FROM publicaciones

                        #WHERE article_id = %s

                        #""", (

                            #detalle["article_id"],

                        #))

                        #existe = cursor.fetchone()

                        # ======================================
                        # VALIDAR CAMBIO HASH
                        # ======================================

                        #if existe:

                            #hash_guardado = existe[0]

                            #if hash_guardado != detalle["hash_publicacion"]:

                                #print("🚨 CAMBIO DETECTADO EN PUBLICACION")

                                #cursor.execute("""

                                #UPDATE publicaciones

                                #SET

                                    #detalle = %s,
                                    #hash_publicacion = %s,
                                    #pdf_url = %s,
                                    #fecha_consulta = NOW(),
                                    #actualizado = TRUE

                                #WHERE article_id = %s

                                #""", (

                                    #detalle["detalle"],
                                    #detalle["hash_publicacion"],
                                    #detalle["pdf_url"],
                                    ##detalle["article_id"]

                                #))

                                #conn.commit()

                                #print("✅ PUBLICACION ACTUALIZADA")

                            #else:

                                #print("✅ Publicación sin cambios")

                            #continue
                    
                        # ======================================
                        # NUEVA PUBLICACION
                        # ======================================

                        #if not existe:

                            #print("🚨 NUEVA PUBLICACION DETECTADA")

                            #cursor.execute("""

                            #INSERT INTO publicaciones (

                                #article_id,
                                #titulo,
                                #url,
                                #despacho,
                                #especialidad,
                                #fecha_publicacion,
                                #detalle,
                                #hash_publicacion,
                                #pdf_url

                            #)

                            #VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)

                            #""", (

                                #detalle["article_id"],
                                #texto,
                                #href,
                                #detalle["despacho"],
                                #detalle["especialidad"],
                                #detalle["fecha_publicacion"],
                                #detalle["detalle"],
                                #detalle["hash_publicacion"],
                                #detalle["pdf_url"]

                            #))

                            #conn.commit()

                            #print("✅ PUBLICACION GUARDADA")

                    #else:

                        #print("✅ Publicación ya existente")

                   
            except Exception as e:

                print(f"❌ ERROR LOOP PUBLICACION: {e}")

        # ======================================
        # RESULTADO BASE
        # ======================================

        # resultado = {
        

            #"fuente": "PUBLICACIONES",
            #"estado": "CONECTADO",
            #"juzgado": juzgado,
            #"especialidad": especialidad,
            #"departamento": departamento,
            #"municipio": municipio,
            #"fecha_revision": time.strftime("%Y-%m-%d %H:%M:%S")
        #}

        print()

        print("🔥 TOTAL PUBLICACIONES PAYLOAD")

        print(len(publicaciones_payload))

        return publicaciones_payload
        
        
    except Exception as e:

        print("❌ ERROR PUBLICACIONES")

        print(type(e))

        print(e)

        return []
    
# ==========================================
# EXTRAER DETALLE PUBLICACION
# ==========================================

def extraer_detalle_publicacion(

    driver,
    url

):
    pdf_urls = []

    article_id = None

    if "articleId=" in url:

        article_id = url.split("articleId=")[1].split("&")[0]

    print(f"🆔 ARTICLE ID: {article_id}")

    try:

        print("\n🚀 ABRIENDO DETALLE")

        # ======================================
        # NUEVA PESTAÑA
        # ======================================

        driver.execute_script(

            "window.open('');"

        )

        driver.switch_to.window(
            driver.window_handles[-1]
        )

        driver.get(url)

        time.sleep(8)

        # ======================================
        # BODY
        # ======================================

        body = driver.find_element(
            By.TAG_NAME,
            "body"
        )

        texto = body.text

        # ======================================
        # EXTRACCION METADATA
        # ======================================

        despacho = None

        especialidad = None

        fecha_publicacion = None

        lineas = texto.split("\n")

        for linea in lineas:

            linea_upper = linea.upper()

            # ==================================
            # DESPACHO
            # ==================================

            if (

                "JUZGADO" in linea_upper
                and
                "UBICACIÓN" not in linea_upper
                and
                "DESPACHOS" not in linea_upper

            ):
                
                despacho = linea.strip()

            # ==================================
            # ESPECIALIDAD
            # ==================================

            if "CIVIL" in linea_upper:

                especialidad = "CIVIL"

            elif "PENAL" in linea_upper:

                especialidad = "PENAL"

            elif "LABORAL" in linea_upper:

                especialidad = "LABORAL"

            elif "ADMINISTRATIVO" in linea_upper:

                especialidad = "ADMINISTRATIVO"

            # ==================================
            # FECHA
            # ==================================

            if (

                fecha_publicacion is None

                and

                re.search(
                    r"\d{1,2}\s[a-zA-Z]{3}\s\d{4}",
                    linea
                )

            ):

                fecha_publicacion = linea.strip()

        # ======================================
        # HASH PUBLICACION
        # ======================================

        hash_publicacion = hashlib.md5(

            texto.encode()

        ).hexdigest()

        print(f"🔐 HASH: {hash_publicacion}")

        print("\n========== DETALLE ==========\n")

        print(texto[:5000])

        # ======================================
        # PDFS
        # ======================================

        pdfs = driver.find_elements(
            By.TAG_NAME,
            "a"
        )        

        print(
            f"📄 PDFS REALES: {len(pdf_urls)}"
        )

        for pdf in pdfs:

            try:

                texto_pdf = pdf.text.strip()

                href = pdf.get_attribute("href")

                onclick = pdf.get_attribute("onclick")

                print("\n====== LINK ======")

                print(f"TEXTO: {texto_pdf}")

                print(f"HREF: {href}")

                print(f"ONCLICK: {onclick}")

                # ==================================
                # DETECTAR PDF POR TEXTO
                # ==================================

                if ".pdf" in texto_pdf.lower():

                    print("✅ PDF DETECTADO")

                    pdf_url = None

                    # ==================================
                    # URL DIRECTA
                    # ==================================

                    if href and href != "#":

                        pdf_url = href

                    # ==================================
                    # URL EN ONCLICK
                    # ==================================

                    elif onclick:

                        pdf_url = onclick

                    # ==================================
                    # AGREGAR PDF
                    # ==================================

                    if pdf_url:

                        pdf_urls.append(pdf_url)

                        print(f"📄 PDF URL: {pdf_url}")

                    
            except Exception as e:

                print(f"❌ ERROR PDF: {e}")
        # ======================================
        # CERRAR PESTAÑA
        # ======================================

        driver.close()

        driver.switch_to.window(
            driver.window_handles[0]
        )

        print("\n===== DEBUG PDF URLS =====")
        print("TOTAL PDF URLS:")
        print(len(pdf_urls))


        for pdf in pdf_urls[:10]:
            print(pdf)

        if "No hay documentos asociados" in texto:

            print("🚫 PUBLICACION SIN PDF")

        else:

            print("✅ POSIBLE PUBLICACION CON PDF")
        
        payload = {

            "numero_proceso": f"PUB_{article_id}",

            "fuente": "PUBLICACIONES",

            "jurisdiccion": "PUBLICACIONES",

            "especialidad": especialidad,

            "despacho": despacho,

            "metadata": {

                "article_id": article_id,

                "fecha_publicacion": fecha_publicacion,

                "fecha_estado": fecha_publicacion,

                "despacho": despacho,

                "especialidad": especialidad,

                "url_publicacion": url,

                "hash_publicacion": hash_publicacion,

                "cantidad_documentos": len(pdf_urls)

            },

            "actuaciones": [

                {

                    "fecha_actuacion": fecha_publicacion,

                    "tipo_actuacion": "PUBLICACION_PROCESAL",

                    "detalle": texto,

                    "metadata": {}

                }

            ],

            "documentos": [

                {

                    "nombre": f"PUBLICACION_{article_id}",
                    "tipo_documento": "PDF_PUBLICACION",
                    "url_publica": pdf,
                    "publico": True,
                    "metadata": {}

                }

                for pdf in pdf_urls

            ]

        }

        print("\n===== DEBUG DOCUMENTOS =====")

        print(
            len(
                payload["documentos"]
            )
        )
    
        print()
        print("🔥 PAYLOAD PUBLICACIONES")
        print(payload)

        return payload


    except Exception as e:

        print(f"❌ ERROR DETALLE: {e}")

        return None