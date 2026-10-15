from datetime import datetime, date

from actividad import Actividad
from asignacion import Asignacion
from cliente import Cliente
from consultor import Consultor
from entregable import Entregable
from excepciones import ErrorCapitalis, DatoInvalidoError
from gasto import Gasto
from marco_referencia import MarcoReferencia
from proyecto_auditoria import ProyectoAuditoria
from proyecto_capacitacion import ProyectoCapacitacion
from proyecto_consultoria import ProyectoConsultoria
from registro_horas import RegistroHoras
from sistema import SistemaCapitalis


PAISES = ("Perú", "Ecuador", "Colombia", "Internacional")


def error_campo(motivo, solucion):
    print(f"\n[ERROR] {motivo}")
    print(f"[CÓMO CORREGIRLO] {solucion}\n")


def leer_texto(mensaje, ejemplo="", opcional=False):
    while True:
        if ejemplo:
            print(f"  Ejemplo: {ejemplo}")
        valor = input(mensaje).strip()
        if valor or opcional:
            return valor
        error_campo("Este campo es obligatorio.", "Escriba un dato y presione Enter.")


def leer_fecha(mensaje, opcional=False):
    while True:
        valor = input(mensaje + " [dd/mm/aaaa]: ").strip()
        if not valor and opcional:
            return None
        try:
            return datetime.strptime(valor, "%d/%m/%Y").date()
        except ValueError:
            error_campo("La fecha ingresada no es válida.",
                        "Use día/mes/año, por ejemplo 01/11/2026.")


def leer_float(mensaje, minimo=None, maximo=None):
    while True:
        valor = input(mensaje).strip()
        try:
            numero = float(valor)
            if numero != numero or numero in (float("inf"), float("-inf")):
                raise ValueError()
        except ValueError:
            error_campo("Se necesita un número válido.", "Ejemplo: 1500 o 12.5 (use punto decimal).")
            continue
        if minimo is not None and numero < minimo:
            error_campo("El número es demasiado pequeño.", f"Ingrese un valor mayor o igual a {minimo}.")
            continue
        if maximo is not None and numero > maximo:
            error_campo("El número supera el máximo permitido.", f"Ingrese un valor menor o igual a {maximo}.")
            continue
        return numero


def leer_int(mensaje, minimo=None, maximo=None):
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor)
        except ValueError:
            error_campo("Se necesita un número entero.", "Ejemplo: 1, 3 o 2026; no escriba letras ni decimales.")
            continue
        if (minimo is not None and numero < minimo) or (maximo is not None and numero > maximo):
            # Mensaje según los límites que existan.
            if maximo is None:
                solucion = f"Ingrese un valor mayor o igual a {minimo}."
            elif minimo is None:
                solucion = f"Ingrese un valor menor o igual a {maximo}."
            else:
                solucion = f"Ingrese un valor entre {minimo} y {maximo}."
            error_campo("Número fuera del rango disponible.", solucion)
            continue
        return numero


def leer_codigo(mensaje, existentes, ejemplo=""):
    """Pide un código obligatorio que no se repita."""
    usados = [c.lower() for c in existentes]
    while True:
        codigo = leer_texto(mensaje, ejemplo)
        if codigo.lower() not in usados:
            return codigo
        error_campo(f"El código {codigo} ya existe.", "Ingrese un código diferente.")


def elegir(mensaje, opciones):
    print(f"\n{mensaje}")
    for i, opcion in enumerate(opciones, 1):
        print(f"  {i}. {opcion}")
    numero = leer_int("Digite el número de la opción: ", 1, len(opciones))
    return opciones[numero - 1]


def leer_si_no(mensaje):
    while True:
        valor = input(mensaje + " (S/N): ").strip().upper()
        if valor in ("S", "N"):
            return valor == "S"
        error_campo("Respuesta inválida.", "Escriba S para Sí o N para No.")


def seleccionar_objeto(lista, titulo):
    if not lista:
        print(f"\n[ATENCIÓN] No hay {titulo.lower()} registrados.")
        print("Registre primero la información relacionada y vuelva a esta opción.")
        return None
    print(f"\n{titulo}")
    for i, objeto in enumerate(lista, start=1):
        print(f"{i}. {objeto}")
    posicion = leer_int("Seleccione un número de la lista: ", 1, len(lista))
    return lista[posicion - 1]


