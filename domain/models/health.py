from dataclasses import dataclass


@dataclass
class Health:

    score: int

    estado: str

    color: str

    prioridad: str

    riesgo: str

    recomendacion: str
    
    porcentaje: int