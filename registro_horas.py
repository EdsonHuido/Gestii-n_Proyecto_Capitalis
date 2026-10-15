from excepciones import DatoInvalidoError


class RegistroHoras:
    def __init__(self, codigo, actividad, consultor, fecha, cantidad_horas):
        self.__codigo = codigo
        self.__actividad = actividad
        self.__consultor = consultor
        self.__fecha = fecha
        self.__cantidad_horas = cantidad_horas
        self.__costo_hora_registrado = consultor.costo_hora
        self.validar_horas()

    @property
    def costo_hora_registrado(self):
        return self.__costo_hora_registrado

    @property
    def codigo(self):
        return self.__codigo

    @property
    def actividad(self):
        return self.__actividad

    @property
    def consultor(self):
        return self.__consultor

    @property
    def fecha(self):
        return self.__fecha

    @property
    def cantidad_horas(self):
        return self.__cantidad_horas

    def validar_horas(self):
        if self.__cantidad_horas <= 0:
            raise DatoInvalidoError("Las horas reales deben ser mayores que cero.")
        if self.__fecha < self.__actividad.fecha_inicio or self.__fecha > self.__actividad.fecha_fin:
            raise DatoInvalidoError("La fecha del registro debe estar dentro del periodo de la actividad.")
        return True

    def __str__(self):
        return (f"{self.__codigo} | {self.__consultor.nombre} | "
                f"{self.__cantidad_horas:.2f} h | {self.__fecha}")