def leer_marcos(sistema):
    if not sistema.marcos_referencia:
        print("No hay marcos registrados. Puede agregarlos desde el menú 1.")
        return []
    print("\nMarcos disponibles (ejemplo de código: MR01):")
    for marco in sistema.marcos_referencia:
        print(f"  {marco.codigo}: {marco.identificacion} [{marco.pais}]")
    while True:
        codigos = input("Códigos separados por coma (Enter para ninguno): ").strip()
        if not codigos:
            return []
        marcos = []
        inexistentes = []
        for codigo in codigos.split(","):
            marco = sistema.buscar_marco(codigo.strip())
            if marco is None:
                inexistentes.append(codigo.strip())
            elif marco not in marcos:
                marcos.append(marco)
        if not inexistentes:
            return marcos
        error_campo("No se encontraron los códigos: " + ", ".join(inexistentes),
                    "Use únicamente códigos de la lista anterior, por ejemplo MR01,MR02.")


def solicitar_proyecto(sistema, accion):
    if not sistema.proyectos:
        print(f"\n[ATENCIÓN] No puede {accion}: todavía no hay proyectos.")
        print("Primero registre un cliente (menú 1) y cree el proyecto (menú 2).")
        return None
    return seleccionar_objeto(sistema.proyectos, "Proyectos")


def mostrar_distribucion(proyecto):
    distribucion = proyecto.calcular_distribucion_horas()
    print("\nDistribución planificada por etapa y nivel:")
    print(f"{'Etapa':42} {'Jr':>10} {'Sr':>10} {'Owner':>10} {'Total':>10}")
    print("-" * 86)
    for etapa, niveles in distribucion.items():
        jr = niveles.get("Jr", 0)
        sr = niveles.get("Sr", 0)
        owner = niveles.get("Owner", 0)
        total = jr + sr + owner
        print(f"{etapa:42} {jr:10.2f} {sr:10.2f} {owner:10.2f} {total:10.2f}")


def registrar_datos_maestros(sistema):
    while True:
        print("\nDATOS MAESTROS")
        print("1. Registrar cliente")
        print("2. Registrar marco de referencia")
        print("3. Registrar consultor")
        print("4. Volver")
        opcion = leer_int("Opción: ", 1, 4)
        if opcion == 4:
            break
        try:
            if opcion == 1:
                print("\nREGISTRO DE CLIENTE")
                cliente = Cliente(
                    leer_texto("Código del cliente: ", "CLI02"),
                    leer_texto("Razón social: ", "Industrias del Perú S.A.C."),
                    elegir("País del cliente:", PAISES),
                    leer_texto("Contacto (persona o área): ", "Carlos Ramírez")
                )
                sistema.agregar_cliente(cliente)
                print("[OK] Cliente registrado:", cliente)
            elif opcion == 2:
                print("\nREGISTRO DE MARCO DE REFERENCIA")
                marco = MarcoReferencia(
                    leer_texto("Código del marco: ", "MR02"),
                    elegir("Tipo de marco:", ("ISO", "Legal", "Otro")),
                    leer_texto("Identificación o nombre: ", "ISO 45001:2018 o Ley N° 29783"),
                    elegir("Ámbito de aplicación:", PAISES)
                )
                sistema.agregar_marco(marco)
                print("[OK] Marco registrado:", marco)
            elif opcion == 3:
                print("\nREGISTRO DE CONSULTOR")
                fecha_ingreso = leer_fecha("Fecha de ingreso")
                fecha_cese = leer_fecha("Fecha de cese (Enter si sigue activo)", True)
                consultor = Consultor(
                    leer_texto("Código: ", "C04"),
                    leer_texto("Nombre completo: ", "Ana Torres"),
                    elegir("Nivel de experiencia:", ("Jr", "Sr", "Owner")),
                    leer_float("Costo por hora: ", 0),
                    leer_float("Capacidad mensual en horas: ", 0),
                    fecha_ingreso, fecha_cese
                )
                for marco in leer_marcos(sistema):
                    consultor.agregar_especialidad(marco)
                sistema.agregar_consultor(consultor)
                print("[OK] Consultor registrado:", consultor)
        except ErrorCapitalis as error:
            error_campo(str(error), "Revise los datos y vuelva a intentar el registro.")


