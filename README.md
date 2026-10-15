# CAPITALIS FP2 — Versión con actualización de información

## Ejecución
Abra esta carpeta en Visual Studio Code. Ejecute únicamente `main.py` (Python 3.10 o superior). No ejecute directamente los archivos de clases. No requiere instalar dependencias externas.

## Menú
1. Registrar datos maestros
2. Registrar proyecto
3. Planificar proyecto
4. Asignar consultores
5. Registrar ejecución
6. Buscar o listar
7. Analizar proyecto
8. Validar cierre
9. Actualizar información **(nueva opción)**
10. Salir

## Actualizaciones disponibles desde la opción 9
- **Cliente**: razón social, contacto y país. El país se transmite a los proyectos abiertos y se valida frente a sus marcos.
- **Consultor**: nivel Jr/Sr/Owner, tarifa, capacidad mensual, especialidades y fecha de cese. Los ascensos NO modifican los roles de asignaciones previas.
- **Marco**: tipo, identificación y ámbito de aplicación.
- **Proyecto abierto**: nombre, precio, fechas y agregar marcos. Las nuevas fechas deben incluir actividades, entregables y meses asignados.
- **Asignación**: permite cambiar consultor, periodo, proyecto y horas planificadas. Valida compatibilidad con los marcos, vigencia, duplicados, periodo del proyecto y límite de capacidad del 90 %. Si existen horas reales, solo permite modificar horas planificadas (sin reducirlas por debajo de lo ejecutado); para reasignar se crea otra asignación desde el menú 4. Al cambiar de consultor se toma el rol y tarifa actuales del nuevo consultor.
- **Actividad**: nombre, etapa, fechas, peso y responsable.
- **Entregable**: nombre, fecha, peso, obligatoriedad y responsable.
- **Gasto**: tipo y monto planificado.

## Reglas de integridad
- Los códigos de los registros se conservan para no romper vínculos.
- Los proyectos cerrados quedan bloqueados para edición y ejecución.
- El costo/hora se conserva como fotografía al crear una asignación o un registro de horas: cambios de tarifa no recalculan esas partidas. Las nuevas asignaciones y registros utilizan la tarifa nueva.
- Los datos se almacenan en **memoria**. Se pierden al terminar la ejecución; esta versión no incorpora base de datos ni persistencia.
- Países válidos: Perú, Ecuador, Colombia e Internacional.
- La opción 9 es una función de mantenimiento del sistema; no incorpora pruebas automáticas.

## Cambios recomendados en UML
- Incorporar operaciones `actualizar_*` de las clases `Cliente`, `MarcoReferencia`, `Consultor`, `Proyecto`, `Actividad`, `Entregable`, `Gasto` y `Asignacion`.
- Incorporar `costo_hora_pactado` (Asignacion) y `costo_hora_registrado` (RegistroHoras) si el UML incluye todos los atributos.
- Representar `SistemaCapitalis` como controlador de colecciones, si se representa la capa de aplicación.
- La interfaz de menú es una función de `main.py`; no requiere convertirla en una clase.


## Eliminación controlada (menú principal 9)

En Actualizar información se incorporaron las opciones 9, 10 y 11 para eliminar
asignaciones, actividades y entregables, respectivamente. Todas requieren confirmar S/N.

- Asignaciones: solo si no existen horas reales de ese consultor en ese periodo;
  se liberan las horas planificadas. Si el consultor sigue como responsable de
  actividades o entregables y no conserva otra asignación en el mismo proyecto,
  debe cambiarse primero el responsable.
- Actividades: solo si no existe avance ni registros de horas. Si los pesos
  restantes no suman 100 %, deben redistribuirse usando la actualización de
  actividades antes de cerrar el proyecto.
- Entregables: solo si están pendientes. Confirme que no incumple compromisos
  asumidos con el cliente.
- No se permiten eliminaciones en proyectos cerrados.

No se añadieron funciones de pruebas al código de uso normal. Ejecute solo `main.py`.
