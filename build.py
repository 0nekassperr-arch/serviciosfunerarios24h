# -*- coding: utf-8 -*-
"""
Generador estatico del sitio serviciosfunerarios24h.es
Produce todas las paginas HTML, sitemap.xml, robots.txt y CNAME
a partir de componentes compartidos (SEO, cabecera, footer, chat).
"""
import os, json, datetime
from content_blog import BLOG_POSTS

# ----------------------------------------------------------------------
# CONFIGURACION DE NEGOCIO  (NAP)  ->  ⚠ DATOS GENERICOS / PLACEHOLDER
# ----------------------------------------------------------------------
BASE_URL   = "https://serviciosfunerarios24h.es"
SITE_NAME  = "Servicios Funerarios 24h"
BRAND      = "serviciosfunerarios24h.es"
PHONE_DISP = "910 000 000"
PHONE_TEL  = "+34910000000"
WHATSAPP   = "+34600000000"          # ⚠ placeholder
EMAIL      = "info@serviciosfunerarios24h.es"
ADDR_STREET= "Calle de Ejemplo 1"    # ⚠ placeholder
ADDR_ZIP   = "28934"
ADDR_CITY  = "Móstoles"
ADDR_PROV  = "Madrid"
ADDR_CC    = "ES"
LEGAL_NAME = "[Razón social / Titular]"   # ⚠ placeholder
LEGAL_NIF  = "[NIF / CIF]"                # ⚠ placeholder
YEAR       = datetime.date.today().year

# Verificación de Google Search Console (método etiqueta HTML).
# Pega aquí SOLO el valor del content="..." que te da Search Console y ejecuta build.py.
GSC_VERIFICATION = ""

ZONES = [
    {"slug":"mostoles","name":"Móstoles","home_clone":True},
    {"slug":"alcorcon","name":"Alcorcón","home_clone":False,
     "hero_sub":"Atención funeraria 24 horas en Alcorcón, con trato cercano y presupuestos claros.",
     "landmarks":"el Hospital Universitario Fundación Alcorcón, el Tanatorio de Alcorcón y barrios como Parque Lisboa, San José de Valderas o Las Retamas",
     "intro":"En Alcorcón acompañamos a las familias en cualquier circunstancia, ya sea un fallecimiento en el domicilio, en el Hospital Universitario Fundación Alcorcón o en una residencia. Coordinamos cada detalle para que usted solo tenga que ocuparse de despedirse.",
     "extra":"Alcorcón es una ciudad con fuerte sentido de comunidad, y creemos que un servicio funerario debe estar a la altura: cercano, humano y sin sorpresas en el precio."},
    {"slug":"fuenlabrada","name":"Fuenlabrada","home_clone":False,
     "hero_sub":"Servicios funerarios 24 horas en Fuenlabrada, con acompañamiento humano y tarifas transparentes.",
     "landmarks":"el Hospital Universitario de Fuenlabrada, el Cementerio y Tanatorio municipal y zonas como Loranca, El Vivero o La Serna",
     "intro":"Atendemos a las familias de Fuenlabrada las 24 horas del día. Si el fallecimiento se produce en el Hospital Universitario de Fuenlabrada, en casa o en una residencia, coordinamos el traslado y todos los preparativos con rapidez y respeto.",
     "extra":"Fuenlabrada es uno de los municipios más jóvenes y dinámicos del sur de Madrid; ofrecemos un servicio moderno pero cálido, pensado para cada familia."},
    {"slug":"leganes","name":"Leganés","home_clone":False,
     "hero_sub":"Asistencia funeraria 24 horas en Leganés, con cercanía y precios sin sorpresas.",
     "landmarks":"el Hospital Severo Ochoa, el Tanatorio de Leganés y barrios como Zarzaquemada, Leganés Norte o San Nicasio",
     "intro":"En Leganés estamos disponibles a cualquier hora para orientarle y gestionar el servicio funerario que necesite. Trabajamos con especial cuidado en los fallecimientos en el Hospital Severo Ochoa, en domicilios y en residencias de la zona.",
     "extra":"Leganés combina historia y modernidad, y así entendemos nosotros el acompañamiento: respetando la tradición de cada familia con un servicio actual y transparente."},
    {"slug":"getafe","name":"Getafe","home_clone":False,
     "hero_sub":"Servicios funerarios 24 horas en Getafe, con trato humano y tarifas claras.",
     "landmarks":"el Hospital Universitario de Getafe, el Cementerio y Tanatorio municipal y barrios como Sector III, Las Margaritas o Getafe Norte",
     "intro":"Acompañamos a las familias de Getafe en todo momento. Ya sea un fallecimiento en el Hospital Universitario de Getafe, en el domicilio o en una residencia, coordinamos cada gestión para que todo se resuelva con serenidad.",
     "extra":"Getafe es una ciudad con arraigo y carácter; ofrecemos un servicio a su altura, cercano y sin costes ocultos."},
    {"slug":"arroyomolinos","name":"Arroyomolinos","home_clone":False,
     "hero_sub":"Atención funeraria 24 horas en Arroyomolinos, cercana y con precios transparentes.",
     "landmarks":"el centro urbano, las urbanizaciones residenciales de reciente construcción y su entorno familiar",
     "intro":"En Arroyomolinos ofrecemos un servicio funerario cercano las 24 horas. Coordinamos el traslado desde el domicilio, hospital o residencia y nos encargamos de todos los preparativos y trámites.",
     "extra":"Arroyomolinos ha crecido mucho en los últimos años; damos un servicio a medida de sus familias, con la calidez de lo local y la seriedad de un equipo profesional."},
]
ZONE_NAMES = [z["name"] for z in ZONES]