def registrar_proyecto(sistema):
    if not sistema.clientes:
        print("\n[ATENCIÓN] Primero registre un cliente en el menú 1.")
        return
    cliente = seleccionar_objeto(sistema.clientes, "Clientes")
    tipo = elegir("Tipo de proyecto:", ("Consultoría", "Auditoría", "Capacitación"))
    codigo = leer_texto("Código del proyecto: ", "PRO01")
    nombre = leer_texto("Nombre del proyecto: ", "Implementación ISO 9001")
    pais = cliente.pais
    print(f"País del proyecto: {pais} (se toma del cliente, no se vuelve a ingresar)")
    complejidad = elegir("Complejidad:", ("Básico", "Moderado", "Avanzado"))
    print("El proyecto debe comenzar el día 1 de un mes y terminar el último día de un mes.")
    fecha_inicio = leer_fecha("Fecha de inicio")
    fecha_fin = leer_fecha("Fecha de fin")
    precio = leer_float("Precio contratado (0 o mayor): ", 0)
    moneda = elegir("Moneda del contrato:", ("PEN", "USD"))
    if tipo == "Consultoría":
        proyecto = ProyectoConsultoria(
            codigo, nombre, cliente, pais, complejidad, fecha_inicio, fecha_fin,
            precio, leer_texto("Tipo de consultoría (ej. Implementación): "),
            leer_texto("Tipo de sistema (ej. SGC): "),
            elegir("Modalidad:", ("Presencial", "Virtual", "Híbrida")), moneda
        )
    elif tipo == "Auditoría":
        proyecto = ProyectoAuditoria(
            codigo, nombre, cliente, pais, complejidad, fecha_inicio, fecha_fin,
            precio, leer_texto("Tipo de auditoría (ej. Interna): "),
            leer_float("Días auditor (mayor a 0): ", 0.01),
            leer_texto("Alcance (procesos o sedes): "),
            leer_texto("Criterios (ej. ISO 9001:2015): "), moneda
        )
    else:
        proyecto = ProyectoCapacitacion(
            codigo, nombre, cliente, pais, complejidad, fecha_inicio, fecha_fin,
            precio, leer_texto("Tema: "),
            elegir("Modalidad:", ("Presencial", "Virtual", "Híbrida")),
            leer_int("Número de participantes: ", 1),
            leer_float("Horas efectivas de capacitación: ", 0.01), moneda
        )
    for marco in leer_marcos(sistema):
        if marco.pais not in ("Internacional", pais) and pais != "Internacional":
            raise DatoInvalidoError(f"El marco {marco.codigo} corresponde a {marco.pais}, no a {pais}.")
        proyecto.agregar_marco(marco)
    sistema.agregar_proyecto(proyecto)
    print("[OK] Proyecto registrado:", proyecto)
    print(f"Horas estimadas: {proyecto.calcular_horas_planificadas():.2f} h")


def planificar_proyecto(sistema):
    proyecto = solicitar_proyecto(sistema, "continuar")
    if proyecto is None:
        return

    print(f"\nHoras planificadas del proyecto: {proyecto.calcular_horas_planificadas():.2f} h")
    if isinstance(proyecto, ProyectoConsultoria):
        print(f"Horas mensuales: {proyecto.calcular_horas_mensuales():.2f} h/mes")
    mostrar_distribucion(proyecto)

    if proyecto.estado == "Cerrado":
        error_campo("El proyecto está cerrado.", "Solo se pueden planificar proyectos abiertos.")
        return
    while True:
        print("\nPlanificación")
        print("1. Agregar actividad")
        print("2. Agregar entregable")
        print("3. Agregar gasto planificado")
        print("4. Volver")
        opcion = input("Opción: ")

        if opcion == "1":
            responsable = None
            if sistema.consultores:
                usar = ("S" if leer_si_no("¿Desea seleccionar un responsable?") else "N")
                if usar == "S":
                    responsable = seleccionar_objeto(sistema.consultores, "Consultores")

            actividad = Actividad(
                input("Código: "), input("Nombre: "), input("Etapa: "),
                leer_fecha("Fecha de inicio"), leer_fecha("Fecha de fin"),
                leer_float("Peso en el avance total (% de 0 a 100): ", 0.01, 100), 0, "Pendiente", responsable
            )
            proyecto.agregar_actividad(actividad)
            print("Actividad registrada.")

        elif opcion == "2":
            responsable = None
            if sistema.consultores:
                usar = ("S" if leer_si_no("¿Desea seleccionar un responsable?") else "N")
                if usar == "S":
                    responsable = seleccionar_objeto(sistema.consultores, "Consultores")

            obligatorio = leer_si_no("¿Es un entregable obligatorio?")
            entregable = Entregable(
                input("Código: "), input("Nombre: "), leer_fecha("Fecha de entrega"),
                leer_float("Peso referencial (0 si no aplica): ", 0, 100), obligatorio,
                "Pendiente", responsable
            )
            proyecto.agregar_entregable(entregable)
            print("Entregable registrado.")

        elif opcion == "3":
            gasto = Gasto(
                input("Código: "), input("Tipo: "),
                leer_float("Monto planificado: ", 0)
            )
            proyecto.agregar_gasto(gasto)
            print("Gasto planificado registrado.")

        elif opcion == "4":
            break
        else:
            print("Opción no válida.")


