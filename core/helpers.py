"""
Funciones auxiliares reutilizables de Nexus Automata.
"""

from datetime import datetime


def ahora():

    """
    Devuelve la fecha y hora actual.
    """

    return datetime.now()


def timestamp():

    """
    Devuelve timestamp legible.
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")