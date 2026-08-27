"""
Lista de fuentes para RESUMEN INTERNACIONAL.

Cada fuente define hasta 3 métodos de acceso, probados en orden.
Solo se marca "rota" si los 3 fallan en la misma corrida.

  rss:          URL de feed RSS/Atom (método 1, preferido)
  scrape_url + scrape_selector: URL de portada/sección + selector CSS
                de los links a artículos (método 2)
  search_query: query de respaldo para búsqueda web (método 3, sin API key)

tier: "diario" (chequeo en cada corrida) | "semanal" (analistas personales,
      chequeados 1x por semana o a pedido)
group: "analisis" | "voz_oficial" | "secundaria"
"""

SOURCES = [
    # ---------- NIVEL 1 — ANÁLISIS (diario) ----------
    dict(
        name="Quincy Institute / Responsible Statecraft",
        bias="Realista/restraint",
        tier="diario", group="analisis",
        rss="https://responsiblestatecraft.org/feed/",
        scrape_url="https://responsiblestatecraft.org/", scrape_selector="article a",
        search_query="site:responsiblestatecraft.org",
    ),
    dict(
        name="War on the Rocks",
        bias="Atlantista",
        tier="diario", group="analisis",
        rss="https://warontherocks.com/feed/",
        scrape_url="https://warontherocks.com/", scrape_selector="h2.entry-title a",
        search_query="site:warontherocks.com",
    ),
    dict(
        name="RUSI",
        bias="Gubernamental — Reino Unido (cercano al MoD)",
        tier="diario", group="analisis",
        rss="https://rusi.org/rss",
        scrape_url="https://rusi.org/explore-our-research/publications/commentary",
        scrape_selector="a.card__link",
        search_query="site:rusi.org commentary",
    ),
    dict(
        name="Chatham House",
        bias="Atlantista (UK)",
        tier="diario", group="analisis",
        rss="https://www.chathamhouse.org/rss/all",
        scrape_url="https://www.chathamhouse.org/publications/the-world-today",
        scrape_selector="a.card__link",
        search_query="site:chathamhouse.org expert comment",
    ),
    dict(
        name="ISW (Institute for the Study of War)",
        bias="Atlantista (hawkish)",
        tier="diario", group="analisis",
        rss=None,
        scrape_url="https://www.understandingwar.org/backgrounder",
        scrape_selector="a.field-content",
        search_query='"Offensive Campaign Assessment" understandingwar.org',
    ),
    dict(
        name="ECFR",
        bias="Atlantista/UE",
        tier="diario", group="analisis",
        rss="https://ecfr.eu/feed/",
        scrape_url="https://ecfr.eu/publications/", scrape_selector="a.article-card__link",
        search_query="site:ecfr.eu",
    ),
    dict(
        name="Arms Control Association",
        bias="Académico/independiente (nuclear)",
        tier="diario", group="analisis",
        rss="https://www.armscontrol.org/rss.xml",
        scrape_url="https://www.armscontrol.org/issue-briefs", scrape_selector="a",
        search_query="site:armscontrol.org",
    ),

    # ---------- NIVEL 1 — VOZ OFICIAL DIRECTA (diario, alfabético) ----------
    dict(
        name="Al Jazeera",
        bias="Gubernamental — Qatar",
        tier="diario", group="voz_oficial",
        rss="https://www.aljazeera.com/xml/rss/all.xml",
        scrape_url="https://www.aljazeera.com/where/mena/", scrape_selector="a.u-clickable-card__link",
        search_query="site:aljazeera.com",
    ),
    dict(
        name="Global Times",
        bias="Estatal chino",
        tier="diario", group="voz_oficial",
        rss="https://www.globaltimes.cn/rss/outbrain.xml",
        scrape_url="https://www.globaltimes.cn/china/diplomacy/", scrape_selector="a",
        search_query="site:globaltimes.cn",
    ),
    dict(
        name="RT (Russia Today)",
        bias="Estatal ruso (internacional)",
        tier="diario", group="voz_oficial",
        rss="https://www.rt.com/rss/",
        scrape_url="https://www.rt.com/news/", scrape_selector="a.link",
        search_query="site:rt.com",
    ),
    dict(
        name="TASS",
        bias="Estatal ruso",
        tier="diario", group="voz_oficial",
        rss="https://tass.com/rss/v2.xml",
        scrape_url="https://tass.com/world", scrape_selector="a.tass_pkg_link",
        search_query="site:tass.com",
    ),
    dict(
        name="Times of Israel",
        bias="Privado empresarial (Israel)",
        tier="diario", group="voz_oficial",
        rss="https://www.timesofisrael.com/feed/",
        scrape_url="https://www.timesofisrael.com/", scrape_selector="a.headline-link",
        search_query="site:timesofisrael.com",
    ),

    # ---------- ANALISTAS PERSONALES (semanal / a pedido) ----------
    dict(
        name="John Mearsheimer (Substack propio)",
        bias="Realista/independiente",
        tier="semanal", group="analisis",
        rss="https://mearsheimer.substack.com/feed",
        scrape_url="https://mearsheimer.substack.com/archive", scrape_selector="a.post-preview-title",
        search_query="site:mearsheimer.substack.com",
        no_window=True,
    ),
    dict(
        name="Douglas Macgregor (Substack propio)",
        bias="Realista/restraint",
        tier="semanal", group="analisis",
        rss="https://coloneldoug.substack.com/feed",
        scrape_url="https://coloneldoug.substack.com/archive", scrape_selector="a.post-preview-title",
        search_query="site:coloneldoug.substack.com",
        no_window=True,
    ),
    dict(
        name="Cnel. Markus Reisner (TRUPPENDIENST / Clausewitz Network)",
        bias="Gubernamental — Austria (Bundesheer)",
        tier="semanal", group="analisis",
        rss=None,
        scrape_url="https://www.bundesheer.at/truppendienst/", scrape_selector="a",
        search_query='Reisner Bundesheer Ukraine Analyse truppendienst.bundesheer.at',
        no_window=True,
        video_fallback="Ukraine aktuell (YouTube) — solo título+fecha+link si no hay texto",
    ),

    # ---------- NIVEL 2 — SECUNDARIAS (a demanda) ----------
    dict(name="The Diplomat", bias="Atlantista", tier="secundaria", group="secundaria",
         rss="https://thediplomat.com/feed/", scrape_url="https://thediplomat.com/",
         scrape_selector="h3 a", search_query="site:thediplomat.com"),
    dict(name="RAND", bias="Industria militar / gubernamental EEUU", tier="secundaria", group="secundaria",
         rss="https://www.rand.org/content/rand/blog.xml", scrape_url="https://www.rand.org/international_affairs.html",
         scrape_selector="a", search_query="site:rand.org"),
    dict(name="CSIS", bias="Atlantista/industria de defensa", tier="secundaria", group="secundaria",
         rss="https://www.csis.org/analysis/rss.xml", scrape_url="https://www.csis.org/analysis",
         scrape_selector="a.link--card", search_query="site:csis.org"),
    dict(name="Carnegie Endowment", bias="Atlantista (liberal-internacionalista)", tier="secundaria", group="secundaria",
         rss="https://carnegieendowment.org/rss/solr/?fa=pubs", scrape_url="https://carnegieendowment.org/research/",
         scrape_selector="a", search_query="site:carnegieendowment.org"),
    dict(name="Foreign Affairs", bias="Atlantista (establishment)", tier="secundaria", group="secundaria",
         rss="https://www.foreignaffairs.com/rss.xml", scrape_url="https://www.foreignaffairs.com/most-recent",
         scrape_selector="a", search_query="site:foreignaffairs.com"),
    dict(name="Atlantic Council", bias="Atlantista/OTAN", tier="secundaria", group="secundaria",
         rss="https://www.atlanticcouncil.org/blogs/new-atlanticist/feed/",
         scrape_url="https://www.atlanticcouncil.org/blogs/new-atlanticist/", scrape_selector="a.title-link",
         search_query="site:atlanticcouncil.org"),
    dict(name="HCSS", bias="Gubernamental — Países Bajos", tier="secundaria", group="secundaria",
         rss="https://hcss.nl/feed/", scrape_url="https://hcss.nl/publications/", scrape_selector="a",
         search_query="site:hcss.nl"),
    dict(name="Bruegel", bias="Atlantista/UE (economía)", tier="secundaria", group="secundaria",
         rss="https://www.bruegel.org/rss.xml", scrape_url="https://www.bruegel.org/latest",
         scrape_selector="a", search_query="site:bruegel.org"),
    dict(name="Valdai Club", bias="Estatal ruso (semi-oficial)", tier="secundaria", group="secundaria",
         rss="https://valdaiclub.com/rss/", scrape_url="https://valdaiclub.com/a/highlights/",
         scrape_selector="a", search_query="site:valdaiclub.com"),
    dict(name="RIAC", bias="Estatal ruso (semi-oficial)", tier="secundaria", group="secundaria",
         rss="https://russiancouncil.ru/en/rss/", scrape_url="https://russiancouncil.ru/en/analytics-and-comments/",
         scrape_selector="a", search_query="site:russiancouncil.ru"),
    dict(name="Xinhua", bias="Estatal chino", tier="secundaria", group="secundaria",
         rss="http://www.xinhuanet.com/english/rss/worldrss.xml",
         scrape_url="https://english.news.cn/world/index.htm", scrape_selector="a",
         search_query="site:news.cn world"),
    dict(name="Mehr News Agency", bias="Estatal iraní", tier="secundaria", group="secundaria",
         rss="https://en.mehrnews.com/rss", scrape_url="https://en.mehrnews.com/",
         scrape_selector="a.title-link", search_query="site:en.mehrnews.com"),
    dict(name="Al-Monitor", bias="Privado empresarial (enfoque MENA)", tier="secundaria", group="secundaria",
         rss="https://www.al-monitor.com/rss", scrape_url="https://www.al-monitor.com/originals",
         scrape_selector="a", search_query="site:al-monitor.com"),
    dict(name="Middle East Eye", bias="Privado empresarial (crítico Israel/Golfo)", tier="secundaria", group="secundaria",
         rss="https://www.middleeasteye.net/rss", scrape_url="https://www.middleeasteye.net/",
         scrape_selector="a", search_query="site:middleeasteye.net"),
    dict(name="Jerusalem Post", bias="Privado empresarial (Israel, derecha)", tier="secundaria", group="secundaria",
         rss="https://www.jpost.com/rss/rssfeedsfrontpage.aspx", scrape_url="https://www.jpost.com/middle-east",
         scrape_selector="a", search_query="site:jpost.com"),
    dict(name="Haaretz", bias="Privado empresarial (Israel, crítico del gobierno)", tier="secundaria", group="secundaria",
         rss=None, scrape_url="https://www.haaretz.com/middle-east-news",
         scrape_selector="a", search_query="site:haaretz.com"),
    dict(name="Bulletin of Atomic Scientists", bias="Académico/independiente (nuclear)", tier="secundaria", group="secundaria",
         rss="https://thebulletin.org/feed/", scrape_url="https://thebulletin.org/",
         scrape_selector="a.c-card__link", search_query="site:thebulletin.org"),
    dict(name="CSET Georgetown", bias="Gubernamental/académico — EEUU (IA)", tier="secundaria", group="secundaria",
         rss="https://cset.georgetown.edu/feed/", scrape_url="https://cset.georgetown.edu/publications/",
         scrape_selector="a", search_query="site:cset.georgetown.edu"),
    dict(name="SWP Berlin", bias="Gubernamental — Alemania", tier="secundaria", group="secundaria",
         rss="https://www.swp-berlin.org/en/rss", scrape_url="https://www.swp-berlin.org/en/publications",
         scrape_selector="a", search_query="site:swp-berlin.org"),
    dict(name="IFRI", bias="Gubernamental/académico — Francia", tier="secundaria", group="secundaria",
         rss=None, scrape_url="https://www.ifri.org/en/publications", scrape_selector="a",
         search_query="site:ifri.org"),
    dict(name="MP-IDSA", bias="Gubernamental — India", tier="secundaria", group="secundaria",
         rss=None, scrape_url="https://www.idsa.in/publisher/issue-brief", scrape_selector="a",
         search_query="site:idsa.in"),
    dict(name="The New York Times (World)", bias="Atlantista/liberal-internacionalista", tier="secundaria", group="secundaria",
         rss="https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
         scrape_url="https://www.nytimes.com/section/world", scrape_selector="a",
         search_query="site:nytimes.com"),
    dict(name="The Washington Post (World)", bias="Atlantista/establishment EEUU", tier="secundaria", group="secundaria",
         rss="https://feeds.washingtonpost.com/rss/world", scrape_url="https://www.washingtonpost.com/world/",
         scrape_selector="a", search_query="site:washingtonpost.com"),
    dict(name="The Guardian (World)", bias="Atlantista/liberal", tier="secundaria", group="secundaria",
         rss="https://www.theguardian.com/world/rss", scrape_url="https://www.theguardian.com/world",
         scrape_selector="a", search_query="site:theguardian.com"),
    dict(name="Kyiv Independent", bias="Nacionalista — Ucrania (primaria local)", tier="secundaria", group="secundaria",
         rss="https://kyivindependent.com/feed/", scrape_url="https://kyivindependent.com/",
         scrape_selector="a", search_query="site:kyivindependent.com"),
    dict(name="Meduza", bias="Independiente ruso en exilio", tier="secundaria", group="secundaria",
         rss="https://meduza.io/rss/en/all", scrape_url="https://meduza.io/en/",
         scrape_selector="a", search_query="site:meduza.io"),
    dict(name="Sputnik / RIA Novosti", bias="Estatal ruso (agencia oficial)", tier="secundaria", group="secundaria",
         rss="https://ria.ru/export/rss2/archive/index.xml", scrape_url="https://sputnikglobe.com/",
         scrape_selector="a", search_query="site:sputnikglobe.com"),
]