def asignar_consultor(sistema):
    proyecto = solicitar_proyecto(sistema, "asignar consultores")
    if proyecto is None:
        return
    if proyecto.estado == "Cerrado":
        error_campo("El proyecto está cerrado.", "No se pueden agregar asignaciones a proyectos cerrados.")
        return
    consultor = seleccionar_objeto(sistema.consultores, "Consultores")
    if consultor is None:
        return

    print(f"Rol del consultor: {consultor.nivel_experiencia} (automático)")
    asignacion = Asignacion(
        input("Código de asignación: "), proyecto, consultor,
        leer_int("Mes (1-12): ", 1, 12), leer_int("Año (ej. 2026): ", 1900, 2200),
        leer_float("Horas planificadas (mayor a 0): ", 0.01), consultor.nivel_experiencia
    )
    proyecto.agregar_asignacion(asignacion)
    print("Asignación registrada correctamente.")
    print(f"Horas todavía disponibles del consultor: "
          f"{consultor.calcular_horas_disponibles(asignacion.mes, asignacion.anio):.2f} h")


def registrar_ejecucion(sistema):
    proyecto = solicitar_proyecto(sistema, "continuar")
    if proyecto is None:
        return
    if proyecto.estado == "Cerrado":
        error_campo("El proyecto está cerrado.", "No se puede modificar la ejecución de un proyecto cerrado.")
        return

    while True:
        print("\nEjecución")
        print("1. Registrar horas reales")
        print("2. Registrar gasto real")
        print("3. Actualizar avance de actividad")
        print("4. Completar entregable")
        print("5. Volver")
        opcion = input("Opción: ")

        if opcion == "1":
            actividad = seleccionar_objeto(proyecto.actividades, "Actividades")
            consultor = seleccionar_objeto(sistema.consultores, "Consultores")
            if actividad is None or consultor is None:
                continue

            esta_asignado = any(a.consultor is consultor for a in proyecto.asignaciones)
            if not esta_asignado:
                raise DatoInvalidoError("El consultor no tiene asignación en este proyecto.")

            codigos = [r.codigo for a in proyecto.actividades for r in a.registros_horas]
            codigo = leer_codigo("Código del registro: ", codigos, "R01")
            fecha = leer_fecha("Fecha")
            # El consultor debe estar asignado en el mes de la fecha.
            asignado_en_mes = any(
                a.consultor is consultor and a.mes == fecha.month and a.anio == fecha.year
                for a in proyecto.asignaciones
            )
            if not asignado_en_mes:
                raise DatoInvalidoError(
                    f"{consultor.nombre} no tiene asignación en {fecha.month:02d}/{fecha.year}. "
                    "Asígnelo primero en el menú 4."
                )
            registro = RegistroHoras(
                codigo, actividad, consultor, fecha,
                leer_float("Cantidad de horas (mayor a 0): ", 0.01)
            )
            actividad.agregar_registro_horas(registro)
            print("Horas reales registradas.")

        elif opcion == "2":
            gasto = seleccionar_objeto(proyecto.gastos, "Gastos")
            if gasto is not None:
                gasto.registrar_monto_real(leer_float("Monto real: ", 0))
                print("Gasto real actualizado.")

        elif opcion == "3":
            actividad = seleccionar_objeto(proyecto.actividades, "Actividades")
            if actividad is not None:
                actividad.actualizar_avance(leer_float("Nuevo avance (0 a 100 %): ", 0, 100))
                print("Avance actualizado.")

        elif opcion == "4":
            entregable = seleccionar_objeto(proyecto.entregables, "Entregables")
            if entregable is not None:
                entregable.marcar_completado()
                print("Entregable completado.")

        elif opcion == "5":
            break
        else:
            print("Opción no válida.")


