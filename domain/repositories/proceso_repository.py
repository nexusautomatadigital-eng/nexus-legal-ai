from domain.repositories.base_repository import BaseRepository
from domain.models.proceso import Proceso


class ProcesoRepository(BaseRepository):

    def __init__(self):
        super().__init__()

    def get_by_cliente(self, cliente_id):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                cliente_id,
                numero_proceso,
                despacho,
                especialidad,
                demandante,
                demandado,
                estado_proceso,
                ultima_actuacion,
                fecha_ultima_actuacion,
                ultima_revision,
                fuente,
                jurisdiccion,
                activo
            FROM procesos_v2
            WHERE cliente_id = %s
            ORDER BY created_at DESC
            """,
            (cliente_id,)
        )

        rows = cursor.fetchall()

        cursor.close()

        procesos = []

        for row in rows:

            procesos.append(

                Proceso(

                    id=row[0],
                    cliente_id=row[1],
                    numero_proceso=row[2],
                    despacho=row[3],
                    especialidad=row[4],
                    demandante=row[5],
                    demandado=row[6],
                    estado_proceso=row[7],
                    ultima_actuacion=row[8],
                    fecha_ultima_actuacion=row[9],
                    ultima_revision=row[10],
                    fuente=row[11],
                    jurisdiccion=row[12],
                    activo=row[13]

                )

            )

        return procesos