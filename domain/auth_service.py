import bcrypt

from domain.repositories.cliente_repository import ClienteRepository
from domain.models.cliente import Cliente


class AuthService:

    def __init__(self):

        self.repository = ClienteRepository()

    def login(self, usuario: str, password: str):

        row = self.repository.get_login_data(usuario)

        if row is None:
            return None

        password_guardado = row[2]

        password_correcto = bcrypt.checkpw(
            password.encode(),
            password_guardado.encode()
        )

        if not password_correcto:
            return None

        return Cliente(
            id=row[0],
            usuario=row[1],
            nombre=row[3],
            email=row[4],
            whatsapp=row[5],
            plan=row[6]
        )