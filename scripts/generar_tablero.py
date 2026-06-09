#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_tablero.py — Del Informe de Diagnóstico de NeuroAgentes al mockup de la
Plataforma: el Tablero de Validación, con agentes por ÁREA (Comercial, Marketing,
Finanzas, Operaciones, Administrativo) y soporte MULTI-EMPRESA.

Lee el informe (.md de neuroagentes-pipeline, o .docx renderizado), extrae cada
caso de uso (### UC-XX) y su :::hitl (auto/escala/notifica), infiere a qué ÁREA
pertenece, y arma un agente por área con sus tareas en kanban de validación.
La plataforma es multi-tenant: cada empresa es una pestaña; se acumulan con --merge.

Uso:
    python generar_tablero.py --informe informe.md --cliente "DVR Ingeniería" --sector "Ingeniería" --salida tablero.html
    python generar_tablero.py --informe otro.md --cliente "Pizza 203" --sector "Retail" --merge tablero_modelo.json --salida tablero.html
    python generar_tablero.py --modelo tablero_modelo.json --salida tablero.html      # render desde modelo editado
Opciones:
    --solo-cliente   No incluir la empresa de ejemplo (Aurora Retail).
    --dump-json X    Vuelca el modelo intermedio (para editar/acumular).
"""
import argparse, json, re, sys, datetime, unicodedata
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from surfaces_dvr import enriquecer

AQUI = Path(__file__).resolve().parent
PLANTILLA = AQUI.parent / "assets" / "plantilla_tablero.html"

# ---- Departamentos canónicos (codename de la línea gráfica NeuroAgentes) ----
DEPARTAMENTOS = [
    {"id": "comercial",      "nombre": "Comercial",      "codename": "Vector", "icon": "comercial",      "tint": "--comercial"},
    {"id": "marketing",      "nombre": "Marketing",      "codename": "Muse",   "icon": "marketing",      "tint": "--marketing"},
    {"id": "finanzas",       "nombre": "Finanzas",       "codename": "Ledger", "icon": "finanzas",       "tint": "--finanzas"},
    {"id": "operaciones",    "nombre": "Operaciones",    "codename": "Orion",  "icon": "operaciones",    "tint": "--operaciones"},
    {"id": "administrativo", "nombre": "Administrativo", "codename": "Atlas",  "icon": "administrativo", "tint": "--administrativo"},
    {"id": "soporte",        "nombre": "Soporte",        "codename": "Lyra",   "icon": "soporte",        "tint": "--soporte"},
]

# Palabras clave por área (sin tildes, minúsculas). Orden = prioridad de desempate.
KEYWORDS = [
    ("finanzas",       ["factur", "pago", "cobr", "causac", "poliza", "siigo", "contab", "presupuesto",
                         "anticipo", "tesoreria", "recaudo", "cartera", "financ", "nomina", "impuesto", "rut "]),
    ("comercial",      ["comercial", "venta", " lead", "cotiz", "propuesta", "crm", "embudo", "prospec",
                        "oportunidad", "cierre", "negociac", "cliente potencial"]),
    ("marketing",      ["marketing", "campaña", "campana", "contenido", "redes", "remarketing", "seo",
                        "publicidad", "linkedin", "newsletter", "anuncio", "post "]),
    ("soporte",        ["soporte", "ticket", "pqr", "atencion al cliente", "reclamo", "incidencia", "queja"]),
    ("operaciones",    ["plano", "tecnic", "especialista", "interventoria", "inventario", "pedido",
                        "proveedor", "compra", "logistic", "obra", "produccion", "despacho",
                        "insumo", "memoria", "apu", "dwg", "autocad", "licitacion", "pliego"]),
    ("administrativo", ["correo", "correspondencia", "acta", "contrato", "documento", "archiv", "agenda",
                        "reunion", "rrhh", "recursos humanos", "firma", "legal", "tramite", "comunicac"]),
]
DESCRIPCION_DEP = {
    "comercial": "Atiende leads, prepara cotizaciones y propuestas, y mueve el embudo de ventas.",
    "marketing": "Crea contenido y campañas, y nutre la relación con prospectos y clientes.",
    "finanzas": "Gestiona facturas, pagos, cobranza y conciliación contable.",
    "operaciones": "Coordina proyectos, compras, proveedores e insumos técnicos.",
    "administrativo": "Gestiona correspondencia, actas, contratos y documentos.",
    "soporte": "Resuelve consultas y tickets de clientes con fuentes autorizadas.",
}
SECUENCIA_DEMO = ["pendiente", "pendiente", "en_proceso", "pendiente", "hecho", "en_proceso"]

COLUMNAS = [
    {"id": "pendiente",  "nombre": "Pendiente",  "tipo": "escala", "desc": "El agente dejó esto listo y espera tu validación."},
    {"id": "en_proceso", "nombre": "En Proceso", "tipo": "humano", "desc": "En revisión o ejecutándose tras tu visto bueno."},
    {"id": "hecho",      "nombre": "Hecho",      "tipo": "done",   "desc": "Validado y ejecutado por el agente."},
]


def na(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


# ---------------- lectura del informe ----------------

def leer_informe(ruta):
    ruta = Path(ruta)
    if ruta.suffix.lower() in (".md", ".txt"):
        return ruta.read_text(encoding="utf-8")
    if ruta.suffix.lower() == ".docx":
        try:
            from docx import Document
        except ImportError:
            sys.exit("Para leer .docx: pip install python-docx --break-system-packages")
        doc = Document(str(ruta)); out = []
        for p in doc.paragraphs:
            t = p.text.rstrip(); est = (p.style.name or "").lower()
            if not t: out.append(""); continue
            if re.match(r"\s*UC-\d+", t): out.append("### " + t)
            elif "heading 1" in est or est == "title": out.append("# " + t)
            else: out.append(t)
        return "\n".join(out)
    sys.exit("Formato no soportado: usa .md o .docx")


def extraer_ucs(md):
    ucs = []
    patron = re.compile(r"^###\s+(UC-\d+)\s*[—–-]\s*(.+?)\s*$", re.M)
    marcas = [(m.start(), m.group(1), m.group(2)) for m in patron.finditer(md)]
    for i, (pos, cod, nom) in enumerate(marcas):
        fin = marcas[i + 1][0] if i + 1 < len(marcas) else len(md)
        sec = re.search(r"^#\s+\S", md[pos + 1:fin], re.M)
        bloque = md[pos:(pos + 1 + sec.start()) if sec else fin]
        hitl = _bloque(bloque, "hitl")
        ucs.append({
            "uc": cod, "nombre": nom.strip(),
            "descripcion": _campo(bloque, "Descripci[oó]n"),
            "auto": _linea(hitl, "auto"), "escala": _linea(hitl, "escala"), "notifica": _linea(hitl, "notifica"),
        })
    return ucs


def _bloque(t, n):
    m = re.search(r":::" + n + r"\s*\n(.*?)\n:::", t, re.S); return m.group(1) if m else ""
def _linea(h, k):
    m = re.search(r"^\s*" + k + r"\s*:\s*(.+?)\s*$", h, re.M); return m.group(1).strip() if m else ""
def _campo(b, et):
    m = re.search(r"\*\*" + et + r"\*\*\s*\n+\s*(.+?)(?:\n\n|\n\*\*|\n:::|$)", b, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


# ---------------- inferencias ----------------

def inferir_area(uc):
    txt = na(uc["nombre"] + " " + uc.get("descripcion", "") + " " + uc.get("auto", "") + " " + uc.get("escala", ""))
    puntajes = {}
    for dep, claves in KEYWORDS:
        puntajes[dep] = sum(1 for k in claves if k in txt)
    mejor = max(puntajes, key=lambda d: puntajes[d])
    return mejor if puntajes[mejor] > 0 else "administrativo"  # catch-all: documentos/correos


def inferir_prioridad(uc):
    t = na(uc.get("escala", "") + " " + uc.get("notifica", ""))
    claves = ["entidad publica", "contratante", "interventoria", "findeter", " men", " fie",
              "prioridad alta", "urgente", "doble click", "nunca", "sin aprobacion",
              "representante legal", "firma", "pago", "contrato"]
    return "alta" if any(k in t for k in claves) else "normal"


def inferir_confianza(uc):
    t = na(uc.get("escala", ""))
    if any(k in t for k in ["baja confianza", "no identific", "incierto", "no reconocid", "duda", "sin fuente"]):
        return 58
    if any(k in t for k in ["todo ", "siempre", "nunca", "cada ", "doble click"]):
        return 92
    return 78


def inferir_canales(uc):
    t = na(uc.get("notifica", "")); c = ["Plataforma"]
    if "whatsapp" in t: c.append("WhatsApp")
    if "correo" in t or "email" in t or "mail" in t: c.append("Correo")
    return c


def corto(s, n=46):
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


def titulo_tarea(uc):
    base = re.split(r"\s+(?:por|con|a partir de|para|y)\s+", uc["nombre"], 1)[0].strip()
    verbo = na(base.split()[0]) if base.split() else ""
    plant = {"clasificar": "Correo entrante por clasificar", "redactar": "Borrador listo para tu visto bueno",
             "generar": "Documento generado, pendiente de revisión", "analizar": "Análisis listo para tu revisión",
             "analisis": "Análisis listo para tu revisión", "automatizar": "Paso del ciclo a la espera de tu OK",
             "pre-analisis": "Pre-diagnóstico listo", "causacion": "Causación preparada, pendiente de registrar",
             "monitorear": "Alertas detectadas para tu revisión", "generacion": "Informe en borrador para revisión"}
    return plant.get(verbo, corto(base, 40) + " — pendiente de validación")


def construir_empresa_desde_informe(ucs, nombre, sector):
    eid = re.sub(r"[^a-z0-9]+", "-", na(nombre)).strip("-") or "cliente"
    por_dep = {}
    tareas = []
    for i, uc in enumerate(ucs):
        dep = inferir_area(uc); prio = inferir_prioridad(uc); conf = inferir_confianza(uc); can = inferir_canales(uc)
        por_dep.setdefault(dep, []).append(uc)
        # Reparte por todo el ciclo para mostrar el tablero completo; la prioridad es un distintivo aparte.
        col = SECUENCIA_DEMO[i % len(SECUENCIA_DEMO)]
        surface, autonomia, contenido, firma, traza = enriquecer(uc, nombre)
        propuesta = "\n\n".join(filter(None, [
            uc.get("descripcion", ""),
            ("El agente resolvió por su cuenta: " + uc["auto"]) if uc.get("auto") else "",
            "Acción propuesta: ejecutar este paso una vez lo apruebes."]))
        tareas.append({
            "id": f"{eid}-{uc['uc'].lower()}", "dep": dep, "uc": uc["uc"], "columna": col,
            "titulo": titulo_tarea(uc),
            "resumen": corto("El agente dejó listo: " + ((uc.get("auto") or "el trabajo previo")[:1].lower() + (uc.get("auto") or "el trabajo previo")[1:]), 150),
            "propuesta": propuesta,
            "razon_escala": uc.get("escala", "") or "Requiere tu visto bueno antes de ejecutarse.",
            "confianza": conf, "prioridad": prio, "canales": can,
            "fecha": (datetime.date.today() - datetime.timedelta(days=(i % 9))).strftime("%d/%m/%Y"),
            "surface": surface, "autonomia": autonomia, "firma": firma, "contenido": contenido, "traza": traza,
            "chat": [{"de": "agente", "texto": "Dejé esto listo para tu visto bueno. Puedo ajustarlo si me dices qué cambiar, o apruébalo para ejecutarlo."}],
        })
    agentes = []
    for dep, lista in por_dep.items():
        agentes.append({
            "dep": dep, "nombre": next(d["nombre"] for d in DEPARTAMENTOS if d["id"] == dep),
            "descripcion": DESCRIPCION_DEP.get(dep, "") + f" ({len(lista)} flujo{'s' if len(lista)!=1 else ''}: " + ", ".join(u["uc"] for u in lista) + ").",
            "escala": (lista[0].get("escala") or ""),
        })
    # orden de agentes según DEPARTAMENTOS
    orden = {d["id"]: i for i, d in enumerate(DEPARTAMENTOS)}
    agentes.sort(key=lambda a: orden.get(a["dep"], 99))
    return {"id": eid, "nombre": nombre, "sector": sector, "agentes": agentes, "tareas": tareas}


def empresa_ejemplo():
    """Empresa demo con las 5 áreas pobladas, para mostrar la estructura multi-empresa."""
    def t(dep, col, titulo, resumen, propuesta, razon, conf, prio, can, uc=None):
        return {"id": f"aurora-{dep}-{col}-{abs(hash(titulo))%9999}", "dep": dep, "uc": uc, "columna": col,
                "titulo": titulo, "resumen": resumen, "propuesta": propuesta, "razon_escala": razon,
                "confianza": conf, "prioridad": prio, "canales": can,
                "fecha": (datetime.date.today() - datetime.timedelta(days=abs(hash(titulo)) % 7)).strftime("%d/%m/%Y"),
                "chat": [{"de": "agente", "texto": "Dejé esto listo. Dime si ajusto algo o apruébalo para ejecutar."}]}
    tareas = [
        t("comercial", "pendiente", "Cotización para lead caliente", "El agente redactó la cotización con el catálogo y el descuento vigente.",
          "El lead pidió precio de 200 unidades. El agente armó la cotización con el precio de lista y un 8% de descuento por volumen.\n\nAcción propuesta: enviar la cotización por WhatsApp al lead.",
          "Toda cotización con descuento > 5% requiere tu visto bueno antes de enviarse.", 88, "alta", ["Plataforma", "WhatsApp"]),
        t("comercial", "en_proceso", "Seguimiento a oportunidad estancada", "El agente detectó 4 oportunidades sin movimiento hace 15 días.",
          "El agente propone un mensaje de reactivación para cada oportunidad detenida.", "Reactivación de oportunidades: requiere tu aprobación del mensaje.", 74, "normal", ["Plataforma"]),
        t("marketing", "pendiente", "Campaña 'Cyber lunes · 15%'", "El agente preparó el copy y la pieza para la campaña de descuento.",
          "Borrador de campaña para redes y correo con el 15% de descuento del Cyber lunes.\n\nAcción propuesta: programar la publicación para el lunes 8 a.m.",
          "Toda publicación queda en borrador hasta tu aprobación.", 90, "normal", ["Plataforma", "Correo"]),
        t("finanzas", "pendiente", "Factura por encima del comparativo", "El agente detectó una factura 12% mayor a la cotización aprobada.",
          "El proveedor facturó $1.240.000; la cotización aprobada era $1.105.000.\n\nAcción propuesta: retener el registro hasta aclarar la diferencia.",
          "Cualquier diferencia entre factura y cotización se escala a Finanzas antes de causar.", 60, "alta", ["Plataforma"]),
        t("finanzas", "hecho", "Conciliación bancaria del día", "El agente concilió 38 movimientos contra el extracto.",
          "Conciliación automática completada; 1 movimiento marcado para revisión manual.", "—", 95, "normal", ["Plataforma"]),
        t("operaciones", "en_proceso", "Orden de compra a proveedor", "El agente arma el comparativo de 3 proveedores para insumos.",
          "El agente está cotizando con 3 proveedores y armará el cuadro comparativo.", "La orden de compra requerirá tu firma antes de enviarse.", 80, "normal", ["Plataforma"]),
        t("operaciones", "pendiente", "Pedido a despacho — stock bajo", "El agente preparó el pedido de reposición para 6 referencias bajo mínimos.",
          "6 referencias por debajo del stock mínimo. El agente preparó el pedido de reposición.\n\nAcción propuesta: confirmar para enviar al proveedor habitual.",
          "Pedidos de reposición requieren tu confirmación.", 84, "normal", ["Plataforma", "WhatsApp"]),
        t("administrativo", "pendiente", "Acta de la reunión de comité", "El agente transcribió la reunión y armó el acta con compromisos.",
          "Acta con 5 compromisos y responsables identificados.\n\nAcción propuesta: enviar el acta a los participantes tras tu aprobación.",
          "El acta se envía solo tras tu aprobación.", 86, "normal", ["Plataforma", "Correo"]),
    ]
    deps = sorted({x["dep"] for x in tareas}, key=lambda d: [dd["id"] for dd in DEPARTAMENTOS].index(d))
    agentes = [{"dep": d, "nombre": next(x["nombre"] for x in DEPARTAMENTOS if x["id"] == d),
                "descripcion": DESCRIPCION_DEP[d], "escala": ""} for d in deps]
    return {"id": "aurora-retail", "nombre": "Aurora Retail", "sector": "Retail · e-commerce (ejemplo)", "agentes": agentes, "tareas": tareas}


def render(modelo, salida):
    if not PLANTILLA.exists():
        sys.exit(f"No encuentro la plantilla en {PLANTILLA}")
    html = PLANTILLA.read_text(encoding="utf-8")
    html = html.replace("__MODELO_JSON__", json.dumps(modelo, ensure_ascii=False))
    Path(salida).write_text(html, encoding="utf-8")
    return salida


def main():
    ap = argparse.ArgumentParser(description="Genera el Tablero de Validación multi-empresa de NeuroAgentes.")
    ap.add_argument("--informe"); ap.add_argument("--modelo")
    ap.add_argument("--cliente", default="Cliente"); ap.add_argument("--sector", default="")
    ap.add_argument("--salida", default="tablero_validacion.html")
    ap.add_argument("--merge", help="Modelo JSON existente al que se le AÑADE esta empresa")
    ap.add_argument("--solo-cliente", action="store_true", help="No incluir la empresa de ejemplo")
    ap.add_argument("--dump-json")
    args = ap.parse_args()

    if args.modelo:
        modelo = json.loads(Path(args.modelo).read_text(encoding="utf-8"))
    else:
        if args.merge:
            modelo = json.loads(Path(args.merge).read_text(encoding="utf-8"))
            modelo.setdefault("empresas", [])
        else:
            modelo = {"generado": datetime.date.today().isoformat(), "departamentos": DEPARTAMENTOS,
                      "columnas": COLUMNAS, "empresas": []}
        if args.informe:
            ucs = extraer_ucs(leer_informe(args.informe))
            if not ucs:
                sys.exit("No detecté casos de uso (### UC-XX) en el informe.")
            emp = construir_empresa_desde_informe(ucs, args.cliente, args.sector)
            # reemplaza si ya existe una empresa con ese id
            modelo["empresas"] = [e for e in modelo["empresas"] if e["id"] != emp["id"]] + [emp]
            por_area = {}
            for tk in emp["tareas"]:
                por_area[tk["dep"]] = por_area.get(tk["dep"], 0) + 1
            print(f"{args.cliente}: {len(ucs)} UC -> áreas " + ", ".join(f"{k}:{v}" for k, v in por_area.items()))
        elif not args.merge:
            sys.exit("Indica --informe, --modelo o --merge.")
        # empresa de ejemplo (a menos que se excluya o ya esté)
        if not args.solo_cliente and not any(e["id"] == "aurora-retail" for e in modelo["empresas"]):
            modelo["empresas"].append(empresa_ejemplo())

    if args.dump_json:
        Path(args.dump_json).write_text(json.dumps(modelo, ensure_ascii=False, indent=2), encoding="utf-8")
        print("Modelo en", args.dump_json)
    print("Tablero en", render(modelo, args.salida))


if __name__ == "__main__":
    main()
