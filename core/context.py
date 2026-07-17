from dataclasses import dataclass


@dataclass
class UserContext:

    cliente_id: int | None = None

    nombre: str | None = None

    usuario: str | None = None

    email: str | None = None

    whatsapp: str | None = None

    plan: str | None = None

    logueado: bool = False