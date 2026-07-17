from domain.repositories.base_repository import BaseRepository
from domain.models.proceso import Proceso


class ProcesoRepository(BaseRepository):

    def __init__(self):

        super().__init__()

    def get_by_usuario(self, usuario):

        cursor = self.conn.cursor()

        cursor.execute(
            """

            SELECT

                id,

                nombre,

                email,

                plan
                
            FROM clientes
            WHERE usuario = %s
            """,
            (usuario,)

            

        )

        rows = cursor.fetchall()

        cursor.close()

        return rows