def buscar_o_listar(sistema):
    if not sistema.proyectos:
        print("\n[ATENCIÓN] Todavía no hay proyectos para buscar. Registre uno en el menú 2.")
        return
    print("\nDeje el filtro vacío si no desea aplicarlo.")
    cliente = input("Cliente (nombre o código; Enter = todos): ").strip()
    pais = input("País (Perú/Ecuador/Colombia/Internacional; Enter = todos): ").strip()
    tipo = input("Tipo (Consultoria/Auditoria/Capacitacion; Enter = todos): ").strip()
    marco = input("Marco (código o nombre; Enter = todos): ").strip()
    estado = input("Estado (Abierto/Cerrado; Enter = todos): ").strip()

    resultados = sistema.filtrar_proyectos(cliente, pais, tipo, marco, estado)
    print(f"\nProyectos encontrados: {len(resultados)}")
    for proyecto in resultados:
        print(f"- {proyecto}")


def analizar_proyecto(sistema):
    proyecto = solicitar_proyecto(sistema, "continuar")
    if proyecto is None:
        return

    fecha_eval = leer_fecha("Fecha de evaluación")
    horas_plan = proyecto.calcular_horas_planificadas()
    horas_real = proyecto.calcular_horas_reales()
    costo_plan = proyecto.calcular_costo_planificado()
    costo_real = proyecto.calcular_costo_real()
    margen_plan = proyecto.calcular_margen_planificado()
    margen_real = proyecto.calcular_margen_real()
    avance_plan = proyecto.calcular_avance_planificado(fecha_eval)
    avance_real = proyecto.calcular_avance_real()

    print("\nANÁLISIS DEL PROYECTO")
    print(f"Proyecto: {proyecto}")
    print(f"Horas planificadas: {horas_plan:.2f}")
    print(f"Horas reales:       {horas_real:.2f}")
    print(f"Variación horas:    {horas_real - horas_plan:.2f}")
    print(f"Costo planificado:  {proyecto.moneda} {costo_plan:.2f}")
    print(f"Costo real:         {proyecto.moneda} {costo_real:.2f}")
    print(f"Margen planificado: {proyecto.moneda} {margen_plan:.2f}")
    print(f"Margen real:        {proyecto.moneda} {margen_real:.2f}")
    print(f"Variación margen:   {proyecto.moneda} {margen_real - margen_plan:.2f}")
    print(f"Avance planificado: {avance_plan:.2f}%")
    print(f"Avance real:        {avance_real:.2f}%")
    print(f"Estado de plazo:    {proyecto.evaluar_retraso(fecha_eval)}")


def validar_cierre(sistema):
    proyecto = solicitar_proyecto(sistema, "continuar")
    if proyecto is None:
        return

    proyecto.cerrar()
    print("El proyecto cumple las condiciones y ha sido cerrado.")


