from excepciones import DatoInvalidoError


class Gasto:
    def __init__(self, codigo, tipo, monto_planificado, monto_real=0):
        if monto_planificado < 0 or monto_real < 0:
            raise DatoInvalidoError("Los montos del gasto no pueden ser negativos.")

        self.__codigo = codigo
        self.__tipo = tipo
        self.__monto_planificado = monto_planificado
        self.__monto_real = monto_real

    @property
    def codigo(self):
        return self.__codigo

    @property
    def tipo(self):
        return self.__tipo

    @property
    def monto_planificado(self):
        return self.__monto_planificado

    @property
    def monto_real(self):
        return self.__monto_real

    def actualizar_plan(self, tipo, monto):
        if not tipo.strip() or monto < 0:
            raise DatoInvalidoError("El tipo debe tener texto y el monto no puede ser negativo.")
        self.__tipo, self.__monto_planificado = tipo.strip(), monto

    def registrar_monto_real(self, monto):
        if monto < 0:
            raise DatoInvalidoError("El gasto real no puede ser negativo.")
        self.__monto_real = monto

    def calcular_variacion(self):
        return self.__monto_real - self.__monto_planificado

    def __str__(self):
        return (f"{self.__codigo} - {self.__tipo} | Plan: {self.__monto_planificado:.2f} | "
                f"Real: {self.__monto_real:.2f}")
