"""
Una sola llamada a la API de Claude con todo el material ya recolectado.
Esto es lo que mantiene el costo bajo: el modelo no busca ni navega,
solo lee texto ya filtrado y lo redacta/agrupa.
"""
import os
import json
from anthropic import Anthropic
from sources import EJES, REGLA_RELEVANCIA, REGLA_ANTI_CITA

MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = f"""Sos el editor de "RESUMEN INTERNACIONAL", informe diario de relaciones
internacionales para Ricardo Narvaez, funcionario de una fiscalía federal argentina.

Ejes temáticos (en este orden de aparición): {", ".join(EJES)}, y otros ejes de
trascendencia comparable que surjan del material.

{REGLA_RELEVANCIA}

{REGLA_ANTI_CITA}

FORMATO DE SALIDA: JSON estricto, sin texto fuera del JSON, con esta forma exacta:
{{
  "secciones": [
    {{
      "eje": "Ucrania",
      "notas": [
        {{
          "titulo": "string",
          "url": "string",
          "medio": "string (nombre del medio o analista)",
          "sesgo": "string (etiqueta de sesgo, te la doy junto con cada fuente)",
          "resumen": "string, 1-3 párrafos objetivos, sin adoptar el framing de la fuente"
        }}
      ]
    }}
  ]
}}

Si una fuente es estatal o tiene alineamiento geopolítico declarado, el resumen debe
mantenerse descriptivo (qué dice la fuente) sin adoptar su marco como si fuera hecho
establecido. No agregues secciones vacías. No inventes notas: usá solo el material
que te paso a continuación."""


def build_user_content(fetch_results):
    """Arma el bloque de material crudo para el prompt, con la etiqueta de sesgo
    de cada fuente ya incluida (no depende de que el modelo la sepa de memoria)."""
    blocks = []
    for name, data in fetch_results.items():
        if not data["items"]:
            continue
        bias = data["source"]["bias"]
        lines = [f"### FUENTE: {name} | SESGO: {bias} | método de acceso: {data['method']}"]
        for it in data["items"]:
            lines.append(f"- Título: {it['title']}")
            lines.append(f"  URL: {it['link']}")
            if it.get("published"):
                lines.append(f"  Fecha: {it['published']}")
            if it.get("summary"):
                lines.append(f"  Extracto: {it['summary']}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def summarize(fetch_results):
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    user_content = build_user_content(fetch_results)

    message = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )
    if message.stop_reason == "max_tokens":
        raise RuntimeError(
            "La respuesta de Claude se cortó por límite de tokens (max_tokens=16000). "
            "Subir el valor de max_tokens en summarize.py."
        )
    raw = message.content[0].text.strip()
    # por si el modelo envuelve el JSON en ```json ... ```
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw
        if raw.lower().startswith("json"):
            raw = raw.split("\n", 1)[1]
    return json.loads(raw)
