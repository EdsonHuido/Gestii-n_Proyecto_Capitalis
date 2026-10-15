from datetime import timedelta

from excepciones import DatoInvalidoError


class Actividad:
    def __init__(self, codigo, nombre, etapa, fecha_inicio, fecha_fin,
                 peso, avance=0, estado="Pendiente", responsable=None):
        if fecha_fin < fecha_inicio:
            raise DatoInvalidoError("La fecha final de la actividad no puede ser anterior a la inicial.")
        if peso <= 0 or peso > 100:
            raise DatoInvalidoError("El peso de la actividad debe ser mayor que 0 y menor o igual a 100.")
        if avance < 0 or avance > 100:
            raise DatoInvalidoError("El avance debe estar entre 0 y 100.")

        self.__codigo = codigo
        self.__nombre = nombre
        self.__etapa = etapa
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        self.__peso = peso
        self.__avance = avance
        self.__estado = estado
        self.__responsable = responsable
        self.__registros_horas = []

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def etapa(self):
        return self.__etapa

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio

    @property
    def fecha_fin(self):
        return self.__fecha_fin

    @property
    def peso(self):
        return self.__peso

    @property
    def avance(self):
        return self.__avance

    @property
    def estado(self):
        return self.__estado

    @property
    def responsable(self):
        return self.__responsable

    @property
    def registros_horas(self):
        return self.__registros_horas

    def actualizar_plan(self, nombre, etapa, inicio, fin, peso, responsable):
        if not nombre.strip() or fin < inicio or not 0 < peso <= 100:
            raise DatoInvalidoError("Revise nombre, fechas y peso entre 0 y 100.")
        for registro in self.__registros_horas:
            if not inicio <= registro.fecha <= fin:
                raise DatoInvalidoError("Hay horas registradas fuera de las nuevas fechas.")
        self.__nombre, self.__etapa = nombre.strip(), etapa.strip()
        self.__fecha_inicio, self.__fecha_fin = inicio, fin
        self.__peso, self.__responsable = peso, responsable

    def actualizar_avance(self, porcentaje):
        if porcentaje < 0 or porcentaje > 100:
            raise DatoInvalidoError("El avance debe estar entre 0 y 100.")
        self.__avance = porcentaje
        self.__estado = "Completada" if porcentaje == 100 else "En progreso"

    def esta_vencida(self, fecha_evaluacion):
        return fecha_evaluacion > self.__fecha_fin and self.__avance < 100

    def calcular_avance_planificado(self, fecha_evaluacion):
        if fecha_evaluacion < self.__fecha_inicio:
            return 0.0
        if fecha_evaluacion >= self.__fecha_fin:
            return 100.0
        if self.__fecha_inicio == self.__fecha_fin:
            return 100.0

        dias_totales = (self.__fecha_fin - self.__fecha_inicio).days
        dias_transcurridos = (fecha_evaluacion - self.__fecha_inicio).days
        return (dias_transcurridos / dias_totales) * 100

    def agregar_registro_horas(self, registro):
        from registro_horas import RegistroHoras

        if not isinstance(registro, RegistroHoras):
            raise DatoInvalidoError("Se esperaba un objeto RegistroHoras.")
        if registro.actividad is not self:
            raise DatoInvalidoError("El registro no corresponde a esta actividad.")
        self.__registros_horas.append(registro)

    def calcular_horas_reales(self):
        total = 0
        for registro in self.__registros_horas:
            total += registro.cantidad_horas
        return total

    def __str__(self):
        return (f"{self.__codigo} - {self.__nombre} | {self.__etapa} | "
                f"peso {self.__peso:.1f}% | avance {self.__avance:.1f}%")
