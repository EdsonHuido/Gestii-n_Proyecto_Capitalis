import calendar
from datetime import date

from excepciones import DatoInvalidoError, ConsultorInactivoError, DisponibilidadInsuficienteError
from marco_referencia import MarcoReferencia


class Consultor:
    NIVELES_VALIDOS = ("Jr", "Sr", "Owner")

    def __init__(self, codigo, nombre, nivel_experiencia, costo_hora,
                 horas_mensuales, fecha_ingreso, fecha_cese=None):
        if nivel_experiencia not in self.NIVELES_VALIDOS:
            raise DatoInvalidoError("El nivel debe ser Jr, Sr u Owner.")
        if costo_hora < 0:
            raise DatoInvalidoError("El costo por hora no puede ser negativo.")
        if horas_mensuales <= 0:
            raise DatoInvalidoError("Las horas mensuales deben ser mayores que cero.")
        if fecha_cese is not None and fecha_cese < fecha_ingreso:
            raise DatoInvalidoError("La fecha de cese no puede ser anterior a la fecha de ingreso.")

        self.__codigo = codigo
        self.__nombre = nombre
        self.__especialidades = []
        self.__nivel_experiencia = nivel_experiencia
        self.__costo_hora = costo_hora
        self.__horas_mensuales = horas_mensuales
        self.__fecha_ingreso = fecha_ingreso
        self.__fecha_cese = fecha_cese

        # Lista de relación. Permite calcular la carga del consultor en todos sus proyectos.
        self.__asignaciones = []

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def especialidades(self):
        return self.__especialidades

    @property
    def nivel_experiencia(self):
        return self.__nivel_experiencia

    @property
    def costo_hora(self):
        return self.__costo_hora

    @property
    def horas_mensuales(self):
        return self.__horas_mensuales

    @property
    def fecha_ingreso(self):
        return self.__fecha_ingreso

    @property
    def fecha_cese(self):
        return self.__fecha_cese

    @property
    def asignaciones(self):
        return self.__asignaciones

    def actualizar_nivel(self, nivel):
        if nivel not in self.NIVELES_VALIDOS:
            raise DatoInvalidoError("El nivel debe ser Jr, Sr u Owner.")
        self.__nivel_experiencia = nivel

    def actualizar_costo(self, costo):
        if costo < 0:
            raise DatoInvalidoError("El costo por hora no puede ser negativo.")
        self.__costo_hora = costo

    def actualizar_capacidad(self, horas):
        if horas <= 0:
            raise DatoInvalidoError("La capacidad debe ser mayor que cero.")
        for asignacion in self.__asignaciones:
            if self.calcular_horas_asignadas(asignacion.mes, asignacion.anio) > horas * 0.9 + 1e-9:
                raise DatoInvalidoError("La nueva capacidad dejaría asignaciones por encima del 90 %.")
        self.__horas_mensuales = horas

    def actualizar_fecha_cese(self, fecha):
        if fecha is not None and fecha < self.__fecha_ingreso:
            raise DatoInvalidoError("El cese no puede ser anterior al ingreso.")
        for asignacion in self.__asignaciones:
            ultimo = date(asignacion.anio, asignacion.mes, calendar.monthrange(asignacion.anio, asignacion.mes)[1])
            if fecha is not None and fecha < ultimo:
                raise DatoInvalidoError("El cese afecta una asignación vigente. Modifíquela primero.")
        self.__fecha_cese = fecha

    def quitar_especialidad(self, marco):
        for asignacion in self.__asignaciones:
            if marco in asignacion.proyecto.marcos_referencia:
                raise DatoInvalidoError("El marco es necesario para una asignación existente.")
        if marco in self.__especialidades:
            self.__especialidades.remove(marco)

    def agregar_especialidad(self, marco):
        if not isinstance(marco, MarcoReferencia):
            raise DatoInvalidoError("La especialidad debe ser un objeto MarcoReferencia.")
        if marco not in self.__especialidades:
            self.__especialidades.append(marco)

    def conoce_marco(self, marco):
        return marco in self.__especialidades

    def calcular_limite_mensual(self):
        return self.__horas_mensuales * 0.90

    def calcular_horas_asignadas(self, mes, anio):
        total = 0
        for asignacion in self.__asignaciones:
            if asignacion.mes == mes and asignacion.anio == anio:
                total += asignacion.horas_planificadas
        return total

    def calcular_horas_disponibles(self, mes, anio):
        return self.calcular_limite_mensual() - self.calcular_horas_asignadas(mes, anio)

    def esta_activo_en_mes(self, mes, anio):
        primer_dia = date(anio, mes, 1)
        ultimo_dia = date(anio, mes, calendar.monthrange(anio, mes)[1])

        ingreso_valido = self.__fecha_ingreso <= primer_dia
        cese_valido = self.__fecha_cese is None or self.__fecha_cese >= ultimo_dia
        return ingreso_valido and cese_valido

    def validar_disponibilidad(self, mes, anio, horas_nuevas):
        if horas_nuevas <= 0:
            raise DatoInvalidoError("Las horas a asignar deben ser mayores que cero.")
        if not self.esta_activo_en_mes(mes, anio):
            raise ConsultorInactivoError(
                f"{self.__nombre} no se encuentra activo durante todo {mes:02d}/{anio}."
            )

        disponible = self.calcular_horas_disponibles(mes, anio)
        if horas_nuevas > disponible + 1e-9:
            raise DisponibilidadInsuficienteError(
                f"La asignación supera el límite mensual del 90 %. "
                f"Disponible: {disponible:.2f} h; solicitado: {horas_nuevas:.2f} h."
            )
        return True

    def registrar_asignacion(self, asignacion):
        if asignacion not in self.__asignaciones:
            self.__asignaciones.append(asignacion)

    def __str__(self):
        return (f"{self.__codigo} - {self.__nombre} | {self.__nivel_experiencia} | "
                f"{self.__horas_mensuales:.0f} h/mes")
