from domain.models.health import Health

class HealthEngine:

    def calculate(
        self,
        publicaciones,
        actuaciones,
        documentos,
        alertas=0
    ):

        score = 100

        score -= publicaciones * 4

        score -= actuaciones * 8

        score -= documentos * 2

        score -= alertas * 25

        score = max(0, score)

        estado, color = self._get_status(score)

        prioridad = self._get_priority(score)

        riesgo = self._get_risk(score)

        recomendacion = self._get_recommendation(score)       
        

        return Health(

            score=score,

            porcentaje=score,

            estado=estado,

            color=color,

            prioridad=prioridad,

            riesgo=riesgo,            

            recomendacion=recomendacion

        )
    
    def _get_priority(self, score):

        if score >= 90:
            return "Baja"

        elif score >= 70:
             return "Media"

        return "Alta"
    
    def _get_risk(self, score):

        if score >= 90:
            return "Bajo"

        elif score >= 70:
            return "Medio"

        elif score >= 40:
            return "Alto"

        return "Crítico"
    
    def _get_status(self, score):

        if score >= 90:
            return "Excelente", "#16A34A"

        elif score >= 70:
            return "Estable", "#22C55E"

        elif score >= 40:
            return "Requiere revisión", "#F59E0B"

        return "Crítico", "#DC2626"
    
    def _get_recommendation(self, score):

        if score >= 90:
            return "No existen acciones pendientes."

        elif score >= 70:
            return "Continuar monitoreo."

        elif score >= 40:
            return "Revisar publicaciones y actuaciones recientes."

        return "Se recomienda revisar este proceso inmediatamente."