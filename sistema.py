from cliente import Cliente
from consultor import Consultor
from excepciones import DatoInvalidoError
from marco_referencia import MarcoReferencia
from proyecto import Proyecto


class SistemaCapitalis:
    def __init__(self):
        self.__clientes = []
        self.__consultores = []
        self.__marcos_referencia = []
        self.__proyectos = []

    @property
    def clientes(self):
        return self.__clientes

    @property
    def consultores(self):
        return self.__consultores

    @property
    def marcos_referencia(self):
        return self.__marcos_referencia

    @property
    def proyectos(self):
        return self.__proyectos

    def _validar_codigo_unico(self, lista, codigo, nombre_objeto):
        for objeto in lista:
            if objeto.codigo.lower() == codigo.lower():
                raise DatoInvalidoError(
                    f"Ya existe un {nombre_objeto} con el código {codigo}."
                )

    def agregar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Se esperaba un objeto Cliente.")
        self._validar_codigo_unico(self.__clientes, cliente.codigo, "cliente")
        self.__clientes.append(cliente)

    def agregar_consultor(self, consultor):
        if not isinstance(consultor, Consultor):
            raise DatoInvalidoError("Se esperaba un objeto Consultor.")
        self._validar_codigo_unico(self.__consultores, consultor.codigo, "consultor")
        self.__consultores.append(consultor)

    def agregar_marco(self, marco):
        if not isinstance(marco, MarcoReferencia):
            raise DatoInvalidoError("Se esperaba un objeto MarcoReferencia.")
        self._validar_codigo_unico(self.__marcos_referencia, marco.codigo, "marco")
        self.__marcos_referencia.append(marco)

    def agregar_proyecto(self, proyecto):
        if not isinstance(proyecto, Proyecto):
            raise DatoInvalidoError("Se esperaba un objeto Proyecto.")
        self._validar_codigo_unico(self.__proyectos, proyecto.codigo, "proyecto")
        self.__proyectos.append(proyecto)

    def buscar_cliente(self, codigo):
        for cliente in self.__clientes:
            if cliente.codigo.lower() == codigo.lower():
                return cliente
        return None

    def buscar_consultor(self, codigo):
        for consultor in self.__consultores:
            if consultor.codigo.lower() == codigo.lower():
                return consultor
        return None

    def buscar_marco(self, codigo):
        for marco in self.__marcos_referencia:
            if marco.codigo.lower() == codigo.lower():
                return marco
        return None

    def buscar_proyecto(self, codigo):
        for proyecto in self.__proyectos:
            if proyecto.codigo.lower() == codigo.lower():
                return proyecto
        return None

    def filtrar_proyectos(self, cliente="", pais="", tipo="", marco="", estado=""):
        resultados = []
        for proyecto in self.__proyectos:
            cumple = True

            if cliente and (cliente.lower() not in proyecto.cliente.razon_social.lower()
                            and cliente.lower() not in proyecto.cliente.codigo.lower()):
                cumple = False
            if pais and pais.lower() not in proyecto.pais_ejecucion.lower():
                cumple = False
            if tipo and tipo.lower() not in proyecto.tipo_proyecto.lower():
                cumple = False
            if estado and estado.lower() not in proyecto.estado.lower():
                cumple = False
            if marco:
                tiene_marco = any(
                    marco.lower() in m.codigo.lower() or marco.lower() in m.identificacion.lower()
                    for m in proyecto.marcos_referencia
                )
                if not tiene_marco:
                    cumple = False

            if cumple:
                resultados.append(proyecto)
        return resultados

    def calcular_planificacion_todos(self):
        """
        Demuestra polimorfismo: la lista contiene objetos de subclases distintas,
        pero todos responden al mismo método calcular_horas_planificadas().
        """
        resultados = []
        for proyecto in self.__proyectos:
            resultados.append({
                "codigo": proyecto.codigo,
                "tipo": proyecto.tipo_proyecto,
                "horas": proyecto.calcular_horas_planificadas()
            })
        return resultados
