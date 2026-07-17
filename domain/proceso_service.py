from domain.repositories.proceso_repository import ProcesoRepository
import pandas as pd


class ProcesoService:

    def __init__(self):

        self.repository = ProcesoRepository()

    def get_procesos(self, cliente_id):

        return self.repository.get_by_cliente(cliente_id)

    def get_procesos_dataframe(self, cliente_id):

        procesos = self.get_procesos(cliente_id)

        data = []

        for proceso in procesos:

            data.append({

                "id": proceso.id,
                "cliente_id": proceso.cliente_id,
                "numero_proceso": proceso.numero_proceso,
                "despacho": proceso.despacho,
                "especialidad": proceso.especialidad,
                "demandante": proceso.demandante,
                "demandado": proceso.demandado,
                "estado_proceso": proceso.estado_proceso,
                "ultima_actuacion": proceso.ultima_actuacion,
                "fecha_ultima_actuacion": proceso.fecha_ultima_actuacion,
                "ultima_revision": proceso.ultima_revision,
                "fuente": proceso.fuente,
                "jurisdiccion": proceso.jurisdiccion,
                "activo": proceso.activo

            })

        return pd.DataFrame(data)