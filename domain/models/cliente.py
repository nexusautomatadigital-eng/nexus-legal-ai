from dataclasses import dataclass


@dataclass
class Cliente:

    id: int

    usuario: str

    nombre: str

    email: str

    whatsapp: str

    plan: str