from domain.models.actividad import Actividad


class ActivityService:

    def __init__(self):

        pass

    def get_activity(self, proceso_id):

        """
        Devuelve la actividad agregada
        del proceso.
        """

        return Actividad(
            publicaciones=0,
            actuaciones=0,
            documentos=0,
            alertas=0
        )