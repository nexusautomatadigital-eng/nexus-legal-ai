from dataclasses import dataclass


@dataclass
class Prioridad:

    proceso_id: str

    numero_proceso: str

    cliente: str

    evento: str

    impacto: str

    accion: str

    fecha: str

    fuente: str
    
    score: int