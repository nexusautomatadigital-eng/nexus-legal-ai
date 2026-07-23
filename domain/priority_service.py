from domain.proceso_service import ProcesoService
from domain.engines.priority_engine import PriorityEngine


class PriorityService:

    def __init__(self, cliente_id):

        self.cliente_id = cliente_id

        self.proceso_service = ProcesoService()

        self.engine = PriorityEngine()

    def get_prioridades(self):

        procesos = self.proceso_service.get_procesos(
            self.cliente_id
        )

        prioridades = []

        for proceso in procesos:

            prioridad = self.engine.calculate(proceso)

            prioridades.append(prioridad)

        prioridades.sort(
            key=lambda p: p.score,
            reverse=True
        )

        return prioridades[:3]