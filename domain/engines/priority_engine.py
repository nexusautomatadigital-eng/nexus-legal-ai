from domain.models.prioridad import Prioridad


class PriorityEngine:

    def calculate(self, proceso):

        score = 0

        # Impacto inicial
        impacto = "Bajo"

        evento = "Sin novedades"

        accion = "Continuar monitoreo."

        # Regla 1
        if proceso.actividad.publicaciones > 0:

            score = 40

            impacto = "Alto"

            evento = "Nueva publicación judicial"

            accion = "Revisar publicación inmediatamente."

        # Regla 2
        elif proceso.actividad.actuaciones > 0:

            score = 25

            impacto = "Medio"

            evento = "Nueva actuación"

            accion = "Revisar actuación."

        # Regla 3
        elif proceso.actividad.documentos > 0:

            score = 10

            impacto = "Bajo"

            evento = "Nuevo documento"

            accion = "Validar documento."

            

        return Prioridad(

            proceso_id=proceso.id,

            numero_proceso=proceso.numero,

            cliente=proceso.cliente,

            evento=evento,

            impacto=impacto,

            accion=accion,

            fecha="Hoy",

            fuente="Nexus Engine",

            score=score

        )