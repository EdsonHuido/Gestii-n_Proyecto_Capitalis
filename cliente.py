from excepciones import DatoInvalidoError


class Cliente:
    def __init__(self, codigo, razon_social, pais, contacto):
        if not codigo or not razon_social:
            raise DatoInvalidoError("El código y la razón social del cliente son obligatorios.")

        if pais not in ("Perú", "Ecuador", "Colombia", "Internacional"):
            raise DatoInvalidoError("País inválido. Use Perú, Ecuador, Colombia o Internacional.")
        self.__codigo = codigo
        self.__razon_social = razon_social
        self.__pais = pais
        self.__contacto = contacto

    @property
    def codigo(self):
        return self.__codigo

    @property
    def razon_social(self):
        return self.__razon_social

    @property
    def pais(self):
        return self.__pais

    @property
    def contacto(self):
        return self.__contacto

    def actualizar_datos(self, razon_social, contacto):
        if not razon_social.strip():
            raise DatoInvalidoError("La razón social no puede quedar vacía.")
        self.__razon_social = razon_social.strip()
        self.__contacto = contacto.strip()

    def actualizar_pais(self, pais):
        if pais not in ("Perú", "Ecuador", "Colombia", "Internacional"):
            raise DatoInvalidoError("Seleccione uno de los cuatro países disponibles.")
        self.__pais = pais

    def __str__(self):
        return f"{self.__codigo} - {self.__razon_social} ({self.__pais})"
