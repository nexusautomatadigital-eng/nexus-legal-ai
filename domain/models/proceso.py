from dataclasses import dataclass

from domain.models.health import Health

from domain.models.actividad import Actividad


@dataclass
class Proceso:

    id: str

    numero: str

    cliente: str

    plan: str

    health: Health

    actividad: Actividad