# Ejes temáticos y regla de relevancia estratégica, usados en el prompt de resumen.
EJES = [
    "Ucrania", "Gaza / Medio Oriente (incluye Líbano)", "Irán",
    "Taiwán-China", "OTAN-EEUU", "Armas nucleares", "IA geopolítica",
]

REGLA_RELEVANCIA = """
Incluir una nota solo si cumple AL MENOS UNO de estos criterios:
1. Cambio de control territorial (toma/pérdida de una localidad, avance o repliegue de frente)
2. Disponibilidad o escasez de un medio militar clave (stock de misiles, municiones, drones, defensa aérea)
3. Transferencia de armamento o acuerdo de suministro de volumen/impacto significativo
4. Alianza o acuerdo estratégico que afecta la capacidad de sostener el conflicto
5. Bajas o pérdidas de escala relevante que revelen eficacia de un arma, una maniobra, o ritmo de desgaste
6. Capacidades no cinéticas: guerra electrónica, guerra cognitiva/informativa, ciberguerra, satélites/ISR, IA aplicada al conflicto
7. Decisión política/diplomática que altera la trayectoria del conflicto
8. Señal real de escalada o desescalada (umbral cruzado, amenaza creíble, cambio doctrinario)

Test: ¿esto cambia la lectura de un observador experto sobre cómo va el conflicto, qué recursos
tiene cada bando, o hacia dónde va políticamente? Si no, se omite aunque tenga alto impacto humano.
"""

REGLA_ANTI_CITA = """
Si una fuente solo replica, resume o cita textualmente lo publicado por otra fuente
(incluye despachos de agencia reempaquetados por diarios generalistas), no se incluye esa nota.
"""
