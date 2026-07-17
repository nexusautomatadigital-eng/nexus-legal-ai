from dataclasses import dataclass

@dataclass
class Expediente:

    proceso: object

    publicaciones: list

    actuaciones: list

    documentos: list

    health: object

    resumen: str