def actualizar_informacion(sistema):
    """Modificaciones y eliminaciones controladas; no cambia códigos."""
    while True:
        print("\nACTUALIZAR INFORMACIÓN")
        print("1. Cliente  2. Consultor  3. Marco de referencia")
        print("4. Proyecto  5. Asignación  6. Actividad")
        print("7. Entregable  8. Gasto planificado")
        print("9. Eliminar asignación  10. Eliminar actividad")
        print("11. Eliminar entregable  12. Volver")
        opcion = leer_int("Opción: ", 1, 12)
        if opcion == 12:
            return
        try:
            if opcion in (9, 10, 11):
                proyecto = solicitar_proyecto(sistema, "eliminar registros")
                if proyecto is None:
                    continue
                if proyecto.estado == "Cerrado":
                    raise DatoInvalidoError("Un proyecto cerrado no puede modificarse.")
                if opcion == 9:
                    elemento = seleccionar_objeto(proyecto.asignaciones, "Asignaciones del proyecto")
                    tipo = "asignación"
                elif opcion == 10:
                    elemento = seleccionar_objeto(proyecto.actividades, "Actividades del proyecto")
                    tipo = "actividad"
                else:
                    elemento = seleccionar_objeto(proyecto.entregables, "Entregables del proyecto")
                    tipo = "entregable"
                if elemento is None:
                    continue
                print(f"\nRegistro seleccionado para eliminar: {elemento}")
                if opcion == 9:
                    print(f"Horas reales vinculadas: {elemento.calcular_horas_reales():.2f}")
                elif opcion == 10:
                    print(f"Avance: {elemento.avance:.1f}% | Horas reales: {elemento.calcular_horas_reales():.2f}")
                    print("ATENCIÓN: después de eliminar, revise los pesos de las actividades para sumar 100% antes del cierre.")
                else:
                    print(f"Estado: {elemento.estado} | Obligatorio: {'Sí' if elemento.obligatorio else 'No'}")
                    print("ATENCIÓN: confirme que el cambio sea compatible con los compromisos del cliente.")
                if not leer_si_no(f"¿Confirma eliminar esta {tipo}?"):
                    print("Operación cancelada. No se modificó ningún registro.")
                    continue
                if opcion == 9:
                    proyecto.eliminar_asignacion(elemento)
                elif opcion == 10:
                    proyecto.eliminar_actividad(elemento)
                    restante = sum(a.peso for a in proyecto.actividades)
                    print(f"Peso total de actividades restantes: {restante:.1f}%.")
                    if restante != 100:
                        print("[ATENCIÓN] Actualice los pesos en la opción 9 antes del cierre.")
                else:
                    proyecto.eliminar_entregable(elemento)
                print(f"[OK] {tipo.capitalize()} eliminada correctamente.")
                continue
            if opcion == 1:
                cliente = seleccionar_objeto(sistema.clientes, "Clientes")
                if cliente is None:
                    continue
                print(f"Actual: {cliente.razon_social} | {cliente.contacto} | {cliente.pais}")
                accion = elegir("Modificar:", ("Razón social y contacto", "País"))
                if accion == "País":
                    nuevo = elegir("Nuevo país:", PAISES)
                    if any(p.cliente is cliente and p.estado == "Cerrado" for p in sistema.proyectos):
                        raise DatoInvalidoError("Existe un proyecto cerrado del cliente; conserve su país histórico.")
                    for proyecto in sistema.proyectos:
                        if proyecto.cliente is cliente:
                            for marco in proyecto.marcos_referencia:
                                if nuevo != "Internacional" and marco.pais not in ("Internacional", nuevo):
                                    raise DatoInvalidoError("El nuevo país es incompatible con un marco del proyecto. No se aplicó el cambio.")
                    cliente.actualizar_pais(nuevo)
                    for proyecto in sistema.proyectos:
                        if proyecto.cliente is cliente:
                            proyecto.actualizar_pais_desde_cliente(nuevo)
                else:
                    nombre = leer_texto("Nueva razón social: ", cliente.razon_social)
                    contacto = leer_texto("Nuevo contacto: ", cliente.contacto)
                    cliente.actualizar_datos(nombre, contacto)
            elif opcion == 2:
                consultor = seleccionar_objeto(sistema.consultores, "Consultores")
                if consultor is None:
                    continue
                print(f"Actual: {consultor} | Costo/h: {consultor.costo_hora} | Cese: {consultor.fecha_cese}")
                accion = elegir("Modificar:", ("Nivel", "Costo por hora", "Capacidad mensual", "Agregar especialidad", "Quitar especialidad", "Fecha de cese"))
                if accion == "Nivel":
                    consultor.actualizar_nivel(elegir("Nuevo nivel:", consultor.NIVELES_VALIDOS))
                    print("Las asignaciones existentes conservan el rol que tenían al crearse.")
                elif accion == "Costo por hora":
                    consultor.actualizar_costo(leer_float("Nuevo costo/hora: ", 0))
                    print("La nueva tarifa no altera costos históricos ya registrados.")
                elif accion == "Capacidad mensual":
                    consultor.actualizar_capacidad(leer_float("Nueva capacidad mensual: ", 0.01))
                elif accion == "Agregar especialidad":
                    marco = seleccionar_objeto(sistema.marcos_referencia, "Marcos de referencia")
                    if marco:
                        consultor.agregar_especialidad(marco)
                elif accion == "Quitar especialidad":
                    marco = seleccionar_objeto(consultor.especialidades, "Especialidades actuales")
                    if marco:
                        consultor.quitar_especialidad(marco)
                else:
                    print("Ingrese nueva fecha; deje vacío para indicar que sigue activo.")
                    consultor.actualizar_fecha_cese(leer_fecha("Nueva fecha de cese", True))
            elif opcion == 3:
                marco = seleccionar_objeto(sistema.marcos_referencia, "Marcos de referencia")
                if marco is None:
                    continue
                print(f"Actual: {marco.identificacion}, {marco.tipo}, {marco.pais}")
                tipo = elegir("Tipo:", ("ISO", "Legal", "Otro"))
                nombre = leer_texto("Identificación: ", marco.identificacion)
                pais = elegir("País:", PAISES)
                for proyecto in sistema.proyectos:
                    if marco in proyecto.marcos_referencia and proyecto.pais_ejecucion != "Internacional" and pais not in ("Internacional", proyecto.pais_ejecucion):
                        raise DatoInvalidoError(f"El cambio sería incompatible con el proyecto {proyecto.codigo}.")
                marco.actualizar_datos(tipo, nombre, pais)
            elif opcion == 4:
                proyecto = solicitar_proyecto(sistema, "actualizar proyectos")
                if proyecto is None:
                    continue
                if proyecto.estado == "Cerrado":
                    raise DatoInvalidoError("El proyecto está cerrado y no admite modificaciones.")
                accion = elegir("Modificar:", ("Nombre y precio contratado", "Fechas", "Agregar marco requerido"))
                if accion == "Nombre y precio contratado":
                    proyecto.actualizar_datos(leer_texto("Nuevo nombre: ", proyecto.nombre), leer_float("Nuevo precio: ", 0))
                elif accion == "Fechas":
                    print(f"Periodo actual: {proyecto.fecha_inicio} a {proyecto.fecha_fin}")
                    proyecto.actualizar_fechas(leer_fecha("Nuevo inicio"), leer_fecha("Nuevo fin"))
                else:
                    marco = seleccionar_objeto(sistema.marcos_referencia, "Marcos")
                    if marco:
                        if proyecto.pais_ejecucion != "Internacional" and marco.pais not in ("Internacional", proyecto.pais_ejecucion):
                            raise DatoInvalidoError("El ámbito del marco no coincide con el país del proyecto.")
                        proyecto.agregar_marco_actualizado(marco)
            elif opcion == 5:
                proyecto = solicitar_proyecto(sistema, "actualizar asignaciones")
                if proyecto is None:
                    continue
                if proyecto.estado == "Cerrado":
                    raise DatoInvalidoError("El proyecto está cerrado.")
                asignacion = seleccionar_objeto(proyecto.asignaciones, "Asignaciones")
                if asignacion is None:
                    continue
                print(f"Actual: {asignacion} | Proyecto: {proyecto.codigo}")
                accion = elegir("¿Qué desea modificar?", (
                    "Solo horas", "Consultor", "Periodo (mes y año)",
                    "Proyecto", "Varios datos a la vez"))
                destino = proyecto
                consultor = asignacion.consultor
                mes, anio = asignacion.mes, asignacion.anio
                horas = asignacion.horas_planificadas
                if accion in ("Proyecto", "Varios datos a la vez"):
                    destino = seleccionar_objeto(
                        [p for p in sistema.proyectos if p.estado != "Cerrado"],
                        "Proyectos abiertos (destino)")
                    if destino is None:
                        continue
                if accion in ("Consultor", "Varios datos a la vez"):
                    consultor = seleccionar_objeto(sistema.consultores, "Consultores")
                    if consultor is None:
                        continue
                if accion in ("Periodo (mes y año)", "Varios datos a la vez"):
                    mes = leer_int("Nuevo mes (1-12): ", 1, 12)
                    anio = leer_int("Nuevo año: ", 1900, 2200)
                if accion in ("Solo horas", "Varios datos a la vez"):
                    horas = leer_float("Nuevas horas planificadas: ", 0.01)
                if asignacion.calcular_horas_reales() > 0 and (
                    destino is not proyecto or consultor is not asignacion.consultor
                    or mes != asignacion.mes or anio != asignacion.anio
                ):
                    raise DatoInvalidoError(
                        "Existen horas ejecutadas. Mantenga la asignación histórica y "
                        "registre otra desde la opción 4 para el cambio solicitado."
                    )
                asignacion.actualizar_datos(destino, consultor, mes, anio, horas)
                print("Asignación actualizada correctamente.")
                print(f"Resultado: {asignacion} | Proyecto: {destino.codigo}")
            elif opcion in (6, 7, 8):
                proyecto = solicitar_proyecto(sistema, "actualizar planificación")
                if proyecto is None:
                    continue
                if proyecto.estado == "Cerrado":
                    raise DatoInvalidoError("No se pueden actualizar proyectos cerrados.")
                if opcion == 6:
                    actividad = seleccionar_objeto(proyecto.actividades, "Actividades")
                    if actividad is None:
                        continue
                    print(f"Actual: {actividad}")
                    nombre = leer_texto("Nuevo nombre: ", actividad.nombre)
                    etapa = leer_texto("Nueva etapa: ", actividad.etapa)
                    inicio = leer_fecha("Nuevo inicio")
                    fin = leer_fecha("Nuevo fin")
                    peso = leer_float("Nuevo peso (%): ", 0.01, 100)
                    responsable = actividad.responsable
                    if leer_si_no("¿Cambiar responsable?"):
                        responsable = seleccionar_objeto(sistema.consultores, "Consultores")
                        if responsable is None:
                            continue
                    proyecto.actualizar_actividad(actividad, nombre, etapa, inicio, fin, peso, responsable)
                elif opcion == 7:
                    entregable = seleccionar_objeto(proyecto.entregables, "Entregables")
                    if entregable is None:
                        continue
                    print(f"Actual: {entregable}")
                    nombre = leer_texto("Nuevo nombre: ", entregable.nombre)
                    fecha = leer_fecha("Nueva fecha de entrega")
                    peso = leer_float("Nuevo peso referencial: ", 0, 100)
                    obligatorio = leer_si_no("¿Es obligatorio?")
                    responsable = entregable.responsable
                    if leer_si_no("¿Cambiar responsable?"):
                        responsable = seleccionar_objeto(sistema.consultores, "Consultores")
                        if responsable is None:
                            continue
                    proyecto.actualizar_entregable(entregable, nombre, fecha, peso, obligatorio, responsable)
                else:
                    gasto = seleccionar_objeto(proyecto.gastos, "Gastos")
                    if gasto is None:
                        continue
                    gasto.actualizar_plan(leer_texto("Nuevo tipo: ", gasto.tipo), leer_float("Nuevo monto planificado: ", 0))
            print("[OK] Información actualizada correctamente.")
        except ErrorCapitalis as error:
            error_campo(str(error), "Revise las relaciones y las restricciones indicadas; no se aplicó el cambio rechazado.")


