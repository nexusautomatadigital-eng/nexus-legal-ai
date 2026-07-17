from services.db import get_connection


class DashboardService:

    def __init__(self):

        self.conn = get_connection()

    # ==========================================
    # METODO PRIVADO
    # ==========================================

    def _scalar(self, sql):

        cursor = self.conn.cursor()

        cursor.execute(sql)

        valor = cursor.fetchone()[0]

        cursor.close()

        return valor

    # ==========================================
    # KPIs
    # ==========================================

    def get_total_procesos(self):

        return self._scalar("""

            SELECT COUNT(*)

            FROM procesos_v2

        """)

    def get_total_clientes(self):

        return self._scalar("""

            SELECT COUNT(*)

            FROM clientes

        """)

    def get_total_publicaciones(self):

        return self._scalar("""

            SELECT COUNT(*)

            FROM publicaciones_v2

        """)
    
    def get_priority(self):

        cursor = self.conn.cursor()

        cursor.execute("""

            SELECT

                c.nombre,
                p.numero_proceso,
                pub.fecha_publicacion,
                pub.fuente

            FROM publicaciones_v2 pub

            JOIN procesos_v2 p

                ON pub.proceso_id = p.id

            JOIN clientes c

                ON p.cliente_id = c.id

            ORDER BY pub.fecha_publicacion DESC

            LIMIT 1

        """)

        row = cursor.fetchone()

        cursor.close()

        if row is None:

            return {

                "cliente": "-",

                "proceso": "-",

                "evento": "Sin novedades",

                "fecha": "-",

                "fuente": "-",

                "accion": "No existen eventos prioritarios."

            }

        return {

            "cliente": row[0],

            "proceso": row[1],

            "evento": "Nueva publicación encontrada",

            "fecha": row[2],

            "fuente": "Publicaciones Judiciales",

            "accion": "Revisar publicación inmediatamente."

        }

    def get_total_actuaciones(self):

        return self._scalar("""

            SELECT COUNT(*)

            FROM actuaciones_v2

        """)

    def get_total_documentos(self):

        return self._scalar("""

            SELECT COUNT(*)

            FROM documentos_v2

        """)

    def get_total_alertas(self):

        return self._scalar("""

            SELECT COUNT(*)

            FROM alertas_v2

        """)

    def get_total_vigilancias(self):

        return self._scalar("""

            SELECT COUNT(*)

            FROM vigilancias_v2

        """)