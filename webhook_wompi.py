from fastapi import FastAPI, Request
import psycopg2
import os

app = FastAPI()

# ==========================================
# CONEXION SUPABASE
# ==========================================

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

# ==========================================
# WEBHOOK WOMPI
# ==========================================

@app.post("/webhook-wompi")

async def webhook_wompi(request: Request):

    data = await request.json()

    print("📩 WEBHOOK RECIBIDO")

    print(data)

    try:

        evento = data["event"]

        transaccion = data["data"]["transaction"]

        estado = transaccion["status"]

        email_cliente = transaccion["customer_email"]

        monto = transaccion["amount_in_cents"]

        referencia = transaccion["reference"]

        # ==========================================
        # VALIDAR PAGO EXITOSO
        # ==========================================

        if estado == "APPROVED":

            # ==========================================
            # DEFINIR PLAN
            # ==========================================

            plan = "FREE"

            if monto == 2990000:
                plan = "BASICO"

            elif monto == 5990000:
                plan = "PREMIUM"

            elif monto == 9990000:
                plan = "GOLD"

            # ==========================================
            # ACTUALIZAR USUARIO
            # ==========================================

            cursor.execute("""

            UPDATE usuarios

            SET plan = %s

            WHERE email = %s

            """, (

                plan,
                email_cliente

            ))

            conn.commit()

            print("✅ PLAN ACTUALIZADO")

        return {

            "status": "ok"

        }

    except Exception as e:

        print("❌ ERROR WEBHOOK")

        print(e)

        return {

            "status": "error"

        }