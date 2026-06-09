#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_y_publicar.py — Genera el mockup interactivo de una propuesta Y lo publica
automático a GitHub (si la carpeta sitio es un repo Git conectado a Cloudflare Pages).

Uso:
  python3 generar_y_publicar.py \
      --informe /ruta/informe.md \
      --cliente "DVR Ingeniería" \
      --sitio ~/propuestas_neuroagentes

Resultado: el mockup se genera, se copia a sitio/<cliente>/index.html, y se publica
a GitHub con un git push. Cloudflare auto-despliega en ~1 minuto.
"""
import argparse, subprocess, sys, tempfile
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(
        description="Genera mockup + publica automático a GitHub."
    )
    ap.add_argument("--informe", required=True, help="Informe MD para generar el mockup")
    ap.add_argument("--cliente", required=True, help="Nombre del cliente")
    ap.add_argument("--sitio", required=True, help="Carpeta del repo Git donde se publica")
    ap.add_argument("--sector", default="", help="Sector/industria del cliente (opcional)")
    a = ap.parse_args()

    informe = Path(a.informe).expanduser()
    if not informe.exists():
        sys.exit(f"✗ No existe el informe: {informe}")

    sitio = Path(a.sitio).expanduser()
    if not sitio.exists():
        sys.exit(f"✗ No existe la carpeta sitio: {sitio}")

    # PASO 1: Generar mockup en un archivo temporal
    print("📊 Generando mockup...")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as tmp:
        tmp_file = tmp.name

    try:
        cmd_gen = [
            "python3", "scripts/generar_tablero.py",
            f"--informe={informe}",
            f"--cliente={a.cliente}",
            f"--salida={tmp_file}",
        ]
        if a.sector:
            cmd_gen.append(f"--sector={a.sector}")
        subprocess.run(cmd_gen, check=True, cwd=informe.parent)
        print(f"✓ Mockup generado en {tmp_file}")
    except subprocess.CalledProcessError as e:
        sys.exit(f"✗ Error al generar mockup: {e}")

    # PASO 2: Publicar (copia a sitio + git push)
    print("🚀 Publicando a GitHub...")
    try:
        cmd_pub = [
            "python3", "scripts/publicar_cloudflare.py",
            f"--archivo={tmp_file}",
            f"--cliente={a.cliente}",
            f"--sitio={sitio}",
            "--proyecto=propuestas-neuroagentes",  # Ajusta si usas otro nombre
        ]
        subprocess.run(cmd_pub, check=True)
        print(f"\n✅ Listo. La propuesta de «{a.cliente}» está en línea.")
        print(f"   URL: https://propuestas-neuroagentes.pages.dev/{a.cliente.lower().replace(' ', '-')}/")
    except subprocess.CalledProcessError as e:
        sys.exit(f"✗ Error al publicar: {e}")
    finally:
        Path(tmp_file).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