NAV = [
    ("Inicio", ""),
    ("Servicios", "servicios/"),
    ("Zonas", "zonas/"),
    ("Necesito ayuda", "necesito-ayuda/"),
    ("Blog", "blog/"),
    ("Contacto", "contacto/"),
]

OUT = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------
def prefix_for(route):
    depth = route.count("/")
    return "../" * depth

def L(prefix, target):
    """Enlace interno relativo."""
    h = prefix + target
    return h if h else "./"

FAVICON = ("data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
    "%3Crect width='64' height='64' rx='14' fill='%23faf7f1'/%3E"
    "%3Ctext x='32' y='44' font-size='40' text-anchor='middle' fill='%23c2a568'%3E%E2%9C%A6%3C/text%3E%3C/svg%3E")

def head(route, title, description, keywords, schema_blocks, og_image="assets/hero-serenidad.jpg", og_type="website"):
    prefix = prefix_for(route)
    canonical = BASE_URL + "/" + route
    img_abs = BASE_URL + "/" + og_image
    blocks = "\n".join(
        '  <script type="application/ld+json">\n%s\n  </script>' % json.dumps(b, ensure_ascii=False, indent=2)
        for b in schema_blocks
    )
    gsc = ('\n  <meta name="google-site-verification" content="%s" />' % GSC_VERIFICATION) if GSC_VERIFICATION else ""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="author" content="{BRAND}" />
  <meta name="theme-color" content="#c2a568" />{gsc}
  <link rel="canonical" href="{canonical}" />
  <link rel="icon" href="{prefix}favicon.ico" sizes="any" />
  <link rel="icon" type="image/png" sizes="32x32" href="{prefix}assets/favicon-32.png" />
  <link rel="apple-touch-icon" href="{prefix}assets/apple-touch-icon.png" />

  <!-- Open Graph -->
  <meta property="og:type" content="{og_type}" />
  <meta property="og:site_name" content="{SITE_NAME}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{img_abs}" />
  <meta property="og:locale" content="es_ES" />

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{description}" />
  <meta name="twitter:image" content="{img_abs}" />

  <link rel="stylesheet" href="{prefix}style.css" />
{blocks}
</head>
<body>
"""

def header(route):
    prefix = prefix_for(route)
    top = route.split("/")[0]
    links = []
    for label, target in NAV:
        active = " is-active" if (target.rstrip("/") == top) or (target=="" and route=="") else ""
        # zonas activo tambien en paginas de ciudad
        if target=="zonas/" and top in [z["slug"] for z in ZONES]:
            active = " is-active"
        links.append(f'<a class="nav-link{active}" href="{L(prefix,target)}">{label}</a>')
    links_html = "\n        ".join(links)
    return f"""  <header class="navbar" role="banner">
    <div class="container navbar__inner">
      <a class="brand" href="{L(prefix,'')}" aria-label="{BRAND} - inicio">
        <img class="brand__logo-img" src="{prefix}assets/logo-mark.png" alt="Servicios Funerarios 24h" width="48" height="48" />
        <span class="brand__text">
          <span class="brand__name">Servicios Funerarios 24h</span>
          <span class="brand__subtitle">Madrid Sur</span>
        </span>
      </a>
      <button class="nav-toggle" id="navToggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="navMenu">
        <span></span><span></span><span></span>
      </button>
      <nav class="nav-menu" id="navMenu" aria-label="Navegación principal">
        {links_html}
        <a class="navbar__phone" href="tel:{PHONE_TEL}" data-track="navbar-call" aria-label="Llamar al servicio 24 horas">
          <span aria-hidden="true">📞</span> {PHONE_DISP}
        </a>
      </nav>
    </div>
  </header>
