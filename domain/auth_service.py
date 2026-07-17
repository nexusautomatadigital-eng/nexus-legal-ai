from domain.repositories.cliente_repository import ClienteRepository


class AuthService:

    def __init__(self):

        self.repository = ClienteRepository()

    def login(self, usuario):

        return self.repository.get_by_usuario(usuario)