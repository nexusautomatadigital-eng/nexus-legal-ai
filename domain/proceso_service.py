from domain.repositories.proceso_repository import ProcesoRepository
import pandas as pd


class ProcesoService:

    def __init__(self):

        self.repository = ProcesoRepository()

    def get_procesos(self, cliente_id):

        print(f"[DEBUG] cliente_id={cliente_id}")
        procesos = self.repository.get_by_cliente(cliente_id)

        print(f"[DEBUG] tipo={type(procesos)}")
        print(f"[DEBUG] cantidad={len(procesos) if procesos is not None else 'None'}")

        return procesos

    def get_procesos_dataframe(self, cliente_id):

        try:

            print("[DEBUG] Entrando a get_procesos_dataframe")

            procesos = self.get_procesos(cliente_id)

            print("TIPO:", type(procesos))
            print("VALOR:", procesos)

            data = []

            for proceso in procesos:

                print("PROCESO:", proceso)

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
        
        except Exception as e:

            print("ERROR REAL:", repr(e))
            raise