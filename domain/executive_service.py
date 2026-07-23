from services.db import get_connection

from domain.priority_service import PriorityService


class ExecutiveService:

    def __init__(self, cliente_id):

        self.conn = get_connection()

        self.cliente_id = cliente_id

        self.priority_service = PriorityService(cliente_id)

    def get_kpis(self):

        cursor = self.conn.cursor()

        cursor.execute("""

            SELECT

                (SELECT COUNT(*) FROM procesos_v2),

                (SELECT COUNT(*) FROM publicaciones_v2),

                (SELECT COUNT(*) FROM actuaciones_v2),

                (SELECT COUNT(*) FROM documentos_v2),

                (SELECT COUNT(*) FROM alertas_v2)

        """)

        row = cursor.fetchone()

        cursor.close()

        return {

            "procesos": row[0],

            "publicaciones": row[1],

            "actuaciones": row[2],

            "documentos": row[3],

            "alertas": row[4]

        }
    
    def get_summary(self):

        kpis = self.get_kpis()

        return f"""
    Hoy se detectaron:

    • {kpis['publicaciones']} publicaciones.

    • {kpis['procesos']} procesos vigilados.

    • {kpis['actuaciones']} actuaciones.

    • {kpis['documentos']} documentos.

    • {kpis['alertas']} alertas registradas.

    Prioridad del día:

    Revisar las publicaciones encontradas.
    """

    def get_priority(self):

        prioridades = self.priority_service.get_prioridades()

        if prioridades:

            return prioridades[0]
        
        return None

        # Código anterior temporalmente comentado

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
    
    def get_recent_events(self):

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

                ON p.cliente_id = c.id

            ORDER BY pub.fecha_publicacion DESC

            LIMIT 5

        """)

        rows = cursor.fetchall()

        cursor.close()

        events = []

        for row in rows:

            events.append({

                "icon": "📰",

                "titulo": "Nueva publicación",

                "cliente": f"{row[0]}",

                "fecha": f"{row[2]}"

            })

        return events
    
    def get_executive_brief(self):

        kpis = self.get_kpis()

        prioridad = self.get_priority()

        return {

            "greeting": "Buenos días",

            "last_sync": "Hace unos minutos",

            "critical": 1 if prioridad else 0,

            "important": max(kpis["actuaciones"], 0),

            "stable": max(
                kpis["procesos"]
                - kpis["publicaciones"]
                - kpis["actuaciones"],
                0
            ),

            "estimated_time": 12,

            "summary": self.get_summary(),

            "priority": prioridad

        }
