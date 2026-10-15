class ErrorCapitalis(Exception):
    """Excepción base del sistema Capitalis."""
    pass


class DatoInvalidoError(ErrorCapitalis):
    pass


class FechaProyectoError(ErrorCapitalis):
    pass


class ConsultorInactivoError(ErrorCapitalis):
    pass


class DisponibilidadInsuficienteError(ErrorCapitalis):
    pass


class MarcoNoConocidoError(ErrorCapitalis):
    pass


class CierreProyectoError(ErrorCapitalis):
    pass
