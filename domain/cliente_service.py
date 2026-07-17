from services.db import get_connection


class ProcesoService:

    def __init__(self):

        self.conn = get_connection()

    def get_clientes(self):

        cursor = self.conn.cursor()

        cursor.execute("""

            SELECT

                c.id,

                c.nombre,

                c.plan,

                COUNT(DISTINCT p.id) procesos,

                COUNT(DISTINCT pub.id) publicaciones

            FROM clientes c

            LEFT JOIN procesos_v2 p

                ON p.cliente_id = c.id

            LEFT JOIN publicaciones_v2 pub

                ON pub.proceso_id = p.id

            GROUP BY

                c.id,

                c.nombre,

                c.plan

            ORDER BY c.nombre

        """)

        rows = cursor.fetchall()

        cursor.close()

        clientes = []

        for row in rows:

            clientes.append({

                "id": row[0],

                "nombre": row[1],

                "plan": row[2],

                "procesos": row[3],

                "publicaciones": row[4]

            })

        return clientes