from excepciones import DatoInvalidoError


class Entregable:
    def __init__(self, codigo, nombre, fecha_entrega, peso=0,
                 obligatorio=True, estado="Pendiente", responsable=None):
        if peso < 0 or peso > 100:
            raise DatoInvalidoError("El peso del entregable debe estar entre 0 y 100.")

        self.__codigo = codigo
        self.__nombre = nombre
        self.__fecha_entrega = fecha_entrega
        self.__peso = peso
        self.__obligatorio = bool(obligatorio)
        self.__estado = estado
        self.__responsable = responsable

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def fecha_entrega(self):
        return self.__fecha_entrega

    @property
    def peso(self):
        return self.__peso

    @property
    def obligatorio(self):
        return self.__obligatorio

    @property
    def estado(self):
        return self.__estado

    @property
    def responsable(self):
        return self.__responsable

    def actualizar_plan(self, nombre, fecha, peso, obligatorio, responsable):
        if not nombre.strip() or not 0 <= peso <= 100:
            raise DatoInvalidoError("Nombre obligatorio y peso entre 0 y 100.")
        self.__nombre, self.__fecha_entrega = nombre.strip(), fecha
        self.__peso, self.__obligatorio = peso, obligatorio
        self.__responsable = responsable

    def marcar_completado(self):
        self.__estado = "Completado"

    def esta_vencido(self, fecha_evaluacion):
        return fecha_evaluacion > self.__fecha_entrega and not self.esta_completado()

    def esta_completado(self):
        return self.__estado.lower() == "completado"

    def __str__(self):
        requerido = "Obligatorio" if self.__obligatorio else "Opcional"
        return f"{self.__codigo} - {self.__nombre} | {requerido} | {self.__estado}"
