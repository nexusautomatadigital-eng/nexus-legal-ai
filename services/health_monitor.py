from services.db import get_connection


def actualizar_estado_fuente(
    fuente,
    estado,
    mensaje
):

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""

            update estado_fuentes

            set

                estado = %s,
                mensaje = %s,
                ultima_revision = now()

            where fuente = %s

        """, (

            estado,
            mensaje,
            fuente

        ))

        conn.commit()

        print(
            f"✅ FUENTE ACTUALIZADA: {fuente}"
        )

    except Exception as e:

        conn.rollback()

        print(
            f"❌ ERROR ESTADO FUENTE: {e}"
        )

    finally:

        cur.close()
        conn.close()