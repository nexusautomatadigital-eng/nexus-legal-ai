from datetime import datetime
from .db_repository import DBRepository


class ProcesoRepository(DBRepository):

    def exists(self, cliente_id, numero_proceso):

        cursor = self.execute(
            """
            SELECT id
            FROM procesos_v2
            WHERE cliente_id = %s
            AND numero_proceso = %s
            LIMIT 1
            """,
            (cliente_id, numero_proceso)
        )

        return cursor.fetchone() is not None
    
    def create(
        self,
        cliente_id,
        numero_proceso,
    ):

        cursor = self.execute(
            """
            INSERT INTO procesos_v2
            (
                cliente_id,
                numero_proceso,
                activo,
                metadata,
                created_at
            )

            VALUES
            (
                %s,
                %s,
                TRUE,
                '{}'::jsonb,
                %s
            )

            RETURNING id
            """,
            (
                cliente_id,
                numero_proceso,
                datetime.utcnow(),
            )
        )

        proceso_id = cursor.fetchone()[0]

        self.commit()

        return proceso_id