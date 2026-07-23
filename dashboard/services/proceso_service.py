from dashboard.repositories.proceso_repository import ProcesoRepository


class ProcesoService:

    def __init__(self):
        self.repository = ProcesoRepository()

    def agregar_proceso(
        self,
        cliente_id,
        numero_proceso,
    ):

        if self.repository.exists(
            cliente_id,
            numero_proceso,
        ):

            return {
                "ok": False,
                "mensaje": "El proceso ya existe."
            }

        proceso_id = self.repository.create(
            cliente_id,
            numero_proceso,
        )

        return {
            "ok": True,
            "proceso_id": proceso_id
        }