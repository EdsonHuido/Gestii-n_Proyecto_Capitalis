from excepciones import CierreProyectoError, DatoInvalidoError
from matrices import (MATRICES_CAPACITACION, PORCENTAJE_EJECUCION_CAPACITACION,
                      convertir_matriz_a_horas)
from proyecto import Proyecto


class ProyectoCapacitacion(Proyecto):
    def __init__(self, codigo, nombre, cliente, pais_ejecucion, complejidad,
                 fecha_inicio, fecha_fin, precio_contratado, tema, modalidad,
                 participantes, horas_capacitacion, moneda="USD"):
        if participantes <= 0:
            raise DatoInvalidoError("La cantidad de participantes debe ser mayor que cero.")
        if horas_capacitacion <= 0:
            raise DatoInvalidoError("Las horas de capacitación deben ser mayores que cero.")

        super().__init__(codigo, nombre, cliente, pais_ejecucion, complejidad,
                         fecha_inicio, fecha_fin, precio_contratado, moneda)
        self.__tema = tema
        self.__modalidad = modalidad
        self.__participantes = int(participantes)
        self.__horas_capacitacion = horas_capacitacion

    @property
    def tema(self):
        return self.__tema

    @property
    def modalidad(self):
        return self.__modalidad

    @property
    def participantes(self):
        return self.__participantes

    @property
    def horas_capacitacion(self):
        return self.__horas_capacitacion

    def calcular_horas_planificadas(self):
        porcentaje_ejecucion = PORCENTAJE_EJECUCION_CAPACITACION[self.complejidad]
        return self.__horas_capacitacion / porcentaje_ejecucion

    def calcular_distribucion_horas(self):
        matriz = MATRICES_CAPACITACION[self.complejidad]
        return convertir_matriz_a_horas(self.calcular_horas_planificadas(), matriz)

    def validar_cierre(self):
        self._validar_cierre_general()

        actividades_ejecucion = [
            a for a in self.actividades if "ejec" in a.etapa.lower() or "ejec" in a.nombre.lower()
        ]
        if not actividades_ejecucion or any(a.avance < 100 for a in actividades_ejecucion):
            raise CierreProyectoError(
                "La capacitación requiere completar la actividad de ejecución."
            )

        materiales = [
            e for e in self.entregables
            if e.obligatorio and "material" in e.nombre.lower()
        ]
        asistencias = [
            e for e in self.entregables
            if e.obligatorio and "asistencia" in e.nombre.lower()
        ]
        if not materiales or any(not e.esta_completado() for e in materiales):
            raise CierreProyectoError(
                "El material de capacitación debe figurar como entregable obligatorio completado."
            )
        if not asistencias or any(not e.esta_completado() for e in asistencias):
            raise CierreProyectoError(
                "El registro de asistencia debe figurar como entregable obligatorio completado."
            )
        return True
