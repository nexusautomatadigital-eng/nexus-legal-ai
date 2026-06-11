from services.db import get_connection

print("🚨 NOTIFICACIONES CARGADO")

def obtener_alertas_pendientes():

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""

            select

                id,
                proceso_id,
                fuente,
                titulo,
                mensaje,
                created_at

            from alertas_v2

            where enviada = false

            order by created_at asc

        """)

        return cur.fetchall()

    finally:

        cur.close()
        conn.close()

def marcar_alerta_enviada(alerta_id):

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""

            update alertas_v2

            set enviada = true

            where id = %s

        """, (

            alerta_id,

        ))

        conn.commit()

        print(
            f"✅ ALERTA ENVIADA: {alerta_id}"
        )

    finally:

        cur.close()
        conn.close()

def procesar_alertas():

    alertas = obtener_alertas_pendientes()

    print()

    print(
        f"🚨 ALERTAS PENDIENTES: "
        f"{len(alertas)}"
    )

    for alerta in alertas:

        alerta_id = alerta[0]

        proceso_id = alerta[1]

        fuente = alerta[2]

        titulo = alerta[3]

        mensaje = alerta[4]

        print()

        print("================================")

        print(f"FUENTE: {fuente}")

        print(f"TITULO: {titulo}")

        print(f"MENSAJE: {mensaje}")

        print("================================")

        marcar_alerta_enviada(
            alerta_id
        )