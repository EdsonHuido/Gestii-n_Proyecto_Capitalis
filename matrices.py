# Porcentajes expresados como valores decimales.
# Las matrices provienen del Anexo 4 del trabajo parcial.

MATRICES_CONSULTORIA = {
    "Básico": {
        "Diagnóstico y levantamiento": {"Jr": 0.15, "Sr": 0.08, "Owner": 0.02},
        "Diseño y planificación": {"Jr": 0.15, "Sr": 0.07, "Owner": 0.01},
        "Implementación y seguimiento": {"Jr": 0.35, "Sr": 0.07, "Owner": 0.00},
        "Verificación y cierre": {"Jr": 0.05, "Sr": 0.03, "Owner": 0.02},
    },
    "Moderado": {
        "Diagnóstico y levantamiento": {"Jr": 0.0875, "Sr": 0.1125, "Owner": 0.03125},
        "Diseño y planificación": {"Jr": 0.10, "Sr": 0.125, "Owner": 0.03125},
        "Implementación y seguimiento": {"Jr": 0.2125, "Sr": 0.15, "Owner": 0.0125},
        "Verificación y cierre": {"Jr": 0.05, "Sr": 0.0625, "Owner": 0.025},
    },
    "Avanzado": {
        "Diagnóstico y levantamiento": {"Jr": 0.00, "Sr": 0.1458, "Owner": 0.1250},
        "Diseño y planificación": {"Jr": 0.00, "Sr": 0.1667, "Owner": 0.1250},
        "Implementación y seguimiento": {"Jr": 0.00, "Sr": 0.1875, "Owner": 0.0667},
        "Verificación y cierre": {"Jr": 0.00, "Sr": 0.10, "Owner": 0.0833},
    },
}

MATRICES_AUDITORIA = {
    "Básico": {
        "Planificación": {"Jr": 0.08, "Sr": 0.04, "Owner": 0.03},
        "Revisión documental": {"Jr": 0.20, "Sr": 0.05, "Owner": 0.00},
        "Ejecución de auditoría": {"Jr": 0.30, "Sr": 0.10, "Owner": 0.00},
        "Elaboración del informe": {"Jr": 0.10, "Sr": 0.05, "Owner": 0.00},
        "Cierre": {"Jr": 0.02, "Sr": 0.01, "Owner": 0.02},
    },
    "Moderado": {
        "Planificación": {"Jr": 0.06, "Sr": 0.10, "Owner": 0.04},
        "Revisión documental": {"Jr": 0.12, "Sr": 0.08, "Owner": 0.00},
        "Ejecución de auditoría": {"Jr": 0.14, "Sr": 0.18, "Owner": 0.00},
        "Elaboración del informe": {"Jr": 0.09, "Sr": 0.07, "Owner": 0.02},
        "Cierre": {"Jr": 0.04, "Sr": 0.02, "Owner": 0.04},
    },
    "Avanzado": {
        "Planificación": {"Jr": 0.00, "Sr": 0.13, "Owner": 0.12},
        "Revisión documental": {"Jr": 0.00, "Sr": 0.10, "Owner": 0.05},
        "Ejecución de auditoría": {"Jr": 0.00, "Sr": 0.15, "Owner": 0.10},
        "Elaboración del informe": {"Jr": 0.00, "Sr": 0.12, "Owner": 0.08},
        "Cierre": {"Jr": 0.00, "Sr": 0.10, "Owner": 0.05},
    },
}

MATRICES_CAPACITACION = {
    "Básico": {
        "Diseño de capacitación": {"Jr": 0.08, "Sr": 0.04, "Owner": 0.03},
        "Preparación de materiales y coordinación": {"Jr": 0.30, "Sr": 0.04, "Owner": 0.01},
        "Ejecución de capacitación": {"Jr": 0.28, "Sr": 0.12, "Owner": 0.00},
        "Evaluación y cierre": {"Jr": 0.04, "Sr": 0.05, "Owner": 0.01},
    },
    "Moderado": {
        "Diseño de capacitación": {"Jr": 0.07, "Sr": 0.13, "Owner": 0.05},
        "Preparación de materiales y coordinación": {"Jr": 0.22, "Sr": 0.15, "Owner": 0.03},
        "Ejecución de capacitación": {"Jr": 0.12, "Sr": 0.13, "Owner": 0.00},
        "Evaluación y cierre": {"Jr": 0.04, "Sr": 0.04, "Owner": 0.02},
    },
    "Avanzado": {
        "Diseño de capacitación": {"Jr": 0.00, "Sr": 0.16, "Owner": 0.14},
        "Preparación de materiales y coordinación": {"Jr": 0.00, "Sr": 0.20, "Owner": 0.10},
        "Ejecución de capacitación": {"Jr": 0.00, "Sr": 0.12, "Owner": 0.08},
        "Evaluación y cierre": {"Jr": 0.00, "Sr": 0.12, "Owner": 0.08},
    },
}

PORCENTAJE_EJECUCION_AUDITORIA = {
    "Básico": 0.40,
    "Moderado": 0.32,
    "Avanzado": 0.25,
}

PORCENTAJE_EJECUCION_CAPACITACION = {
    "Básico": 0.40,
    "Moderado": 0.25,
    "Avanzado": 0.20,
}

HORAS_CONSULTORIA = {
    "Básico": 300,
    "Moderado": 480,
    "Avanzado": 720,
}


def convertir_matriz_a_horas(total_horas, matriz):
    distribucion = {}
    for etapa, porcentajes in matriz.items():
        distribucion[etapa] = {}
        for nivel, porcentaje in porcentajes.items():
            distribucion[etapa][nivel] = total_horas * porcentaje
    return distribucion


def resumir_por_nivel(distribucion):
    resumen = {"Jr": 0.0, "Sr": 0.0, "Owner": 0.0}
    for etapa in distribucion.values():
        for nivel in resumen:
            resumen[nivel] += etapa.get(nivel, 0)
    return resumen