def cargar_datos_demo(sistema):
    """Carga mínima opcional para probar rápidamente el sistema."""
    marco_iso = MarcoReferencia("MR01", "ISO", "ISO 9001:2015", "Internacional")
    sistema.agregar_marco(marco_iso)

    cliente = Cliente("CLI01", "Empresa Demo S.A.C.", "Perú", "Contacto Demo")
    sistema.agregar_cliente(cliente)

    jr = Consultor("C01", "Consultor Jr", "Jr", 20, 160, date(2026, 1, 1))
    sr = Consultor("C02", "Consultor Sr", "Sr", 35, 160, date(2026, 1, 1))
    owner = Consultor("C03", "Consultor Owner", "Owner", 60, 160, date(2026, 1, 1))
    for consultor in (jr, sr, owner):
        consultor.agregar_especialidad(marco_iso)
        sistema.agregar_consultor(consultor)


def mostrar_menu():
    print("\n" + "=" * 60)
    print("CONTROL DE PROYECTOS DE SISTEMAS DE GESTIÓN - CAPITALIS")
    print("=" * 60)
    print("1. Registrar datos maestros")
    print("2. Registrar proyecto")
    print("3. Planificar proyecto (requiere proyecto)")
    print("4. Asignar consultores (requiere proyecto y consultor)")
    print("5. Registrar ejecución (requiere planificación)")
    print("6. Buscar o listar")
    print("7. Analizar proyecto")
    print("8. Validar cierre")
    print("9. Actualizar información")
    print("10. Salir")


