from domain.models.prioridad import Prioridad


class PriorityEngine:

    def calculate(self, proceso):

        """
        Calcula la prioridad de un proceso utilizando únicamente
        la información disponible en el modelo Proceso.
        """

        score = 0
        impacto = "Bajo"
        evento = "Proceso monitoreado"
        accion = "Continuar monitoreo."

        # Regla simple basada en el estado del proceso
        estado = (proceso.estado_proceso or "").lower()

        if "sentencia" in estado:
            score = 90
            impacto = "Alto"
            evento = "Proceso con sentencia"
            accion = "Revisar inmediatamente."

        elif "audiencia" in estado:
            score = 70
            impacto = "Alto"
            evento = "Audiencia programada"
            accion = "Preparar seguimiento."

        elif "traslado" in estado:
            score = 50
            impacto = "Medio"
            evento = "Traslado del proceso"
            accion = "Revisar actuación."

        elif proceso.ultima_actuacion:
            score = 30
            impacto = "Medio"
            evento = "Nueva actuación registrada"
            accion = "Validar la última actuación."

        return Prioridad(
            proceso_id=proceso.id,
            numero_proceso=proceso.numero_proceso,
            cliente=str(proceso.cliente_id),
            evento=evento,
            impacto=impacto,
            accion=accion,
            fecha=str(proceso.fecha_ultima_actuacion)
            if proceso.fecha_ultima_actuacion
            else "-",
            fuente=proceso.fuente or "Nexus Engine",
            score=score
        )