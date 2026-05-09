from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3

# ======================================
# CONFIGURAR NAVEGADOR
# ======================================

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

# ======================================
# ABRIR PORTAL
# ======================================

url = "https://consultaprocesos.ramajudicial.gov.co/"

driver.get(url)

# ======================================
# CONEXION SQLITE
# ======================================

conn = sqlite3.connect("procesos.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS procesos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_proceso TEXT,
    fecha_actuacion TEXT,
    juzgado TEXT,
    demandante TEXT,
    demandado TEXT
)
""")

conn.commit()

time.sleep(5)

# ======================================
# CLICK EN "Número de Radicación"
# ======================================

cards = driver.find_elements(By.CLASS_NAME, "v-card")

cards[0].click()

time.sleep(5)

# ======================================
# SELECCIONAR TODOS LOS PROCESOS
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

campo.send_keys("11001310300120230012300")

time.sleep(2)

# ======================================
# CLICK BOTÓN CONSULTAR
# ======================================

botones = driver.find_elements(By.TAG_NAME, "button")

for boton in botones:

    if "CONSULTAR" in boton.text:
        boton.click()
        break

print("✅ Consulta ejecutada")

# ======================================
# EXTRAER TABLA
# ======================================

# esperar tabla real

WebDriverWait(driver, 30).until(

    EC.presence_of_element_located(
        (By.TAG_NAME, "tr")
    )

)

filas = driver.find_elements(By.TAG_NAME, "tr")

print(f"Filas encontradas: {len(filas)}")

for fila in filas[1:]:

    texto = fila.text

    print("---------------")
    print(texto)

    lineas = texto.split("\n")

    try:

        proceso = lineas[0]

        fecha_radicacion = lineas[1]

        fecha_actuacion = lineas[2]

        juzgado = lineas[3]

        demandante = lineas[4]

        demandado = lineas[5]

        print("\n===== DATOS EXTRAIDOS =====")

        print("Proceso:", proceso)

        print("Fecha actuación:", fecha_actuacion)

        print("Juzgado:", juzgado)

        print("Demandante:", demandante)

        print("Demandado:", demandado)

        # ======================================
        # GUARDAR EN SQLITE
        # ======================================

        cursor.execute("""

        INSERT INTO procesos (
            numero_proceso,
            fecha_actuacion,
            juzgado,
            demandante,
            demandado
        )

        VALUES (?, ?, ?, ?, ?)

        """, (

            proceso,
            fecha_actuacion,
            juzgado,
            demandante,
            demandado

        ))

        conn.commit()

        print("✅ Guardado en SQLite")

    except Exception as e:

        print("❌ Error extrayendo:", e)

# ======================================
# CLICK EN RESULTADO DEL PROCESO
# ======================================

time.sleep(60)

conn.close()

driver.quit()