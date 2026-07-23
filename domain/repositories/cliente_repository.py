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
                usuario,
                nombre,
                email,
                whatsapp,
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
            usuario=row[1],
            nombre=row[2],
            email=row[3],
            whatsapp=row[4],
            plan=row[5]
        )
    
    def get_login_data(self, usuario):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                usuario,
                password,
                nombre,
                email,
                whatsapp,
                plan
            FROM clientes
            WHERE usuario = %s
            """,
            (usuario,)
        )

        row = cursor.fetchone()

        cursor.close()

        return row


