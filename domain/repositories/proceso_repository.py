from domain.repositories.base_repository import BaseRepository


class ProcesoRepository(BaseRepository):

    def __init__(self):
        super().__init__()

    def get_by_cliente(self, cliente):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                numero_proceso,
                cliente,
                plan,
                estado,
                fecha_consulta
            FROM procesos
            WHERE cliente = %s
            ORDER BY id DESC
            """,
            (cliente,)
        )

        rows = cursor.fetchall()

        cursor.close()

        return rows