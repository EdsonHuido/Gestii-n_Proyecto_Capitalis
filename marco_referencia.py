from excepciones import DatoInvalidoError


class MarcoReferencia:
    def __init__(self, codigo, tipo, identificacion, pais):
        if not codigo or not identificacion:
            raise DatoInvalidoError("El código y la identificación del marco son obligatorios.")

        if pais not in ("Perú", "Ecuador", "Colombia", "Internacional"):
            raise DatoInvalidoError("País inválido. Use Perú, Ecuador, Colombia o Internacional.")
        self.__codigo = codigo
        self.__tipo = tipo
        self.__identificacion = identificacion
        self.__pais = pais

    @property
    def codigo(self):
        return self.__codigo

    @property
    def tipo(self):
        return self.__tipo

    @property
    def identificacion(self):
        return self.__identificacion

    @property
    def pais(self):
        return self.__pais

    def actualizar_datos(self, tipo, identificacion, pais):
        if not identificacion.strip():
            raise DatoInvalidoError("La identificación no puede estar vacía.")
        if pais not in ("Perú", "Ecuador", "Colombia", "Internacional"):
            raise DatoInvalidoError("País no permitido.")
        self.__tipo = tipo
        self.__identificacion = identificacion.strip()
        self.__pais = pais

    def __eq__(self, otro):
        return isinstance(otro, MarcoReferencia) and self.__codigo == otro.codigo

    def __str__(self):
        return f"{self.__codigo} - {self.__identificacion} ({self.__tipo})"
