class ReglaDeNegocio(Exception):
    """El caso de uso se negó a cambiar el estado."""


class NoEncontrado(Exception):
    """No hay mesa o reserva con ese identificador."""
