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

        df = self.proceso_service.get_procesos_dataframe(cliente_id)

        # Compatibilidad temporal Dashboard V1
        if not df.empty:

            df = df.rename(columns={
                "estado_proceso": "estado",
                "despacho": "juzgado",
                "fecha_ultima_actuacion": "fecha_actuacion",
                "ultima_revision": "fecha_consulta"
            })

            # Compatibilidad temporal
            if "resumen_ia" not in df.columns:
                df["resumen_ia"] = None

            if "fuente_rama" not in df.columns:
                df["fuente_rama"] = True

            if "fuente_publicaciones" not in df.columns:
                df["fuente_publicaciones"] = False

            if "fuente_samai" not in df.columns:
                df["fuente_samai"] = False

            if "pdfs_encontrados" not in df.columns:
                df["pdfs_encontrados"] = 0

        return df
