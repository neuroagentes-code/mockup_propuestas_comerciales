# -*- coding: utf-8 -*-
"""
Asigna a cada caso de uso su SUPERFICIE de validación (draft/table/findings/form/steps),
su modo de AUTONOMÍA (Sugerir/Co-pilot/Autopilot) y el CONTENIDO de esa superficie.
Incluye curaduría específica para el informe de DVR Ingeniería y una inferencia genérica
para cualquier otro informe. Ver references/ux_aaas_estrategia.md.
"""
import re, unicodedata

def _na(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return s

# Palabras clave -> superficie (orden de prioridad)
SURFACE_KEYWORDS = [
    ("table",    ["comparativo", "cotizacion", "cotizaciones", "compras", "proveedor", "proveedores"]),
    ("steps",    ["ciclo", "poliza", "polizas", "flujo de", "etapas", "pago "]),
    ("form",     ["clasificar", "enrutar", "causacion", "siigo", "registro", "extrae", "datos"]),
    ("findings", ["analisis", "pre-analisis", "pre analisis", "hallazgos", "riesgos", "planos",
                  "estudios", "repositorio", "normativ", "vacios", "auditor"]),
    ("draft",    ["redactar", "respuesta", "correo", "acta", "actas", "informe", "informes",
                  "borrador", "reporte", "comunicado"]),
]

# Acciones de alto riesgo (nunca autopilot): firma, pago, envío a entidad
_ALTO_RIESGO = ["firma", "firmar", "pago", "pagar", "causacion", "transferenc", "contratante",
                "entidad", "interventoria", "fiducia", "publica", "legal"]

def inferir_surface(uc):
    txt = _na(uc.get("nombre", "") + " " + uc.get("descripcion", "") + " " + uc.get("auto", ""))
    for surf, kws in SURFACE_KEYWORDS:
        if any(k in txt for k in kws):
            return surf
    return "draft"

def inferir_autonomia(uc):
    txt = _na((uc.get("escala", "") or "") + " " + uc.get("nombre", ""))
    if any(k in txt for k in _ALTO_RIESGO):
        return "Sugerir"   # siempre compuerta humana
    return "Co-pilot"

# ---------------------------------------------------------------------------
# Curaduría específica para DVR Ingeniería (uc -> superficie + contenido + firma)
# ---------------------------------------------------------------------------
DVR = {
"UC-01": {"surface": "form", "autonomia": "Co-pilot", "contenido": {
    "destino": "Enrutar al tablero del responsable",
    "campos": [
        {"label": "Proyecto", "valor": "Findeter — Colegio El Carmen", "fuente": "asunto + cuerpo del correo", "diff": False},
        {"label": "Responsable", "valor": "Coordinador de obra · Andrea Pulido", "fuente": "matriz de responsables", "diff": False},
        {"label": "Etiqueta", "valor": "Interventoría / Requerimiento", "fuente": "clasificador", "diff": False},
        {"label": "Adjuntos", "valor": "2 PDF archivados en Drive del proyecto", "fuente": "correo", "diff": False},
        {"label": "Confianza de clasificación", "valor": "73% — por debajo del umbral", "fuente": "modelo", "diff": True},
    ]}},
"UC-02": {"surface": "draft", "autonomia": "Sugerir", "contenido": {
    "doc": "Correo", "para": "interventoria@fie.gov.co", "asunto": "Respuesta a requerimiento técnico RT-118",
    "cuerpo": "Estimados,\n\nEn atención a su requerimiento RT-118, remitimos la aclaración solicitada sobre el ítem de cimentación. Según el diseño estructural aprobado (plano E-04, rev. C), la profundidad de desplante corresponde a 1.80 m, consistente con el estudio de suelos del Anexo 3.\n\nQuedamos atentos a cualquier observación adicional.\n\nCordialmente,\nDVR Ingeniería S.A.S.",
    "checklist": ["Insumo encontrado en Drive: plano E-04 rev. C", "Falta: confirmar si adjuntar el estudio de suelos completo"]}},
"UC-03": {"surface": "draft", "autonomia": "Co-pilot", "contenido": {
    "doc": "Acta", "asunto": "Acta — Comité técnico semanal (07/06)",
    "cuerpo": "ASISTENTES: J. Arturo (gerencia), A. Pulido (obra), interventoría FIE.\n\nTEMAS:\n1. Avance de obra 62%, dentro de cronograma.\n2. Pendiente entrega de pólizas actualizadas.\n3. Observación de interventoría sobre acabados piso 2.",
    "checklist": ["Compromiso: enviar pólizas actualizadas — A. Pulido — vence 12/06",
                  "Compromiso: subsanar acabados piso 2 — contratista — vence 14/06",
                  "Compromiso: remitir informe semanal — coordinador — vence 09/06"]}},
"UC-04": {"surface": "findings", "autonomia": "Sugerir", "firma": True, "contenido": {
    "items": [
        {"sev": "alto", "texto": "Cláusula 8.3: multa por mora del 1% diario sin tope máximo definido.", "fuente": "Contrato, pág. 14"},
        {"sev": "alto", "texto": "Anexo 2 exige póliza de estabilidad por 5 años; el borrador actual contempla 3.", "fuente": "Anexo 2 — TdR"},
        {"sev": "medio", "texto": "Norma NSR-10 referenciada en versión 2010; vigente con actualización 2023 (vía UC-08).", "fuente": "Repositorio normativo"},
        {"sev": "medio", "texto": "Matriz de riesgos no asigna el riesgo cambiario; queda en cabeza del contratista por defecto.", "fuente": "Matriz de riesgos"},
        {"sev": "info", "texto": "Objeto contractual y plazos coinciden con los Estudios Previos.", "fuente": "Estudios Previos"},
    ],
    "fuentes": ["Contrato (28 pág.)", "Anexo 1–4", "Estudios Previos", "Matriz de riesgos"]}},
"UC-05": {"surface": "steps", "autonomia": "Co-pilot", "contenido": {
    "pasos": [
        {"nombre": "Solicitud de pólizas al proveedor (García Garzón)", "estado": "hecho", "detalle": "Correo enviado con contrato + actas de inicio adjuntos."},
        {"nombre": "Recepción y verificación de pólizas", "estado": "hecho", "detalle": "3 pólizas recibidas; vigencias verificadas."},
        {"nombre": "Envío a la Fiducia (cc interventoría)", "estado": "actual", "detalle": "Correo redactado y listo; requiere tu aprobación para enviar."},
        {"nombre": "Remisión a contabilidad para pago", "estado": "pendiente", "detalle": "Solicitud de pago preparada; se habilita tras el envío a Fiducia."},
    ]}},
"UC-06": {"surface": "findings", "autonomia": "Co-pilot", "contenido": {
    "items": [
        {"sev": "alto", "texto": "Estructural: falta memoria de cálculo de la losa de entrepiso del eje 4–6.", "fuente": "Plano E-07"},
        {"sev": "medio", "texto": "Hidrosanitario: diámetros de bajante no coinciden entre plano y especificación.", "fuente": "Plano HS-02 vs. especificación"},
        {"sev": "medio", "texto": "Eléctrico: cuadro de cargas sin el circuito de la subestación.", "fuente": "Plano EL-03"},
        {"sev": "info", "texto": "Arquitectónico: planta y cortes consistentes; sin observaciones.", "fuente": "Planos A-01..A-05"},
    ],
    "fuentes": ["Planos estructurales", "Hidrosanitarios", "Eléctricos", "Arquitectónicos"]}},
"UC-07": {"surface": "draft", "autonomia": "Co-pilot", "contenido": {
    "doc": "Informe", "asunto": "Informe semanal de interventoría — semana 23",
    "cuerpo": "1. AVANCE FÍSICO: 62% (programado 60%).\n2. AVANCE FINANCIERO: 58% ejecutado.\n3. PERSONAL EN OBRA: 34 personas.\n4. ACTIVIDADES DE LA SEMANA: fundición de placa piso 3, instalación de redes.\n5. OBSERVACIONES DE CALIDAD: 1 no conformidad menor (acabados piso 2), en subsanación.\n6. PRÓXIMA SEMANA: mampostería piso 3, inicio de enchapes.",
    "checklist": ["Estructura obligatoria de la interventoría: completa", "Listo para envío el lunes tras tu validación"]}},
"UC-08": {"surface": "findings", "autonomia": "Co-pilot", "contenido": {
    "items": [
        {"sev": "alto", "texto": "NSR-10 Título A actualizada (Decreto 2023); afecta el proyecto Findeter — Colegio El Carmen.", "fuente": "Diario Oficial"},
        {"sev": "medio", "texto": "Resolución de interventoría 2024 modifica formato del informe semanal (vinculado a UC-07).", "fuente": "Min. correspondiente"},
        {"sev": "info", "texto": "RETIE sin cambios en lo que va del año.", "fuente": "Repositorio"},
    ],
    "fuentes": ["Diario Oficial", "Repositorio normativo vivo"]}},
"UC-09": {"surface": "table", "autonomia": "Sugerir", "firma": True, "contenido": {
    "columnas": ["Criterio", "Ferretería Andina", "Construmax", "Suministros del Valle"],
    "filas": [
        ["Precio total", "$ 48.200.000", "$ 45.900.000", "$ 51.300.000"],
        ["Tiempo de entrega", "8 días", "12 días", "5 días"],
        ["Garantía", "12 meses", "6 meses", "12 meses"],
        ["Cumple ficha técnica", "Sí", "Parcial", "Sí"],
        ["Historial con DVR", "3 órdenes", "Nuevo", "7 órdenes"],
    ],
    "recomendado": 3,
    "nota": "El agente recomienda Suministros del Valle: mejor historial, entrega más rápida y cumple ficha; el sobrecosto vs. Construmax (+$5.4M) se compensa con la garantía y el tiempo."}},
"UC-10": {"surface": "form", "autonomia": "Sugerir", "firma": True, "contenido": {
    "destino": "Causar en Siigo y autorizar pago",
    "campos": [
        {"label": "Proveedor (de RUT)", "valor": "Suministros del Valle S.A.S. — NIT 900.123.456-7", "fuente": "RUT leído", "diff": False},
        {"label": "Creado en Siigo", "valor": "Sí — tercero #4471", "fuente": "Siigo", "diff": False},
        {"label": "Valor cotización aprobada", "valor": "$ 51.300.000", "fuente": "UC-09", "diff": False},
        {"label": "Valor factura recibida", "valor": "$ 53.800.000", "fuente": "Factura FV-2210", "diff": True},
        {"label": "Diferencia", "valor": "+$ 2.500.000 (4.9%) — se escala a contabilidad", "fuente": "comparación", "diff": True},
    ]}},
}

# Contenido genérico (informes que no son DVR): se arma desde los campos del UC.
def _generico(uc, surface):
    desc = uc.get("descripcion", "") or "El agente preparó este insumo."
    auto = uc.get("auto", "")
    inc = uc.get("incluye", []) if isinstance(uc.get("incluye"), list) else []
    if surface == "draft":
        return {"doc": "Borrador", "asunto": uc.get("nombre", "Borrador"),
                "cuerpo": desc + (("\n\nEl agente resolvió: " + auto) if auto else ""),
                "checklist": inc[:4]}
    if surface == "findings":
        items = [{"sev": "info", "texto": x, "fuente": "informe"} for x in (inc[:5] or [auto or desc])]
        return {"items": items, "fuentes": []}
    if surface == "form":
        return {"destino": "Confirmar y registrar", "campos": [
            {"label": "Resumen", "valor": (auto or desc)[:80], "fuente": "agente", "diff": False}]}
    if surface == "steps":
        partes = [p.strip() for p in re.split(r"[.;]", (uc.get("proceso") or auto or desc)) if p.strip()][:4]
        pasos = []
        for j, p in enumerate(partes):
            pasos.append({"nombre": p[:80], "estado": "hecho" if j < len(partes) - 2 else ("actual" if j == len(partes) - 2 else "pendiente"), "detalle": ""})
        return {"pasos": pasos or [{"nombre": "Paso preparado", "estado": "actual", "detalle": ""}]}
    if surface == "table":
        return {"columnas": ["Criterio", "Opción A", "Opción B"], "filas": [["—", "—", "—"]], "recomendado": 1,
                "nota": "Comparativo de ejemplo; el agente lo arma con los datos reales."}
    return {}

def _tool_de(p):
    t = _na(p)
    if any(k in t for k in ["compar", "valida", "verifica", "vigencia", "calcul", "contra cotiz"]):
        return "Cálculo / comparación"
    if any(k in t for k in ["clasifi", "enruta", "etiqueta"]):
        return "Clasificador"
    if any(k in t for k in ["siigo", "proveedor", "anticipo", "causa"]):
        return "Conector Siigo"
    if any(k in t for k in ["drive", "busca", "insumo", "repositorio"]):
        return "Búsqueda en Drive"
    if any(k in t for k in ["redacta", "genera", "resumen", "informe", "acta", "borrador", "transcri"]):
        return "Generación (LLM)"
    if any(k in t for k in ["envia", "envio", "correo", "notifica", "alerta"]):
        return "Correo / API"
    if any(k in t for k in ["rut", "lee", "lectura", "factura", "documento", "plano", "contrato", "ocr"]):
        return "Lectura / OCR"
    return "Herramienta"

def traza_de(uc):
    """Arma una traza de corrida (observabilidad) desde el auto/escala del UC."""
    auto = uc.get("auto", "") or ""
    partes = [p.strip(" .") for p in re.split(r",| y ", auto) if p.strip(" .")]
    pasos = []
    for i, p in enumerate(partes[:6]):
        accion = (p[:1].upper() + p[1:]) if p else "Paso"
        pasos.append({"accion": accion, "tool": _tool_de(p), "dur": f"{0.4 + 0.3 * i:.1f}s", "estado": "ok"})
    pasos.append({"accion": "Pausa y escala a validación humana", "tool": "HITL gate", "dur": "—",
                  "estado": "hold", "detalle": uc.get("escala", "") or "Requiere validación humana."})
    n = max(1, len(partes))
    return {"pasos": pasos, "modelo": "orquestador + herramientas",
            "latencia": f"{2.0 + 0.4 * n:.1f}s", "tokens": f"{(3200 + 700 * n):,}".replace(",", ".")}

def enriquecer(uc, nombre_cliente):
    """Devuelve (surface, autonomia, contenido, firma, traza) para un UC."""
    es_dvr = "dvr" in _na(nombre_cliente)
    code = uc.get("uc", "").upper()
    traza = traza_de(uc)
    if es_dvr and code in DVR:
        d = DVR[code]
        return d["surface"], d.get("autonomia", "Co-pilot"), d["contenido"], d.get("firma", False), traza
    surf = inferir_surface(uc)
    return surf, inferir_autonomia(uc), _generico(uc, surf), inferir_autonomia(uc) == "Sugerir", traza
