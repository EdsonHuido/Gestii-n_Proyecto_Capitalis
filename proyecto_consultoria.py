from excepciones import CierreProyectoError
from matrices import HORAS_CONSULTORIA, MATRICES_CONSULTORIA, convertir_matriz_a_horas
from proyecto import Proyecto


class ProyectoConsultoria(Proyecto):
    def __init__(self, codigo, nombre, cliente, pais_ejecucion, complejidad,
                 fecha_inicio, fecha_fin, precio_contratado, tipo_consultoria,
                 tipo_sistema, modalidad, moneda="USD"):
        super().__init__(codigo, nombre, cliente, pais_ejecucion, complejidad,
                         fecha_inicio, fecha_fin, precio_contratado, moneda)
        self.__tipo_consultoria = tipo_consultoria
        self.__tipo_sistema = tipo_sistema
        self.__modalidad = modalidad
        self.__horas_totales_estandar = HORAS_CONSULTORIA[self.complejidad]
        self.__horas_mensuales_cliente = self.calcular_horas_mensuales()

    @property
    def tipo_consultoria(self):
        return self.__tipo_consultoria

    @property
    def tipo_sistema(self):
        return self.__tipo_sistema

    @property
    def modalidad(self):
        return self.__modalidad

    @property
    def horas_totales_estandar(self):
        return self.__horas_totales_estandar

    @property
    def horas_mensuales_cliente(self):
        return self.__horas_mensuales_cliente

    def calcular_horas_planificadas(self):
        return self.__horas_totales_estandar

    def calcular_horas_mensuales(self):
        return self.calcular_horas_planificadas() / self.calcular_numero_meses()

    def calcular_distribucion_horas(self):
        matriz = MATRICES_CONSULTORIA[self.complejidad]
        return convertir_matriz_a_horas(self.calcular_horas_planificadas(), matriz)

    def calcular_distribucion_mensual(self):
        matriz = MATRICES_CONSULTORIA[self.complejidad]
        return convertir_matriz_a_horas(self.calcular_horas_mensuales(), matriz)

    def validar_cierre(self):
        self._validar_cierre_general()

        # En consultoría se consideran comprometidos los entregables registrados.
        pendientes = [e.nombre for e in self.entregables if not e.esta_completado()]
        if pendientes:
            raise CierreProyectoError(
                "La consultoría tiene entregables comprometidos pendientes: " +
                ", ".join(pendientes)
            )
        return True
