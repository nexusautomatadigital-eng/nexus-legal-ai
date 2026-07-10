"""
Excepciones personalizadas de Nexus Automata.
"""


class NexusError(Exception):
    """Excepción base de Nexus."""
    pass


class RamaError(NexusError):
    pass


class PublicacionesError(NexusError):
    pass


class SamaiError(NexusError):
    pass


class PersistenciaError(NexusError):
    pass


class DashboardError(NexusError):
    pass