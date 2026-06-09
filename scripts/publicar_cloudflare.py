#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
publicar_cloudflare.py — Publica una propuesta (el HTML que genera la skill) en
Cloudflare Pages.

Modelo: UN solo proyecto de Pages con una CARPETA POR CLIENTE. Mantiene un
"sitio" local que ACUMULA todas las propuestas y lo despliega completo, así
ninguna propuesta anterior se borra. Cada cliente queda en:
    https://<proyecto>.pages.dev/<cliente>/      (o tu dominio propio)

Uso:
  python3 publicar_cloudflare.py \
      --archivo /ruta/propuesta.html \
      --cliente "DVR Ingeniería" \
      --sitio ~/propuestas_neuroagentes \
      --proyecto propuestas [--branch main] [--dry-run]

Autenticación (elige una):
  - Interactiva:  corre antes  `npx wrangler login`  (abre el navegador, una vez).
  - No interactiva (automatización): exporta dos variables de entorno
        export CLOUDFLARE_API_TOKEN=...      (token con permiso "Cloudflare Pages — Edit")
        export CLOUDFLARE_ACCOUNT_ID=...     (ID de tu cuenta de Cloudflare)
    El script NUNCA te pide ni guarda el token; solo lee esas variables si existen.

Requisitos: Node.js (incluye npx). Wrangler se descarga solo vía npx.

Nota de entorno: para que el DESPLIEGUE funcione, este proceso necesita acceso de
red a Cloudflare (api.cloudflare.com y *.cloudflare.com). Si corres la skill dentro
de un entorno con red restringida, usa --dry-run aquí y ejecuta el comando que
imprime en tu propia máquina (o habilita esos dominios en la red del entorno).
"""
import argparse, os, re, shutil, subprocess, sys, unicodedata, html
from pathlib import Path


def slug(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "cliente"


def _index_raiz(sitio: Path, proyecto: str):
    """Genera un index.html en la raíz del sitio con la lista de propuestas."""
    carpetas = sorted([d.name for d in sitio.iterdir()
                       if d.is_dir() and (d / "index.html").exists()])
    filas = "\n".join(
        f'<li><a href="./{html.escape(c)}/">{html.escape(c.replace("-", " ").title())}</a></li>'
        for c in carpetas) or "<li>(aún no hay propuestas)</li>"
    doc = f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Propuestas · NeuroAgentes</title>
<style>body{{font-family:Montserrat,system-ui,sans-serif;background:#0E1F1C;color:#fff;
margin:0;display:grid;place-items:center;min-height:100vh}}
.box{{background:#16302a;border-radius:16px;padding:34px 40px;max-width:560px;width:90%}}
h1{{color:#00FF7A;margin:0 0 6px;font-size:22px}}p{{color:#9fb3aa;margin:0 0 18px;font-size:13px}}
ul{{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px}}
a{{display:block;background:#0E1F1C;border:1px solid rgba(255,255,255,.1);border-radius:10px;
padding:12px 16px;color:#fff;text-decoration:none;font-weight:600;font-size:14px}}
a:hover{{border-color:#00FF7A;color:#00FF7A}}</style></head>
<body><div class="box"><h1>NeuroAgentes</h1><p>Propuestas y demos interactivas.</p>
<ul>{filas}</ul></div></body></html>"""
    (sitio / "index.html").write_text(doc, encoding="utf-8")


def _hay_wrangler():
    from shutil import which
    return which("npx") is not None or which("wrangler") is not None


def _git_push(sitio: Path):
    """Hace git add, commit, push si sitio es un repo Git."""
    if not (sitio / ".git").exists():
        return False
    import subprocess
    os.chdir(sitio)
    try:
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        msg = "Propuestas actualizadas"
        subprocess.run(["git", "commit", "-m", msg], check=True, capture_output=True)
        subprocess.run(["git", "push"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        sys.exit(f"✗ Git push falló. Revisa:\n  - ¿Tienes Git instalado? `git --version`\n  - ¿Estás autenticado en GitHub? `git config --global user.name`\n  - ¿Tienes internet?\nError: {e}")


def main():
    ap = argparse.ArgumentParser(description="Publica una propuesta en Cloudflare Pages.")
    ap.add_argument("--archivo", required=True, help="HTML generado por la skill")
    ap.add_argument("--cliente", required=True, help="Nombre del cliente (se convierte en carpeta)")
    ap.add_argument("--sitio", required=True, help="Carpeta local que acumula TODAS las propuestas")
    ap.add_argument("--proyecto", default="propuestas", help="Nombre del proyecto de Cloudflare Pages")
    ap.add_argument("--branch", default="main", help="Rama de producción del proyecto")
    ap.add_argument("--dry-run", action="store_true", help="Prepara y muestra el comando, sin desplegar")
    a = ap.parse_args()

    archivo = Path(a.archivo).expanduser()
    if not archivo.exists():
        sys.exit(f"✗ No existe el archivo: {archivo}")
    sitio = Path(a.sitio).expanduser()
    cli = slug(a.cliente)
    destino = sitio / cli
    destino.mkdir(parents=True, exist_ok=True)
    shutil.copy(archivo, destino / "index.html")
    _index_raiz(sitio, a.proyecto)

    print(f"✓ Propuesta de «{a.cliente}» lista en: {destino / 'index.html'}")
    print(f"  Quedará en: https://{a.proyecto}.pages.dev/{cli}/")
    print(f"  ({len([d for d in sitio.iterdir() if d.is_dir()])} propuesta(s) en el sitio)")

    # Auto-detectar: si hay .git, git push; si no, wrangler deploy
    if (sitio / ".git").exists():
        print("\n✓ Detectado repositorio Git. Haciendo commit y push...")
        if _git_push(sitio):
            print("✓ Pusheado a GitHub. Cloudflare auto-despliega en ~1 minuto.")
        return
    
    # Si no hay Git, usar wrangler deploy (backward compat)
    cmd = ["npx", "wrangler", "pages", "deploy", str(sitio),
           f"--project-name={a.proyecto}", f"--branch={a.branch}"]
    print("\nComando de despliegue:\n  " + " ".join(cmd))

    if a.dry_run:
        print("\n(dry-run: no se desplegó nada. Quita --dry-run para publicar de verdad.)")
        return
    if not _hay_wrangler():
        sys.exit("\n✗ No encontré npx/wrangler. Instala Node.js (trae npx) y reintenta, "
                 "o corre el comando de arriba en tu máquina.")
    try:
        subprocess.run(cmd, check=True, env=os.environ.copy())
        print("\n✓ Publicado en Cloudflare Pages.")
    except subprocess.CalledProcessError:
        sys.exit("\n✗ El despliegue falló. Revisa:\n"
                 "  1) Autenticación: corre `npx wrangler login`, o exporta "
                 "CLOUDFLARE_API_TOKEN y CLOUDFLARE_ACCOUNT_ID.\n"
                 "  2) Acceso de red a Cloudflare desde este entorno (api.cloudflare.com).\n"
                 "  Truco: puedes copiar el comando de arriba y correrlo en tu máquina.")


if __name__ == "__main__":
    main()
