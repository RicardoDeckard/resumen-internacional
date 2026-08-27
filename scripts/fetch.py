"""
Trae artículos recientes de cada fuente, probando RSS -> scraping -> búsqueda.
No usa la API de Claude en este paso (eso ahorra costo: solo texto ya
filtrado llega al modelo, en summarize.py).
"""
import re
import time
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}
TIMEOUT = 15

# Reconoce entidades XML válidas para no tocarlas al sanear (&amp; &lt; &gt;
# &quot; &apos; &#123; &#x1F;), y escapa cualquier otro "&" suelto que
# aparezca en el feed (causa muy común de "not well-formed" en RSS reales,
# sobre todo en Substack).
_BARE_AMPERSAND = re.compile(r"&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)")


def _sanitize_xml(raw_text):
    return _BARE_AMPERSAND.sub("&amp;", raw_text)


def _recent_enough(published_struct, hours=48):
    if not published_struct:
        return True  # si no hay fecha, no descartamos por esto (se filtra después)
    dt = datetime(*published_struct[:6], tzinfo=timezone.utc)
    return dt > datetime.now(timezone.utc) - timedelta(hours=hours)


def try_rss(source, window_hours):
    if not source.get("rss"):
        return None, "sin RSS configurado"
    try:
        feed = feedparser.parse(source["rss"], request_headers=HEADERS)
        if feed.bozo and not feed.entries:
            # Reintento: traer el texto crudo, sanear ampersands sueltos
            # (típico en feeds de Substack) y volver a parsear desde texto.
            try:
                resp = requests.get(source["rss"], headers=HEADERS, timeout=TIMEOUT)
                sanitized = _sanitize_xml(resp.text)
                feed = feedparser.parse(sanitized)
            except Exception:
                pass
            if feed.bozo and not feed.entries:
                return None, f"RSS inválido: {feed.bozo_exception}"
        items = []
        for e in feed.entries[:15]:
            published = getattr(e, "published_parsed", None)
            if source.get("no_window") or _recent_enough(published, window_hours):
                items.append({
                    "title": e.get("title", "").strip(),
                    "link": e.get("link", "").strip(),
                    "summary": BeautifulSoup(e.get("summary", ""), "html.parser").get_text()[:600],
                    "published": time.strftime("%Y-%m-%d", published) if published else None,
                })
        if items:
            return items, "rss"
        return None, "RSS accesible pero sin entradas dentro de ventana"
    except Exception as ex:
        return None, f"error RSS: {ex}"


def try_scrape(source):
    url = source.get("scrape_url")
    selector = source.get("scrape_selector")
    if not url or not selector:
        return None, "sin scraping configurado"
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if r.status_code != 200:
            return None, f"scrape HTTP {r.status_code}"
        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.select(selector)[:10]
        items = []
        for a in links:
            href = a.get("href", "")
            if href and not href.startswith("http"):
                from urllib.parse import urljoin
                href = urljoin(url, href)
            title = a.get_text(strip=True)
            if title and href:
                items.append({"title": title, "link": href, "summary": "", "published": None})
        if items:
            return items, "scraping"
        return None, "scraping sin resultados con el selector configurado"
    except Exception as ex:
        return None, f"error scraping: {ex}"


def try_search(source):
    query = source.get("search_query")
    if not query:
        return None, "sin query de búsqueda configurada"
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=8, timelimit="w"))
        items = [{"title": r["title"], "link": r["href"], "summary": r.get("body", "")[:600],
                  "published": None} for r in results]
        if items:
            return items, "búsqueda (respaldo)"
        return None, "búsqueda sin resultados"
    except Exception as ex:
        return None, f"error búsqueda: {ex}"


def fetch_source(source, window_hours=48):
    """
    Devuelve (items, metodo_usado, log_de_intentos).
    metodo_usado es None solo si los 3 métodos fallaron -> fuente realmente rota.

    Si la fuente define window_hours propio (think tanks que no publican a
    diario), ese valor tiene prioridad sobre el global.
    """
    window_hours = source.get("window_hours", window_hours)
    log = []
    items, reason = try_rss(source, window_hours)
    log.append(f"RSS: {reason if items is None else 'OK'}")
    if items:
        return items, "rss", log

    items, reason = try_scrape(source)
    log.append(f"Scraping: {reason if items is None else 'OK'}")
    if items:
        return items, "scraping", log

    items, reason = try_search(source)
    log.append(f"Búsqueda: {reason if items is None else 'OK'}")
    if items:
        return items, "búsqueda", log

    return [], None, log


def fetch_all(sources, window_hours=48):
    results = {}
    for s in sources:
        items, method, log = fetch_source(s, window_hours)
        results[s["name"]] = {"items": items, "method": method, "log": log, "source": s}
    return results
