from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Proceso:
    id: str

    cliente_id: Optional[int]

    numero_proceso: str

    despacho: Optional[str]

    especialidad: Optional[str]

    demandante: Optional[str]

    demandado: Optional[str]

    estado_proceso: Optional[str]

    ultima_actuacion: Optional[str]

    fecha_ultima_actuacion: Optional[str]

    ultima_revision: Optional[datetime]

    fuente: Optional[str]

    jurisdiccion: Optional[str]

    activo: bool