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
        window_hours=168,
        tier="diario", group="analisis",
        rss="https://responsiblestatecraft.org/feed/",
        scrape_url="https://responsiblestatecraft.org/", scrape_selector="article a",
        search_query="site:responsiblestatecraft.org",
    ),
    dict(
        name="War on the Rocks",
        bias="Atlantista",
        window_hours=168,
        tier="diario", group="analisis",
        rss="https://warontherocks.com/feed/",
        scrape_url="https://warontherocks.com/", scrape_selector="h2.entry-title a",
        search_query="site:warontherocks.com",
    ),
    dict(
        name="RUSI",
        bias="Gubernamental — Reino Unido (cercano al MoD)",
        window_hours=168,
        tier="diario", group="analisis",
        rss="https://rusi.org/rss",
        scrape_url="https://rusi.org/explore-our-research/publications/commentary",
        scrape_selector="a.card__link",
        search_query="site:rusi.org commentary",
    ),
    dict(
        name="Chatham House",
        bias="Atlantista (UK)",
        window_hours=168,
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
        window_hours=168,
        tier="diario", group="analisis",
        rss="https://ecfr.eu/feed/",
        scrape_url="https://ecfr.eu/publications/", scrape_selector="a.article-card__link",
        search_query="site:ecfr.eu",
    ),
    dict(
        name="Arms Control Association",
        bias="Académico/independiente (nuclear)",
        window_hours=168,
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
    dict(
        name="The Defence Horizon Journal (TDHJ, red Clausewitz)",
        bias="Académico/independiente (defensa)",
        window_hours=168, tier="diario", group="analisis",
        rss="https://tdhj.org/feed/", scrape_url="https://tdhj.org/",
        scrape_selector="a", search_query="site:tdhj.org",
    ),

    # ---------- NIVEL 2 — SECUNDARIAS (a demanda) ----------
    dict(name="The Diplomat", bias="Atlantista", tier="diario", group="secundaria",
         rss="https://thediplomat.com/feed/", scrape_url="https://thediplomat.com/",
         scrape_selector="h3 a", search_query="site:thediplomat.com"),
    dict(name="RAND", bias="Industria militar / gubernamental EEUU", window_hours=168, tier="diario", group="secundaria",
         rss="https://www.rand.org/content/rand/blog.xml", scrape_url="https://www.rand.org/international_affairs.html",
         scrape_selector="a", search_query="site:rand.org"),
    dict(name="CSIS", bias="Atlantista/industria de defensa", window_hours=168, tier="diario", group="secundaria",
         rss="https://www.csis.org/analysis/rss.xml", scrape_url="https://www.csis.org/analysis",
         scrape_selector="a.link--card", search_query="site:csis.org"),
    dict(name="Carnegie Endowment", bias="Atlantista (liberal-internacionalista)", window_hours=168, tier="diario", group="secundaria",
         rss="https://carnegieendowment.org/rss/solr/?fa=pubs", scrape_url="https://carnegieendowment.org/research/",
         scrape_selector="a", search_query="site:carnegieendowment.org"),
    dict(name="Foreign Affairs", bias="Atlantista (establishment)", window_hours=168, tier="diario", group="secundaria",
         rss="https://www.foreignaffairs.com/rss.xml", scrape_url="https://www.foreignaffairs.com/most-recent",
         scrape_selector="a", search_query="site:foreignaffairs.com"),
    dict(name="Atlantic Council", bias="Atlantista/OTAN", tier="diario", group="secundaria",
         rss="https://www.atlanticcouncil.org/blogs/new-atlanticist/feed/",
         scrape_url="https://www.atlanticcouncil.org/blogs/new-atlanticist/", scrape_selector="a.title-link",
         search_query="site:atlanticcouncil.org"),
    dict(name="HCSS", bias="Gubernamental — Países Bajos", window_hours=168, tier="diario", group="secundaria",
         rss="https://hcss.nl/feed/", scrape_url="https://hcss.nl/publications/", scrape_selector="a",
         search_query="site:hcss.nl"),
    dict(name="Bruegel", bias="Atlantista/UE (economía)", window_hours=168, tier="diario", group="secundaria",
         rss="https://www.bruegel.org/rss.xml", scrape_url="https://www.bruegel.org/latest",
         scrape_selector="a", search_query="site:bruegel.org"),
    dict(name="Valdai Club", bias="Estatal ruso (semi-oficial)", window_hours=168, tier="diario", group="secundaria",
         rss="https://valdaiclub.com/rss/", scrape_url="https://valdaiclub.com/a/highlights/",
         scrape_selector="a", search_query="site:valdaiclub.com"),
    dict(name="RIAC", bias="Estatal ruso (semi-oficial)", window_hours=168, tier="diario", group="secundaria",
         rss="https://russiancouncil.ru/en/rss/", scrape_url="https://russiancouncil.ru/en/analytics-and-comments/",
         scrape_selector="a", search_query="site:russiancouncil.ru"),
    dict(name="Xinhua", bias="Estatal chino", tier="diario", group="secundaria",
         rss="http://www.xinhuanet.com/english/rss/worldrss.xml",
         scrape_url="https://english.news.cn/world/index.htm", scrape_selector="a",
         search_query="site:news.cn world"),
    dict(name="Mehr News Agency", bias="Estatal iraní", tier="diario", group="secundaria",
         rss="https://en.mehrnews.com/rss", scrape_url="https://en.mehrnews.com/",
         scrape_selector="a.title-link", search_query="site:en.mehrnews.com"),
    dict(name="Al-Monitor", bias="Privado empresarial (enfoque MENA)", tier="diario", group="secundaria",
         rss="https://www.al-monitor.com/rss", scrape_url="https://www.al-monitor.com/originals",
         scrape_selector="a", search_query="site:al-monitor.com"),
    dict(name="Middle East Eye", bias="Privado empresarial (crítico Israel/Golfo)", tier="diario", group="secundaria",
         rss="https://www.middleeasteye.net/rss", scrape_url="https://www.middleeasteye.net/",
         scrape_selector="a", search_query="site:middleeasteye.net"),
    dict(name="Jerusalem Post", bias="Privado empresarial (Israel, derecha)", tier="diario", group="secundaria",
         rss="https://www.jpost.com/rss/rssfeedsfrontpage.aspx", scrape_url="https://www.jpost.com/middle-east",
         scrape_selector="a", search_query="site:jpost.com"),
    dict(name="Haaretz", bias="Privado empresarial (Israel, crítico del gobierno)", tier="diario", group="secundaria",
         rss=None, scrape_url="https://www.haaretz.com/middle-east-news",
         scrape_selector="a", search_query="site:haaretz.com"),
    dict(name="Bulletin of Atomic Scientists", bias="Académico/independiente (nuclear)", window_hours=168, tier="diario", group="secundaria",
         rss="https://thebulletin.org/feed/", scrape_url="https://thebulletin.org/",
         scrape_selector="a.c-card__link", search_query="site:thebulletin.org"),
    dict(name="CSET Georgetown", bias="Gubernamental/académico — EEUU (IA)", window_hours=168, tier="diario", group="secundaria",
         rss="https://cset.georgetown.edu/feed/", scrape_url="https://cset.georgetown.edu/publications/",
         scrape_selector="a", search_query="site:cset.georgetown.edu"),
    dict(name="SWP Berlin", bias="Gubernamental — Alemania", window_hours=168, tier="diario", group="secundaria",
         rss="https://www.swp-berlin.org/en/rss", scrape_url="https://www.swp-berlin.org/en/publications",
         scrape_selector="a", search_query="site:swp-berlin.org"),
    dict(name="IFRI", bias="Gubernamental/académico — Francia", window_hours=168, tier="diario", group="secundaria",
         rss=None, scrape_url="https://www.ifri.org/en/publications", scrape_selector="a",
         search_query="site:ifri.org"),
    dict(name="MP-IDSA", bias="Gubernamental — India", window_hours=168, tier="diario", group="secundaria",
         rss=None, scrape_url="https://www.idsa.in/publisher/issue-brief", scrape_selector="a",
         search_query="site:idsa.in"),
    dict(name="The New York Times (World)", bias="Atlantista/liberal-internacionalista", tier="diario", group="secundaria",
         rss="https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
         scrape_url="https://www.nytimes.com/section/world", scrape_selector="a",
         search_query="site:nytimes.com"),
    dict(name="The Washington Post (World)", bias="Atlantista/establishment EEUU", tier="diario", group="secundaria",
         rss="https://feeds.washingtonpost.com/rss/world", scrape_url="https://www.washingtonpost.com/world/",
         scrape_selector="a", search_query="site:washingtonpost.com"),
    dict(name="The Guardian (World)", bias="Atlantista/liberal", tier="diario", group="secundaria",
         rss="https://www.theguardian.com/world/rss", scrape_url="https://www.theguardian.com/world",
         scrape_selector="a", search_query="site:theguardian.com"),
    dict(name="Kyiv Independent", bias="Nacionalista — Ucrania (primaria local)", tier="diario", group="secundaria",
         rss="https://kyivindependent.com/feed/", scrape_url="https://kyivindependent.com/",
         scrape_selector="a", search_query="site:kyivindependent.com"),
    dict(name="Sputnik / RIA Novosti", bias="Estatal ruso (agencia oficial)", tier="diario", group="secundaria",
         rss="https://ria.ru/export/rss2/archive/index.xml", scrape_url="https://sputnikglobe.com/",
         scrape_selector="a", search_query="site:sputnikglobe.com"),

    # ---------- CURADURÍA: top-tier occidental que faltaba ----------
    dict(name="International Crisis Group", bias="Académico/independiente (referencia en prevención de conflictos)", window_hours=168,
         tier="diario", group="analisis",
         rss="https://www.crisisgroup.org/rss.xml", scrape_url="https://www.crisisgroup.org/latest-updates",
         scrape_selector="a", search_query="site:crisisgroup.org"),
    dict(name="Brookings Institution", bias="Atlantista (establishment, centrista)", window_hours=168, tier="diario", group="analisis",
         rss="https://www.brookings.edu/feed/", scrape_url="https://www.brookings.edu/research-commentary/",
         scrape_selector="a", search_query="site:brookings.edu"),
    dict(name="Council on Foreign Relations (CFR)", bias="Atlantista (establishment)", window_hours=168, tier="diario", group="analisis",
         rss="https://www.cfr.org/rss.xml", scrape_url="https://www.cfr.org/blogs",
         scrape_selector="a", search_query="site:cfr.org"),
    dict(name="Belfer Center (Harvard Kennedy School)", bias="Académico — EEUU", window_hours=168, tier="diario", group="analisis",
         rss="https://www.belfercenter.org/rss.xml", scrape_url="https://www.belfercenter.org/publications",
         scrape_selector="a", search_query="site:belfercenter.org"),
    dict(name="Lowy Institute", bias="Atlantista — Australia/Asia-Pacífico", window_hours=168, tier="diario", group="analisis",
         rss="https://www.lowyinstitute.org/rss.xml", scrape_url="https://www.lowyinstitute.org/the-interpreter",
         scrape_selector="a", search_query="site:lowyinstitute.org"),

    # ---------- CURADURÍA: equivalentes no occidentales / no atlantistas ----------
    dict(name="IISS (International Institute for Strategic Studies)",
         bias="Atlantista (Reino Unido, referencia en balance militar)", window_hours=168, tier="diario", group="analisis",
         rss="https://www.iiss.org/rss/", scrape_url="https://www.iiss.org/online-analysis/",
         scrape_selector="a", search_query="site:iiss.org"),
    dict(name="Center for China and Globalization (CCG)",
         bias="Gubernamental/estatal chino (semi-oficial, independencia disputada)", window_hours=168, tier="diario", group="analisis",
         rss="https://www.ccg.org.cn/?feed=rss2", scrape_url="https://www.ccg.org.cn/",
         scrape_selector="a", search_query="site:ccg.org.cn"),
    dict(name="Observer Research Foundation (ORF)", bias="Gubernamental/académico — India", window_hours=168, tier="diario", group="analisis",
         rss="https://www.orfonline.org/feed", scrape_url="https://www.orfonline.org/expert-speak/",
         scrape_selector="a", search_query="site:orfonline.org"),
    dict(name="Institute for Security Studies (ISS Africa)",
         bias="Académico/independiente — África (Sudáfrica)", window_hours=168, tier="diario", group="analisis",
         rss="https://issafrica.org/feed", scrape_url="https://issafrica.org/latest",
         scrape_selector="a", search_query="site:issafrica.org"),
]

# Ejes temáticos y regla de relevancia estratégica, usados en el prompt de resumen.
EJES = [
    "Ucrania", "Irán", "Medio Oriente-Israel-Gaza-Siria-Líbano",
    "Taiwán-China", "OTAN-EEUU", "Armas nucleares", "IA geopolítica",
]
# Nota sobre el eje "Medio Oriente-Israel-Gaza-Siria-Líbano": incluye también
# a Turquía y a países árabes del Golfo cuando la nota trate sobre su relación
# con la región (p. ej. pactos de defensa, mediación, Siria), aunque
# Turquía no sea técnicamente Medio Oriente. Los temas de Turquía puramente
# de OTAN (bases, ejercicios) van al eje OTAN-EEUU.

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
