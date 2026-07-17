from services.db import get_connection


class ActionService:

    def __init__(self):

        self.conn = get_connection()

    def get_actions(self):

        cursor = self.conn.cursor()

        cursor.execute("""

            SELECT

                c.nombre,

                p.numero_proceso,

                pub.fecha_publicacion

            FROM publicaciones_v2 pub

            JOIN procesos_v2 p

                ON pub.proceso_id = p.id

            JOIN clientes c

                ON c.id = p.cliente_id

            ORDER BY pub.fecha_publicacion DESC

            LIMIT 5

        """)

        rows = cursor.fetchall()

        cursor.close()

        actions = []

        i = 1

        for row in rows:

            actions.append({

                "id": f"pub_{i}",

                "icon": "📰",

                "titulo": "Revisar publicación",

                "descripcion": "Existe una nueva publicación judicial pendiente de revisión.",

                "cliente": row[0],

                "proceso": row[1]

            })

            i += 1

        return actions