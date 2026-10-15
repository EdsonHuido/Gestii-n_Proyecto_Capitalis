import calendar
from abc import ABC, abstractmethod
from datetime import date

from actividad import Actividad
from asignacion import Asignacion
from entregable import Entregable
from excepciones import CierreProyectoError, DatoInvalidoError, FechaProyectoError
from gasto import Gasto
from marco_referencia import MarcoReferencia


class Proyecto(ABC):
    COMPLEJIDADES_VALIDAS = ("Básico", "Moderado", "Avanzado")
    ESTADOS_VALIDOS = ("Abierto", "Cerrado")

    def __init__(self, codigo, nombre, cliente, pais_ejecucion, complejidad,
                 fecha_inicio, fecha_fin, precio_contratado, moneda="USD",
                 estado="Abierto"):
        if estado not in self.ESTADOS_VALIDOS:
            raise DatoInvalidoError("El estado debe ser Abierto o Cerrado.")
        if complejidad not in self.COMPLEJIDADES_VALIDAS:
            raise DatoInvalidoError("La complejidad debe ser Básico, Moderado o Avanzado.")
        if precio_contratado < 0:
            raise DatoInvalidoError("El precio contratado no puede ser negativo.")

        self.__codigo = codigo
        self.__nombre = nombre
        self.__cliente = cliente
        self.__pais_ejecucion = pais_ejecucion
        self.__complejidad = complejidad
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        self.__precio_contratado = precio_contratado
        self.__moneda = moneda
        self.__estado = estado
        self.__marcos_referencia = []
        self.__asignaciones = []
        self.__actividades = []
        self.__entregables = []
        self.__gastos = []

        self.validar_fechas()

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def cliente(self):
        return self.__cliente

    @property
    def pais_ejecucion(self):
        return self.__pais_ejecucion

    @property
    def complejidad(self):
        return self.__complejidad

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio

    @property
    def fecha_fin(self):
        return self.__fecha_fin

    @property
    def precio_contratado(self):
        return self.__precio_contratado

    @property
    def moneda(self):
        return self.__moneda

    @property
    def estado(self):
        return self.__estado

    @property
    def marcos_referencia(self):
        return self.__marcos_referencia

    @property
    def asignaciones(self):
        return self.__asignaciones

    @property
    def actividades(self):
        return self.__actividades

    @property
    def entregables(self):
        return self.__entregables

    @property
    def gastos(self):
        return self.__gastos

    @property
    def tipo_proyecto(self):
        return self.__class__.__name__.replace("Proyecto", "")

    def actualizar_pais_desde_cliente(self, pais):
        if self.__estado == "Cerrado":
            raise DatoInvalidoError("Un proyecto cerrado no puede cambiar de país.")
        self.__pais_ejecucion = pais

    def actualizar_datos(self, nombre, precio):
        if not nombre.strip() or precio < 0:
            raise DatoInvalidoError("Ingrese un nombre no vacío y un precio no negativo.")
        if self.__estado == "Cerrado":
            raise DatoInvalidoError("No se pueden modificar proyectos cerrados.")
        self.__nombre = nombre.strip()
        self.__precio_contratado = precio

    def actualizar_fechas(self, inicio, fin):
        if self.__estado == "Cerrado":
            raise DatoInvalidoError("No se pueden modificar proyectos cerrados.")
        if fin <= inicio or inicio.day != 1 or fin.day != calendar.monthrange(fin.year, fin.month)[1]:
            raise FechaProyectoError("El inicio debe ser el día 1 y el fin el último día de un mes posterior.")
        for actividad in self.__actividades:
            if actividad.fecha_inicio < inicio or actividad.fecha_fin > fin:
                raise FechaProyectoError(f"La actividad {actividad.codigo} quedaría fuera del proyecto.")
        for entregable in self.__entregables:
            if not inicio <= entregable.fecha_entrega <= fin:
                raise FechaProyectoError(f"El entregable {entregable.codigo} quedaría fuera del proyecto.")
        for asignacion in self.__asignaciones:
            fecha_mes = date(asignacion.anio, asignacion.mes, 1)
            if not inicio <= fecha_mes <= fin:
                raise FechaProyectoError(f"La asignación {asignacion.codigo} quedaría fuera del proyecto.")
        self.__fecha_inicio = inicio
        self.__fecha_fin = fin
        if hasattr(self, '_ProyectoConsultoria__horas_mensuales_cliente'):
            self._ProyectoConsultoria__horas_mensuales_cliente = self.calcular_horas_mensuales()

    def actualizar_actividad(self, actividad, nombre, etapa, inicio, fin, peso, responsable):
        if self.__estado == "Cerrado":
            raise DatoInvalidoError("El proyecto está cerrado.")
        if actividad not in self.__actividades or inicio < self.__fecha_inicio or fin > self.__fecha_fin:
            raise DatoInvalidoError("La actividad debe pertenecer al proyecto y estar dentro de sus fechas.")
        total = sum(a.peso for a in self.__actividades if a is not actividad) + peso
        if total > 100 + 1e-9:
            raise DatoInvalidoError(f"Los pesos sumarían {total:.2f} %, superior a 100 %.")
        actividad.actualizar_plan(nombre, etapa, inicio, fin, peso, responsable)

    def actualizar_entregable(self, entregable, nombre, fecha, peso, obligatorio, responsable):
        if self.__estado == "Cerrado":
            raise DatoInvalidoError("El proyecto está cerrado.")
        if entregable not in self.__entregables or not self.__fecha_inicio <= fecha <= self.__fecha_fin:
            raise DatoInvalidoError("La fecha del entregable debe estar dentro del proyecto.")
        entregable.actualizar_plan(nombre, fecha, peso, obligatorio, responsable)

    def agregar_marco_actualizado(self, marco):
        if self.__estado == "Cerrado":
            raise DatoInvalidoError("El proyecto está cerrado.")
        if marco in self.__marcos_referencia:
            return
        for asignacion in self.__asignaciones:
            if not asignacion.consultor.conoce_marco(marco):
                raise DatoInvalidoError(f"El consultor {asignacion.consultor.codigo} no conoce el marco. Actualice primero su especialidad.")
        self.agregar_marco(marco)

    def validar_fechas(self):
        if self.__fecha_fin <= self.__fecha_inicio:
            raise FechaProyectoError("La fecha de fin debe ser posterior a la fecha de inicio.")
        if self.__fecha_inicio.day != 1:
            raise FechaProyectoError("El proyecto debe iniciar el primer día del mes.")

        ultimo_dia = calendar.monthrange(self.__fecha_fin.year, self.__fecha_fin.month)[1]
        if self.__fecha_fin.day != ultimo_dia:
            raise FechaProyectoError("El proyecto debe finalizar el último día del mes.")
        return True

    def calcular_numero_meses(self):
        return ((self.__fecha_fin.year - self.__fecha_inicio.year) * 12 +
                self.__fecha_fin.month - self.__fecha_inicio.month + 1)

    def agregar_marco(self, marco):
        if not isinstance(marco, MarcoReferencia):
            raise DatoInvalidoError("Se esperaba un objeto MarcoReferencia.")
        if marco not in self.__marcos_referencia:
            self.__marcos_referencia.append(marco)

    def agregar_actividad(self, actividad):
        if not isinstance(actividad, Actividad):
            raise DatoInvalidoError("Se esperaba un objeto Actividad.")
        if actividad.fecha_inicio < self.__fecha_inicio or actividad.fecha_fin > self.__fecha_fin:
            raise DatoInvalidoError("La actividad debe estar dentro de las fechas del proyecto.")

        nuevo_total = actividad.peso
        for existente in self.__actividades:
            nuevo_total += existente.peso
        if nuevo_total > 100:
            raise DatoInvalidoError("La suma de pesos de las actividades no puede superar el 100 %.")
        self.__actividades.append(actividad)

    def agregar_entregable(self, entregable):
        if not isinstance(entregable, Entregable):
            raise DatoInvalidoError("Se esperaba un objeto Entregable.")
        if entregable.fecha_entrega < self.__fecha_inicio or entregable.fecha_entrega > self.__fecha_fin:
            raise DatoInvalidoError("La fecha del entregable debe estar dentro del proyecto.")
        self.__entregables.append(entregable)

    def agregar_gasto(self, gasto):
        if not isinstance(gasto, Gasto):
            raise DatoInvalidoError("Se esperaba un objeto Gasto.")
        self.__gastos.append(gasto)

    def agregar_asignacion(self, asignacion):
        if not isinstance(asignacion, Asignacion):
            raise DatoInvalidoError("Se esperaba un objeto Asignacion.")
        if asignacion.proyecto is not self:
            raise DatoInvalidoError("La asignación no pertenece a este proyecto.")

        # Evita duplicar la misma asignación mensual del consultor en el proyecto.
        for existente in self.__asignaciones:
            if (existente.consultor is asignacion.consultor and
                    existente.mes == asignacion.mes and
                    existente.anio == asignacion.anio):
                raise DatoInvalidoError(
                    "El consultor ya tiene una asignación registrada en ese mes para este proyecto."
                )

        self.__asignaciones.append(asignacion)
        asignacion.consultor.registrar_asignacion(asignacion)

    def eliminar_asignacion(self, asignacion):
        """Retira una asignación sin ejecución, conservando sus relaciones."""
        if self.estado == "Cerrado":
            raise DatoInvalidoError("El proyecto está cerrado y no admite eliminaciones.")
        if asignacion not in self.__asignaciones:
            raise DatoInvalidoError("La asignación no pertenece al proyecto seleccionado.")
        if asignacion.calcular_horas_reales() > 0:
            raise DatoInvalidoError("Hay horas reales del consultor en ese mes. Conserve la asignación histórica.")
        # Si queda otra asignación del mismo consultor en este proyecto,
        # puede seguir figurando como responsable de tareas planificadas.
        otras = any(a is not asignacion and a.consultor is asignacion.consultor
                    for a in self.__asignaciones)
        if not otras:
            if any(a.responsable is asignacion.consultor for a in self.__actividades):
                raise DatoInvalidoError(
                    "El consultor figura como responsable de actividades. Cambie ese responsable primero (menú 9, opción 6).")
            if any(e.responsable is asignacion.consultor for e in self.__entregables):
                raise DatoInvalidoError(
                    "El consultor figura como responsable de entregables. Cambie ese responsable primero (menú 9, opción 7).")
        self.__asignaciones.remove(asignacion)
        asignacion.consultor.asignaciones.remove(asignacion)

    def eliminar_actividad(self, actividad):
        """Elimina actividades sin avance ni registros reales."""
        if self.estado == "Cerrado":
            raise DatoInvalidoError("El proyecto está cerrado y no admite eliminaciones.")
        if actividad not in self.__actividades:
            raise DatoInvalidoError("La actividad no pertenece al proyecto.")
        if actividad.avance > 0 or actividad.registros_horas:
            raise DatoInvalidoError("La actividad tiene avance u horas registradas y debe conservarse.")
        self.__actividades.remove(actividad)

    def eliminar_entregable(self, entregable):
        """Elimina entregables pendientes; completados permanecen como evidencia."""
        if self.estado == "Cerrado":
            raise DatoInvalidoError("El proyecto está cerrado y no admite eliminaciones.")
        if entregable not in self.__entregables:
            raise DatoInvalidoError("El entregable no pertenece al proyecto.")
        if entregable.esta_completado():
            raise DatoInvalidoError("El entregable ya está completado y no puede eliminarse.")
        self.__entregables.remove(entregable)

    def calcular_horas_reales(self):
        total = 0
        for actividad in self.__actividades:
            total += actividad.calcular_horas_reales()
        return total

    def calcular_costo_planificado(self):
        costo_horas = 0
        for asignacion in self.__asignaciones:
            costo_horas += asignacion.horas_planificadas * asignacion.costo_hora_pactado

        gastos_planificados = 0
        for gasto in self.__gastos:
            gastos_planificados += gasto.monto_planificado
        return costo_horas + gastos_planificados

    def calcular_costo_real(self):
        costo_horas = 0
        for actividad in self.__actividades:
            for registro in actividad.registros_horas:
                costo_horas += registro.cantidad_horas * registro.costo_hora_registrado

        gastos_reales = 0
        for gasto in self.__gastos:
            gastos_reales += gasto.monto_real
        return costo_horas + gastos_reales

    def calcular_margen_planificado(self):
        return self.__precio_contratado - self.calcular_costo_planificado()

    def calcular_margen_real(self):
        return self.__precio_contratado - self.calcular_costo_real()

    def calcular_avance_real(self):
        if not self.__actividades:
            return 0.0
        total = 0
        for actividad in self.__actividades:
            total += (actividad.peso * actividad.avance) / 100
        return total

    def calcular_avance_planificado(self, fecha_evaluacion):
        if not self.__actividades:
            return 0.0
        total = 0
        for actividad in self.__actividades:
            total += (actividad.peso * actividad.calcular_avance_planificado(fecha_evaluacion)) / 100
        return total

    def evaluar_retraso(self, fecha_evaluacion):
        avance_real = self.calcular_avance_real()
        avance_planificado = self.calcular_avance_planificado(fecha_evaluacion)

        hay_vencidos = False
        for actividad in self.__actividades:
            if actividad.esta_vencida(fecha_evaluacion):
                hay_vencidos = True
        for entregable in self.__entregables:
            if entregable.esta_vencido(fecha_evaluacion):
                hay_vencidos = True

        if avance_real < avance_planificado or hay_vencidos:
            return "Retrasado"
        if avance_real > avance_planificado:
            return "Adelantado"
        return "En plazo"

    def _validar_cierre_general(self):
        if not self.__actividades:
            raise CierreProyectoError("El proyecto no tiene actividades registradas.")

        suma_pesos = 0
        for actividad in self.__actividades:
            suma_pesos += actividad.peso
        if suma_pesos != 100:
            raise CierreProyectoError(
                f"Los pesos de las actividades deben sumar 100 %. Actualmente suman {suma_pesos:.2f} %."
            )

        pendientes = [a.nombre for a in self.__actividades if a.avance < 100]
        if pendientes:
            raise CierreProyectoError(
                "Existen actividades pendientes: " + ", ".join(pendientes)
            )

        entregables_pendientes = [
            e.nombre for e in self.__entregables
            if e.obligatorio and not e.esta_completado()
        ]
        if entregables_pendientes:
            raise CierreProyectoError(
                "Existen entregables obligatorios pendientes: " +
                ", ".join(entregables_pendientes)
            )
        return True

    def cerrar(self):
        if self.__estado == "Cerrado":
            raise CierreProyectoError("El proyecto ya está cerrado.")
        self.validar_cierre()
        self.__estado = "Cerrado"
        return True

    @abstractmethod
    def calcular_horas_planificadas(self):
        pass

    @abstractmethod
    def calcular_distribucion_horas(self):
        pass

    @abstractmethod
    def validar_cierre(self):
        pass

    def __str__(self):
        return (f"{self.__codigo} - {self.__nombre} | {self.tipo_proyecto} | "
                f"{self.__complejidad} | {self.__estado}")