"""

def footer(route):
    prefix = prefix_for(route)
    zonas_links = "\n            ".join(
        f'<a href="{L(prefix, z["slug"]+"/")}">{z["name"]}</a>' for z in ZONES
    )
    return f"""  <footer class="footer" role="contentinfo">
    <div class="container">
      <div class="footer__inner footer__inner--wide">
        <div class="footer__col">
          <img class="footer__logo" src="{L(prefix,'')}assets/logo-mark.png" alt="Servicios Funerarios 24h" width="70" height="70" onerror="this.style.display='none'" />
          <span class="brand__name">{BRAND}</span>
          <p class="footer__tag">Servicios funerarios 24 horas en Móstoles y todo el sur de Madrid. Atención inmediata, cercana y con precios transparentes.</p>
          <p class="footer__nap">
            <a href="tel:{PHONE_TEL}">📞 {PHONE_DISP}</a><br>
            <a href="mailto:{EMAIL}">✉ {EMAIL}</a><br>
            <span>📍 {ADDR_STREET}, {ADDR_ZIP} {ADDR_CITY} ({ADDR_PROV})</span>
          </p>
        </div>
        <div class="footer__col">
          <p class="footer__title">Servicios</p>
          <nav class="footer__nav" aria-label="Servicios">
            <a href="{L(prefix,'servicios/')}#incineracion">Incineración</a>
            <a href="{L(prefix,'servicios/')}#inhumacion">Inhumación</a>
            <a href="{L(prefix,'servicios/')}#traslados">Traslados</a>
            <a href="{L(prefix,'servicios/')}#tanatorio">Tanatorio y velatorio</a>
            <a href="{L(prefix,'servicios/')}#prevision">Previsión</a>
          </nav>
        </div>
        <div class="footer__col">
          <p class="footer__title">Zonas</p>
          <nav class="footer__nav" aria-label="Zonas">
            {zonas_links}
          </nav>
        </div>
        <div class="footer__col">
          <p class="footer__title">Enlaces</p>
          <nav class="footer__nav" aria-label="Enlaces">
            <a href="{L(prefix,'necesito-ayuda/')}">Necesito ayuda</a>
            <a href="{L(prefix,'blog/')}">Blog</a>
            <a href="{L(prefix,'contacto/')}">Contacto</a>
            <a href="{L(prefix,'contacto/')}#quienes-somos">Quiénes somos</a>
          </nav>
        </div>
        <div class="footer__col">
          <p class="footer__title">Legal</p>
          <nav class="footer__nav" aria-label="Enlaces legales">
            <a href="{L(prefix,'aviso-legal/')}">Aviso Legal</a>
            <a href="{L(prefix,'privacidad/')}">Política de Privacidad</a>
            <a href="{L(prefix,'cookies/')}">Política de Cookies</a>
          </nav>
        </div>
      </div>
      <p class="footer__bottom">© {YEAR} {BRAND} · Todos los derechos reservados.</p>
    </div>
  </footer>