def main():
    sistema = SistemaCapitalis()

    if leer_si_no("¿Desea cargar datos maestros de demostración?"):
        cargar_datos_demo(sistema)
        print("Datos maestros demo cargados.")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1 a 10): ").strip()

        try:
            if opcion == "1":
                registrar_datos_maestros(sistema)
            elif opcion == "2":
                registrar_proyecto(sistema)
            elif opcion == "3":
                planificar_proyecto(sistema)
            elif opcion == "4":
                asignar_consultor(sistema)
            elif opcion == "5":
                registrar_ejecucion(sistema)
            elif opcion == "6":
                buscar_o_listar(sistema)
            elif opcion == "7":
                analizar_proyecto(sistema)
            elif opcion == "8":
                validar_cierre(sistema)
            elif opcion == "9":
                actualizar_informacion(sistema)
            elif opcion == "10":
                print("Programa finalizado.")
                break
            else:
                print("Opción no válida.")

        except ErrorCapitalis as error:
            error_campo(str(error), "Revise el registro previo y los valores solicitados; puede volver a intentar desde el menú.")
        except ValueError as error:
            error_campo(str(error), "Revise el formato del dato indicado y vuelva a ingresar al menú.")
        except Exception as error:
            error_campo(f"Se produjo un error no previsto: {error}", "Revise el dato ingresado y vuelva al menú. Si se repite, consulte al responsable del programa.")


if __name__ == "__main__":
    main()
