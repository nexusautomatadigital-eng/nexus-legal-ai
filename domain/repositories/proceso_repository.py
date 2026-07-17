from domain.repositories.base_repository import BaseRepository


class ProcesoRepository(BaseRepository):

    def __init__(self):
        super().__init__()

    def get_by_cliente(self, cliente_id):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT

                p.id,
                p.numero_proceso,
                c.nombre,
                c.plan,

                COUNT(DISTINCT pub.id) AS publicaciones,
                COUNT(DISTINCT act.id) AS actuaciones,
                COUNT(DISTINCT doc.id) AS documentos

            FROM procesos_v2 p

            INNER JOIN clientes c
                ON c.id = p.cliente_id

            LEFT JOIN publicaciones_v2 pub
                ON pub.proceso_id = p.id

            LEFT JOIN actuaciones_v2 act
                ON act.publicacion_id = pub.id

            LEFT JOIN documentos_v2 doc
                ON doc.publicacion_id = pub.id

            WHERE c.id = %s

            GROUP BY
                p.id,
                p.numero_proceso,
                c.nombre,
                c.plan
            """,
            (cliente_id,)
        )

        rows = cursor.fetchall()

        cursor.close()

        return rows