"""

def chat_and_scripts(route):
    prefix = prefix_for(route)
    return f"""  <a class="sticky-call" href="tel:{PHONE_TEL}" data-track="sticky-call" aria-label="Llamar ahora, atención 24 horas">
    <span aria-hidden="true">📞</span> Llamar 24h · {PHONE_DISP}
  </a>

  <!-- ====== CHAT IA FLOTANTE (listo para conectar Gemma / Google AI Studio) ====== -->
  <button class="chat-fab" id="chatFab" aria-label="Abrir chat de ayuda" aria-expanded="false">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.5 8.5 0 0 1-12.3 7.6L3 21l1.9-5.7A8.5 8.5 0 1 1 21 11.5z"/></svg>
  </button>
  <section class="chat-panel" id="chatPanel" aria-live="polite" aria-label="Chat de ayuda">
    <div class="chat-header">
      <strong>Asistente de {SITE_NAME}</strong>
      <button class="chat-close" id="chatClose" aria-label="Cerrar chat">×</button>
    </div>
    <div class="chat-body" id="chatBody"></div>
    <form class="chat-input" id="chatForm">
      <input type="text" id="chatText" placeholder="Escriba su duda…" autocomplete="off" aria-label="Escriba su mensaje" />
      <button type="submit" aria-label="Enviar">➤</button>
    </form>
  </section>

  <script src="{prefix}script.js"></script>
