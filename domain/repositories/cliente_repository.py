from domain.repositories.base_repository import BaseRepository
from domain.models.cliente import Cliente


class ClienteRepository(BaseRepository):

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

        row = cursor.fetchone()

        cursor.close()

        if row is None:
            return None

        return Cliente(
            id=row[0],
            nombre=row[1],
            email=row[2],
            plan=row[3]
        )


