"""
Dashboard Service
-----------------
Orquesta la información necesaria para el Dashboard.

Versión inicial:
- Utiliza ProcesoService como fuente de datos.
- En próximos sprints incorporará KPIs, actuaciones,
  documentos, publicaciones y alertas.
"""

from domain.proceso_service import ProcesoService


class DashboardService:

    def __init__(self):
        self.proceso_service = ProcesoService()

    def get_dashboard_dataframe(self, cliente_id):
        """
        Retorna el DataFrame principal del Dashboard.
        """
        return self.proceso_service.get_procesos_dataframe(cliente_id)