from services.db import get_connection

from domain.engines.health_engine import HealthEngine
from domain.repositories.proceso_repository import ProcesoRepository

from domain.models.proceso import Proceso
from domain.models.actividad import Actividad
import pandas as pd


class ProcesoService:

    def __init__(self):

        self.repository = ProcesoRepository()

        self.health_engine = HealthEngine()

    def get_procesos(self, cliente_id):

        rows = self.repository.get_by_cliente(cliente_id)

        procesos = []

        for row in rows:

            actividad = Actividad(

                publicaciones=row[4],

                actuaciones=row[5],

                documentos=row[6],

                alertas=0

            )

            health = self.health_engine.calculate(

                publicaciones=actividad.publicaciones,

                actuaciones=actividad.actuaciones,

                documentos=actividad.documentos,

                alertas=actividad.alertas

            )

            proceso = Proceso(

                id=row[0],

                numero=row[1],

                cliente=row[2],

                plan=row[3],

                health=health,

                actividad=actividad

            )

            procesos.append(proceso)

        return procesos
    
    def get_procesos_dataframe(self, cliente_id):

        procesos = self.get_procesos(cliente_id)

        data = []

        for proceso in procesos:

            data.append({

                "id": proceso.id,
                "numero": proceso.numero,
                "cliente": proceso.cliente

            })

        return pd.DataFrame(data)

