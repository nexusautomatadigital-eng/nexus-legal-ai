from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import psycopg2
import os

app = FastAPI()

# =========================================
# CONEXIÓN DB
# =========================================

conn = psycopg2.connect(

    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")

)

cursor = conn.cursor()

# =========================================
# HOME
# =========================================

@app.get("/")
def home():

    return {
        "status": "NEXUS WOMPI ONLINE"
    }

# =========================================
# WEBHOOK WOMPI
# =========================================

@app.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    print("WEBHOOK WOMPI:")
    print(data)

    try:

        evento = data["event"]

        if evento == "transaction.updated":

            transaccion = data["data"]["transaction"]

            estado = transaccion["status"]

            referencia = transaccion["reference"]

            monto = transaccion["amount_in_cents"]

            email = transaccion["customer_email"]

            # =====================================
            # VALIDAR APROBADO
            # =====================================

            if estado == "APPROVED":

                # =====================================
                # DETECTAR PLAN
                # =====================================

                plan = "FREE"

                if monto == 2990000:
                    plan = "BASICO"

                elif monto == 5990000:
                    plan = "PREMIUM"

                elif monto == 9990000:
                    plan = "GOLD"

                # =====================================
                # GUARDAR SUSCRIPCIÓN
                # =====================================

                cursor.execute("""

                INSERT INTO suscripciones (

                    email,
                    referencia,
                    transaccion_id,
                    plan,
                    estado,
                    monto

                )

                VALUES (%s,%s,%s,%s,%s,%s)

                """, (

                    email,
                    referencia,
                    transaccion["id"],
                    plan,
                    estado,
                    monto

                ))

                conn.commit()

                # =====================================
                # ACTUALIZAR USUARIO
                # =====================================

                cursor.execute("""

                UPDATE clientes

                SET

                    plan = %s,
                    estado_pago = 'ACTIVO',
                    fecha_pago = NOW()

                WHERE email = %s

                """, (

                    plan,
                    email

                ))

                conn.commit()

                print("PLAN ACTUALIZADO")

        return JSONResponse({
            "status": "ok"
        })

    except Exception as e:

        print("ERROR WEBHOOK:", e)

        return JSONResponse({
            "error": str(e)
        })