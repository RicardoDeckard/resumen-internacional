"""
Orquestador de RESUMEN INTERNACIONAL.

Uso: python main.py [--incluir-analistas]

--incluir-analistas fuerza el chequeo de las fuentes-analista de cadencia
semanal (Mearsheimer, Macgregor, Reisner) aunque no sea el día que toca.
El workflow de GitHub Actions ya decide esto automáticamente los lunes.
"""
import sys
import os
import datetime
import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

sys.path.insert(0, os.path.dirname(__file__))
from sources import SOURCES
from fetch import fetch_all
from summarize import summarize

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")


def main():
    incluir_analistas = "--incluir-analistas" in sys.argv or datetime.date.today().weekday() == 0  # lunes

    activas = [
        s for s in SOURCES
        if s["tier"] == "diario" or (s["tier"] == "semanal" and incluir_analistas)
    ]
    print(f"Corriendo {len(activas)} fuentes "
          f"({'incluye' if incluir_analistas else 'sin'} analistas personales)...")

    resultados = fetch_all(activas, window_hours=48)

    estado_fuentes = []
    for name, data in resultados.items():
        if data["method"]:
            estado, clase = f"Cubierta ({data['method']})", "estado-cubierta"
        else:
            estado, clase = "No disponible — los 3 métodos fallaron", "estado-no"
        estado_fuentes.append({
            "nombre": name,
            "metodo": data["method"],
            "estado": estado,
            "clase": clase,
            "log": data["log"],
        })

    print("Resumiendo con Claude (1 llamada)...")
    resultado_modelo = summarize(resultados)

    fecha = datetime.date.today().strftime("%d de %B de %Y")

    env = Environment(loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")))
    template = env.get_template("report.html")
    html_out = template.render(
        fecha=fecha,
        secciones=resultado_modelo["secciones"],
        estado_fuentes=estado_fuentes,
    )

    os.makedirs(DOCS_DIR, exist_ok=True)
    slug = datetime.date.today().isoformat()

    html_path = os.path.join(DOCS_DIR, f"resumen_{slug}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_out)

    pdf_path = os.path.join(DOCS_DIR, f"resumen_{slug}.pdf")
    HTML(string=html_out, base_url=BASE_DIR).write_pdf(pdf_path)

    # "último informe" siempre con el mismo nombre, para el link fijo
    with open(os.path.join(DOCS_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_out)
    HTML(string=html_out, base_url=BASE_DIR).write_pdf(os.path.join(DOCS_DIR, "ultimo.pdf"))

    # log de la corrida, útil para depurar fuentes rotas de verdad
    with open(os.path.join(DOCS_DIR, f"log_{slug}.json"), "w", encoding="utf-8") as f:
        json.dump(estado_fuentes, f, ensure_ascii=False, indent=2)

    print(f"Listo: {html_path}")
    print(f"Listo: {pdf_path}")


if __name__ == "__main__":
    main()
