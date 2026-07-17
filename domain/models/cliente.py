from dataclasses import dataclass
from datetime import date


@dataclass
class Cliente:

    id: int

    nombre: str

    email: str

    plan: str