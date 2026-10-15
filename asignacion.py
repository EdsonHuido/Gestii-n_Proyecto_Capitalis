from datetime import date

from excepciones import DatoInvalidoError, MarcoNoConocidoError


class Asignacion:
    def __init__(self, codigo, proyecto, consultor, mes, anio, horas_planificadas, rol):
        self.__codigo = codigo
        self.__proyecto = proyecto
        self.__consultor = consultor
        self.__mes = int(mes)
        self.__anio = int(anio)
        self.__horas_planificadas = horas_planificadas
        self.__rol = rol
        self.__costo_hora_pactado = consultor.costo_hora

        self.validar_asignacion()

    @property
    def costo_hora_pactado(self):
        return self.__costo_hora_pactado

    @property
    def codigo(self):
        return self.__codigo

    @property
    def proyecto(self):
        return self.__proyecto

    @property
    def consultor(self):
        return self.__consultor

    @property
    def mes(self):
        return self.__mes

    @property
    def anio(self):
        return self.__anio

    @property
    def horas_planificadas(self):
        return self.__horas_planificadas

    @property
    def rol(self):
        return self.__rol

    def actualizar_horas(self, nuevas_horas):
        if nuevas_horas <= 0:
            raise DatoInvalidoError("Las horas deben ser mayores que cero.")
        disponibles = self.__consultor.calcular_horas_disponibles(self.__mes, self.__anio)
        if nuevas_horas > disponibles + self.__horas_planificadas + 1e-9:
            raise DatoInvalidoError(f"Supera el 90 % de capacidad. Máximo para esta asignación: {disponibles + self.__horas_planificadas:.2f} h.")
        reales = self.calcular_horas_reales()
        if nuevas_horas < reales:
            raise DatoInvalidoError(f"Ya existen {reales:.2f} horas reales; no puede planificar menos.")
        self.__horas_planificadas = nuevas_horas

    def actualizar_datos(self, nuevo_proyecto, nuevo_consultor, nuevo_mes, nuevo_anio, nuevas_horas):
        """Valida todo antes de modificar referencias o valores de la asignación."""
        mes, anio = int(nuevo_mes), int(nuevo_anio)
        if not 1 <= mes <= 12 or not 1900 <= anio <= 2200:
            raise DatoInvalidoError("El mes o año está fuera del rango permitido.")
        if nuevas_horas <= 0:
            raise DatoInvalidoError("Las horas planificadas deben ser mayores a cero.")
        if nuevo_proyecto.estado == "Cerrado":
            raise DatoInvalidoError("No se puede trasladar una asignación a un proyecto cerrado.")
        if self.__proyecto.estado == "Cerrado":
            raise DatoInvalidoError("No se pueden modificar asignaciones de proyectos cerrados.")

        # No se altera el responsable ni el periodo cuando ya existen horas reales.
        # Para esos casos se mantiene el historial y se crea una asignación nueva.
        if self.calcular_horas_reales() > 0 and (nuevo_proyecto is not self.__proyecto or
                nuevo_consultor is not self.__consultor or mes != self.__mes or anio != self.__anio):
            raise DatoInvalidoError(
                "La asignación tiene horas reales. Conserve el historial y cree otra "
                "asignación para el nuevo consultor, proyecto o periodo."
            )
        if nuevo_proyecto is self.__proyecto and nuevo_consultor is self.__consultor and mes == self.__mes and anio == self.__anio:
            self.actualizar_horas(nuevas_horas)
            return
        inicio_mes = date(anio, mes, 1)
        if not nuevo_proyecto.fecha_inicio <= inicio_mes <= nuevo_proyecto.fecha_fin:
            raise DatoInvalidoError("El periodo elegido está fuera de las fechas del proyecto destino.")
        for marco in nuevo_proyecto.marcos_referencia:
            if not nuevo_consultor.conoce_marco(marco):
                raise MarcoNoConocidoError(
                    f"{nuevo_consultor.nombre} no conoce {marco.identificacion}."
                )
        for otra in nuevo_proyecto.asignaciones:
            if otra is not self and otra.consultor is nuevo_consultor and otra.mes == mes and otra.anio == anio:
                raise DatoInvalidoError("Ya existe una asignación de este consultor en ese proyecto y mes.")
        # Si es el mismo consultor y el mismo periodo, su asignación actual libera horas.
        liberadas = (self.__horas_planificadas if nuevo_consultor is self.__consultor
                     and mes == self.__mes and anio == self.__anio else 0)
        if not nuevo_consultor.esta_activo_en_mes(mes, anio):
            raise DatoInvalidoError("El consultor no está activo durante todo el mes seleccionado.")
        disponibles = nuevo_consultor.calcular_horas_disponibles(mes, anio) + liberadas
        if nuevas_horas > disponibles + 1e-9:
            raise DatoInvalidoError(
                f"Supera el 90 % de capacidad mensual; máximo permitido: {disponibles:.2f} h."
            )
        # Las comprobaciones terminaron: ahora sí se modifican ambas colecciones.
        if nuevo_proyecto is not self.__proyecto:
            self.__proyecto.asignaciones.remove(self)
            nuevo_proyecto.asignaciones.append(self)
        if nuevo_consultor is not self.__consultor:
            self.__consultor.asignaciones.remove(self)
            nuevo_consultor.registrar_asignacion(self)
        self.__proyecto = nuevo_proyecto
        self.__consultor = nuevo_consultor
        self.__mes = mes
        self.__anio = anio
        self.__horas_planificadas = nuevas_horas
        self.__rol = nuevo_consultor.nivel_experiencia
        self.__costo_hora_pactado = nuevo_consultor.costo_hora

    def validar_asignacion(self):
        if self.__mes < 1 or self.__mes > 12:
            raise DatoInvalidoError("El mes debe estar entre 1 y 12.")
        if self.__horas_planificadas <= 0:
            raise DatoInvalidoError("Las horas planificadas deben ser mayores que cero.")
        if self.__rol not in ("Jr", "Sr", "Owner"):
            raise DatoInvalidoError("El rol de la asignación debe ser Jr, Sr u Owner.")
        if self.__consultor.nivel_experiencia != self.__rol:
            raise DatoInvalidoError(
                f"El consultor es {self.__consultor.nivel_experiencia} y no puede cubrir el rol {self.__rol}."
            )

        # La asignación debe caer dentro de los meses del proyecto.
        primer_dia_mes = date(self.__anio, self.__mes, 1)
        if primer_dia_mes < self.__proyecto.fecha_inicio or primer_dia_mes > self.__proyecto.fecha_fin:
            raise DatoInvalidoError("El mes de la asignación está fuera del periodo del proyecto.")

        # Debe conocer todos los marcos requeridos por el proyecto.
        for marco in self.__proyecto.marcos_referencia:
            if not self.__consultor.conoce_marco(marco):
                raise MarcoNoConocidoError(
                    f"{self.__consultor.nombre} no conoce el marco {marco.identificacion}."
                )

        # Debe estar activo el mes completo y no superar el 90 %.
        self.__consultor.validar_disponibilidad(
            self.__mes, self.__anio, self.__horas_planificadas
        )
        return True

    def calcular_horas_reales(self):
        total = 0
        for actividad in self.__proyecto.actividades:
            for registro in actividad.registros_horas:
                if (registro.consultor is self.__consultor and
                        registro.fecha.month == self.__mes and
                        registro.fecha.year == self.__anio):
                    total += registro.cantidad_horas
        return total

    def __str__(self):
        return (f"{self.__codigo} | {self.__consultor.nombre} | {self.__rol} | "
                f"{self.__mes:02d}/{self.__anio} | {self.__horas_planificadas:.2f} h")