</body>
</html>
"""

def page(route, title, description, keywords, body, schema_blocks, og_image="assets/hero-serenidad.jpg", og_type="website"):
    html = head(route, title, description, keywords, schema_blocks, og_image, og_type)
    html += header(route)
    html += '  <main id="contenido">\n' + body + '\n  </main>\n'
    html += footer(route)
    html += chat_and_scripts(route)
    d = os.path.join(OUT, route)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("  ->", route or "(home)")

# ----------------------------------------------------------------------
# SCHEMA COMUN
# ----------------------------------------------------------------------
def org_schema():
    return {
        "@context":"https://schema.org","@type":"FuneralHome",
        "@id": BASE_URL + "/#business",
        "name": SITE_NAME, "url": BASE_URL, "image": BASE_URL+"/assets/hero-serenidad.jpg",
        "logo": BASE_URL+"/assets/favicon-512.png",
        "telephone": PHONE_TEL, "email": EMAIL, "priceRange":"€€",
        "address":{"@type":"PostalAddress","streetAddress":ADDR_STREET,"postalCode":ADDR_ZIP,
                   "addressLocality":ADDR_CITY,"addressRegion":ADDR_PROV,"addressCountry":ADDR_CC},
        "areaServed":[{"@type":"City","name":n} for n in ZONE_NAMES],
        "openingHoursSpecification":[{"@type":"OpeningHoursSpecification",
            "dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
            "opens":"00:00","closes":"23:59"}],
        "sameAs":[]
    }

def website_schema():
    return {"@context":"https://schema.org","@type":"WebSite","name":SITE_NAME,
            "url":BASE_URL,"inLanguage":"es-ES"}

def breadcrumb(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":BASE_URL+"/"+u}
                           for i,(n,u) in enumerate(items)]}

def faq_schema(pairs):
    return {"@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[{"@type":"Question","name":q,
            "acceptedAnswer":{"@type":"Answer","text":a}} for q,a in pairs]}

# ----------------------------------------------------------------------
# COMPONENTES DE CONTENIDO REUTILIZABLES
# ----------------------------------------------------------------------
def crumbs_html(prefix, items):
    parts=[]
    for i,(n,u) in enumerate(items):
        if i==len(items)-1:
            parts.append(f'<span aria-current="page">{n}</span>')
        else:
            parts.append(f'<a href="{L(prefix,u)}">{n}</a>')
    return '<div class="breadcrumb"><div class="container">'+ " › ".join(parts) +'</div></div>'

def page_hero(title, subtitle, photo=True):
    cls = "page-hero page-hero--photo" if photo else "page-hero"
    return f'''<section class="{cls}">
      <div class="container">
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </div>
    </section>'''

def cta_band(prefix, text="¿Necesita ayuda ahora mismo?"):
    return f'''<section class="cta-band">
      <div class="container">
        <h2>{text}</h2>
        <p>Estamos disponibles 24 horas, todos los días del año. Le atendemos de inmediato.</p>
        <div class="cta-band__actions">
          <a class="btn btn--primary btn--xl" href="tel:{PHONE_TEL}" data-track="cta-call">📞 LLAMAR AHORA · {PHONE_DISP}</a>
        </div>
      </div>
    </section>'''

def lead_form(prefix, title="Solicite información sin compromiso", intro="Déjenos sus datos y le llamaremos en unos minutos para orientarle con calma."):
    return f'''<section class="form-section" id="formulario" aria-labelledby="form-title">
      <div class="container form-section__inner">
        <div class="form-intro">
          <span class="section__eyebrow" style="text-align:left">Sin compromiso</span>
          <h2 id="form-title" class="section__title" style="text-align:left">{title}</h2>
          <p class="section__subtitle" style="text-align:left;margin-left:0">{intro}</p>
          <ul class="form-intro__list">
            <li>✦ Respuesta rápida por teléfono o WhatsApp</li>
            <li>✦ Atención personalizada 24 horas</li>
            <li>✦ Sus datos tratados con total confidencialidad</li>
          </ul>
        </div>
        <form class="lead-form" id="leadForm" novalidate>
          <div class="field">
            <label for="tipoServicio">Tipo de servicio</label>
            <select id="tipoServicio" name="tipoServicio" required>
              <option value="" disabled selected>Seleccione una opción…</option>
              <option value="incineracion">Incineración</option>
              <option value="inhumacion">Inhumación (entierro)</option>
              <option value="traslado">Traslado a otra localidad</option>
              <option value="prevision">Previsión / Planificación</option>
              <option value="seguro">Consulta sobre seguro de decesos</option>
              <option value="otro">Otro / No estoy seguro</option>
            </select>
          </div>
          <div class="field">
            <label for="ubicacion">Ubicación / Localidad</label>
            <input type="text" id="ubicacion" name="ubicacion" placeholder="Ej.: Móstoles, domicilio, hospital…" autocomplete="off" required />
          </div>
          <fieldset class="field field--radio">
            <legend>¿Dispone de nicho o sepultura?</legend>
            <div class="radio-group">
              <label class="radio"><input type="radio" name="sepultura" value="si" required /><span>Sí, ya dispongo</span></label>
              <label class="radio"><input type="radio" name="sepultura" value="no" /><span>No, la necesito</span></label>
              <label class="radio"><input type="radio" name="sepultura" value="nolose" /><span>No lo sé</span></label>
            </div>
          </fieldset>
          <div class="field">
            <label for="nombre">Nombre completo</label>
            <input type="text" id="nombre" name="nombre" placeholder="Su nombre y apellidos" autocomplete="name" required />
          </div>
          <div class="field">
            <label for="telefono">Teléfono móvil <span class="req">*</span></label>
            <input type="tel" id="telefono" name="telefono" placeholder="6XX XXX XXX" autocomplete="tel" inputmode="tel" pattern="[0-9\\s+]{{9,15}}" required />
            <small class="field__hint">Le llamaremos o escribiremos por WhatsApp a este número.</small>
          </div>
          <label class="consent">
            <input type="checkbox" id="rgpd" name="rgpd" required />
            <span>He leído y acepto la <a href="{L(prefix,'privacidad/')}">Política de Privacidad</a> y <strong>autorizo el tratamiento de mis datos</strong> para gestionar mi solicitud y ser contactado.</span>
          </label>
          <button type="submit" class="btn btn--primary btn--block" data-track="form-submit">Solicitar información</button>
          <p class="lead-form__legal">Responsable: {BRAND}. Finalidad: atender su solicitud de información o servicio. Sus datos no se usarán para otros fines. Puede ejercer sus derechos según se indica en la Política de Privacidad.</p>
          <div class="form-success" id="formSuccess" role="status" aria-live="polite" hidden></div>
        </form>
      </div>
    </section>'''

def faq_block(title, pairs, alt=True):
    cls = "section section--alt" if alt else "section"
    items = "\n          ".join(
        f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in pairs)
    return f'''<section class="{cls}" aria-labelledby="faq-title">
      <div class="container">
        <span class="section__eyebrow">Preguntas frecuentes</span>
        <h2 id="faq-title" class="section__title">{title}</h2>
        <div class="faq" style="margin-top:26px">
          {items}
        </div>
      </div>
    </section>'''

# ----------------------------------------------------------------------
# HOME BODY (diseño base, sin el bloque disclaimer)  -  {P}=prefix
# ----------------------------------------------------------------------
HOME_BODY = r'''
    <!-- ============ HERO ============ -->
    <section class="hero hero--center" aria-labelledby="hero-title">
      <div class="container">
        <p class="hero__badge">Atención 24 horas · Móstoles y sur de Madrid</p>
        <h1 id="hero-title" class="hero__title">
          Funeraria 24h en Madrid sur.
        </h1>
        <p class="hero__subtitle">
          Le orientamos con calma y sin compromiso
        </p>
        <div class="hero__actions">
          <a class="btn btn--primary btn--xl" href="tel:+34910000000" data-track="hero-call">
            📞 LLAMAR AHORA · 24h
          </a>
          <a class="btn btn--offer" href="#formulario" data-track="hero-cremacion">
            Cremación por 1.500€
            <small>Presupuesto sin compromiso</small>
          </a>
        </div>
        <ul class="hero__trust" aria-label="Garantías del servicio">
          <li>✦ Atención inmediata</li>
          <li>✦ Trato cercano y respetuoso</li>
          <li>✦ Funeraria de confianza</li>
        </ul>
      </div>
    </section>

    <!-- ============ BLOQUE 24H ============ -->
    <section class="urgency urgency--photo" aria-labelledby="urgency-title">
      <div class="container urgency__inner">
        <p class="urgency__flag">Asistencia inmediata 24 horas</p>
        <h2 id="urgency-title" class="urgency__title">¿Ha fallecido un ser querido?</h2>
        <p class="urgency__text">
          Sabemos lo difícil que es este momento. Un asesor le atenderá de inmediato, le orientará
          con calma sobre los primeros pasos y coordinará el contacto con la funeraria.
          Estamos disponibles a cualquier hora, todos los días del año.
        </p>
        <a class="btn-call" href="tel:+34910000000" data-track="urgency-call" aria-label="Llamar ahora, línea 24 horas">
          <span class="btn-call__icon" aria-hidden="true">📞</span>
          <span class="btn-call__label">
            <strong>LLAMAR AHORA · 24H</strong>
            <small>910 000 000 — Le atendemos ya</small>
          </span>
        </a>
        <p class="urgency__note">Llamada de orientación gratuita · También le devolvemos la llamada si lo prefiere</p>
      </div>
    </section>

    <!-- ============ BENEFICIOS ============ -->
    <section class="section" aria-labelledby="benefits-title">
      <div class="container">
        <span class="section__eyebrow">Cómo le ayudamos</span>
        <h2 id="benefits-title" class="section__title">Orientación clara en un momento difícil</h2>
        <p class="section__subtitle">
          Trabajamos al sur de Madrid, de manera cercana y con tarifas transparentes.
        </p>
        <div class="grid-3">
          <article class="card">
            <div class="card__icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 1 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/></svg>
            </div>
            <h3 class="card__title">Acompañamiento humano</h3>
            <p class="card__text">
              Le escuchamos y le orientamos sin presión, con el respeto y la calma que este momento
              merece. Usted decide siempre.
            </p>
          </article>
          <article class="card">
            <div class="card__icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0l-7-7A2 2 0 0 1 3 12.2V4a1 1 0 0 1 1-1h8.2c.5 0 1 .2 1.4.6l7 7a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg>
            </div>
            <h3 class="card__title">Precios transparentes</h3>
            <p class="card__text">
              Le ayudamos a comparar presupuestos claros y desglosados de los servicios,
              para que elija con total tranquilidad.
            </p>
          </article>
          <article class="card">
            <div class="card__icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3h6a1 1 0 0 1 1 1v1h2a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h2V4a1 1 0 0 1 1-1z"/><path d="M9 12h6M9 16h4"/></svg>
            </div>
            <h3 class="card__title">Gestión de trámites</h3>
            <p class="card__text">
              La funeraria de confianza se encarga de certificados, licencias y gestiones legales.
              Le explicamos cada paso con claridad.
            </p>
          </article>
        </div>
      </div>
    </section>

    <!-- ============ IMAGEN + TEXTO ============ -->
    <section class="section section--alt" aria-labelledby="support-title">
      <div class="container media">
        <div class="media__img">
          <img src="{P}assets/apoyo-familiar.jpg" alt="Manos de dos personas sostenidas con delicadeza bajo luz natural cálida, transmitiendo apoyo y acompañamiento" loading="lazy" />
        </div>
        <div class="media__body">
          <span class="section__eyebrow" style="text-align:left">Nuestro compromiso</span>
          <h2 id="support-title">Siempre a su lado</h2>
          <p>
            Ofrecemos el mejor servicio sin gastos ocultos. Orientamos e informamos de manera
            transparente a las familias de los servicios funerarios disponibles en el sur de Madrid,
            ofreciendo un trato familiar.
          </p>
          <ul class="media__list">
            <li>Atención personalizada y sin compromiso</li>
            <li>Comparativa honesta de opciones y precios</li>
            <li>Especial atención a familias sin seguro de decesos</li>
            <li>Asesoramiento también en previsión y planificación</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- ============ ZONAS ============ -->
    <section class="section" aria-labelledby="zones-title">
      <div class="container">
        <span class="section__eyebrow">Dónde le atendemos</span>
        <h2 id="zones-title" class="section__title">Cobertura en el sur de Madrid</h2>
        <p class="section__subtitle">Servicios funerarios 24h en Móstoles y municipios cercanos.</p>
        <nav class="zones" aria-label="Zonas de cobertura">
          <a class="zone-chip" href="{P}mostoles/">Móstoles</a>
          <a class="zone-chip" href="{P}alcorcon/">Alcorcón</a>
          <a class="zone-chip" href="{P}fuenlabrada/">Fuenlabrada</a>
          <a class="zone-chip" href="{P}leganes/">Leganés</a>
          <a class="zone-chip" href="{P}getafe/">Getafe</a>
          <a class="zone-chip" href="{P}arroyomolinos/">Arroyomolinos</a>
        </nav>
        <p class="section__subtitle" style="margin-top:22px">
          <a href="{P}zonas/">Ver todas las zonas donde trabajamos →</a>
        </p>
      </div>
    </section>

    <!-- ============ FORMULARIO ============ -->
    <section class="form-section" id="formulario" aria-labelledby="form-title">
      <div class="container form-section__inner">
        <div class="form-intro">
          <span class="section__eyebrow" style="text-align:left">Sin compromiso</span>
          <h2 id="form-title" class="section__title" style="text-align:left">Solicite orientación o un presupuesto</h2>
          <p class="section__subtitle" style="text-align:left;margin-left:0">
            Para consultas de <strong>previsión</strong>, planificación o situaciones no urgentes.
            Déjenos sus datos y le contactaremos con calma para ayudarle.
          </p>
          <ul class="form-intro__list">
            <li>✦ Respuesta rápida por teléfono o WhatsApp</li>
            <li>✦ Orientación personalizada y gratuita</li>
            <li>✦ Sus datos tratados con total confidencialidad</li>
          </ul>
        </div>

        <form class="lead-form" id="leadForm" novalidate>
          <div class="field">
            <label for="tipoServicio">Tipo de servicio</label>
            <select id="tipoServicio" name="tipoServicio" required>
              <option value="" disabled selected>Seleccione una opción…</option>
              <option value="incineracion">Incineración</option>
              <option value="inhumacion">Inhumación (entierro)</option>
              <option value="traslado">Traslado a otra localidad</option>
              <option value="prevision">Previsión / Planificación</option>
              <option value="seguro">Consulta sobre seguro de decesos</option>
              <option value="otro">Otro / No estoy seguro</option>
            </select>
          </div>

          <div class="field">
            <label for="ubicacion">Ubicación / Localidad</label>
            <input type="text" id="ubicacion" name="ubicacion"
                   placeholder="Ej.: Móstoles, domicilio, hospital…" autocomplete="off" required />
          </div>

          <fieldset class="field field--radio">
            <legend>¿Dispone de nicho o sepultura?</legend>
            <div class="radio-group">
              <label class="radio"><input type="radio" name="sepultura" value="si" required /><span>Sí, ya dispongo</span></label>
              <label class="radio"><input type="radio" name="sepultura" value="no" /><span>No, la necesito</span></label>
              <label class="radio"><input type="radio" name="sepultura" value="nolose" /><span>No lo sé</span></label>
            </div>
          </fieldset>

          <div class="field">
            <label for="nombre">Nombre completo</label>
            <input type="text" id="nombre" name="nombre" placeholder="Su nombre y apellidos" autocomplete="name" required />
          </div>

          <div class="field">
            <label for="telefono">Teléfono móvil <span class="req">*</span></label>
            <input type="tel" id="telefono" name="telefono" placeholder="6XX XXX XXX"
                   autocomplete="tel" inputmode="tel" pattern="[0-9\s+]{9,15}" required />
            <small class="field__hint">Le llamaremos o escribiremos por WhatsApp a este número.</small>
          </div>

          <label class="consent">
            <input type="checkbox" id="rgpd" name="rgpd" required />
            <span>
              He leído y acepto la <a href="{P}privacidad/">Política de Privacidad</a> y
              <strong>autorizo expresamente el tratamiento de mis datos</strong> para
              poder contactarme y ofrecerle la información solicitada.
            </span>
          </label>

          <button type="submit" class="btn btn--primary btn--block" data-track="form-submit">
            Solicitar orientación
          </button>

          <p class="lead-form__legal">
            Responsable: serviciosfunerarios24h.es. Finalidad: gestionar su solicitud. Sus datos no
            se usarán para otros fines. Más información en la Política de Privacidad.
          </p>

          <div class="form-success" id="formSuccess" role="status" aria-live="polite" hidden></div>
        </form>
      </div>
    </section>

    <!-- ============ FAQ ============ -->
    <section class="section section--alt" aria-labelledby="faq-title">
      <div class="container">
        <span class="section__eyebrow">Preguntas frecuentes</span>
        <h2 id="faq-title" class="section__title">Resolvemos sus dudas</h2>
        <div class="faq" style="margin-top:26px">
          <details>
            <summary>¿Atienden las 24 horas?</summary>
            <p>Sí. Estamos disponibles las 24 horas del día, los 365 días del año. Ante un fallecimiento puede llamarnos en cualquier momento y le atenderemos de inmediato.</p>
          </details>
          <details>
            <summary>¿Cuánto cuesta un servicio funerario?</summary>
            <p>Depende del tipo de servicio y las prestaciones. Ofrecemos incineración desde 1.500 €, con presupuestos claros y desglosados, sin cargos ocultos.</p>
          </details>
          <details>
            <summary>¿Qué hago si acaba de fallecer un familiar?</summary>
            <p>Llámenos al 910 000 000 en cualquier momento. Le orientaremos con calma sobre los primeros pasos y coordinaremos todo de inmediato.</p>
          </details>
          <details>
            <summary>¿Trabajan con familias sin seguro de decesos?</summary>
            <p>Sí. Es una de nuestras especialidades. Le ayudamos a encontrar opciones adaptadas a su presupuesto y a conocer posibilidades de financiación.</p>
          </details>
        </div>
      </div>
    </section>
'''

def render_home_body(prefix):
    return HOME_BODY.replace("{P}", prefix)

print("Generando páginas…")

# ---- HOME ----
page("", 
     "Servicios Funerarios 24h en Móstoles y Madrid Sur | Cremación desde 1.500€",
     "Servicios funerarios 24 horas en Móstoles y el sur de Madrid. Atención inmediata ante un fallecimiento, incineración desde 1.500€, trámites incluidos y precios transparentes. Le atendemos ya.",
     "servicios funerarios 24h, funeraria Móstoles, funeraria Madrid sur, incineración Móstoles, precio funeral, tanatorio Madrid sur",
     render_home_body(""),
     [org_schema(), website_schema(),
      faq_schema([
        ("¿Atienden las 24 horas?","Sí, estamos disponibles las 24 horas del día, los 365 días del año."),
        ("¿Cuánto cuesta un servicio funerario?","Ofrecemos incineración desde 1.500 €, con presupuestos claros y sin cargos ocultos."),
        ("¿Qué hago si acaba de fallecer un familiar?","Llámenos al 910 000 000 en cualquier momento; le orientaremos y coordinaremos todo de inmediato."),
      ])])

# ---- resto de paginas se generan en build2 ----
if __name__ == "__main__":
    import build_pages  # genera servicios, zonas, ayuda, blog, contacto, legales, sitemap
    build_pages.run(globals())
    print("Hecho.")
