from excepciones import CierreProyectoError, DatoInvalidoError
from matrices import (MATRICES_AUDITORIA, PORCENTAJE_EJECUCION_AUDITORIA,
                      convertir_matriz_a_horas)
from proyecto import Proyecto


class ProyectoAuditoria(Proyecto):
    def __init__(self, codigo, nombre, cliente, pais_ejecucion, complejidad,
                 fecha_inicio, fecha_fin, precio_contratado, tipo_auditoria,
                 dias_auditor, alcance, criterios, moneda="USD"):
        if dias_auditor <= 0:
            raise DatoInvalidoError("Los días auditor deben ser mayores que cero.")

        super().__init__(codigo, nombre, cliente, pais_ejecucion, complejidad,
                         fecha_inicio, fecha_fin, precio_contratado, moneda)
        self.__tipo_auditoria = tipo_auditoria
        self.__dias_auditor = dias_auditor
        self.__alcance = alcance
        self.__criterios = criterios

    @property
    def tipo_auditoria(self):
        return self.__tipo_auditoria

    @property
    def dias_auditor(self):
        return self.__dias_auditor

    @property
    def alcance(self):
        return self.__alcance

    @property
    def criterios(self):
        return self.__criterios

    def calcular_horas_ejecucion(self):
        return self.__dias_auditor * 8

    def calcular_horas_planificadas(self):
        porcentaje_ejecucion = PORCENTAJE_EJECUCION_AUDITORIA[self.complejidad]
        return self.calcular_horas_ejecucion() / porcentaje_ejecucion

    def calcular_distribucion_horas(self):
        matriz = MATRICES_AUDITORIA[self.complejidad]
        return convertir_matriz_a_horas(self.calcular_horas_planificadas(), matriz)

    def validar_cierre(self):
        self._validar_cierre_general()

        actividades_ejecucion = [
            a for a in self.actividades if "ejec" in a.etapa.lower() or "ejec" in a.nombre.lower()
        ]
        if not actividades_ejecucion or any(a.avance < 100 for a in actividades_ejecucion):
            raise CierreProyectoError(
                "La auditoría requiere completar la actividad de ejecución."
            )

        informes = [
            e for e in self.entregables
            if e.obligatorio and "informe" in e.nombre.lower()
        ]
        if not informes or any(not e.esta_completado() for e in informes):
            raise CierreProyectoError(
                "El informe de auditoría debe figurar como entregable obligatorio completado."
            )
        return True
