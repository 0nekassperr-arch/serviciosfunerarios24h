# -*- coding: utf-8 -*-
"""Genera el resto de paginas del sitio. Recibe el namespace de build.py."""
import os

def run(g):
    page        = g["page"]
    prefix_for  = g["prefix_for"]
    L           = g["L"]
    page_hero   = g["page_hero"]
    crumbs_html = g["crumbs_html"]
    cta_band    = g["cta_band"]
    lead_form   = g["lead_form"]
    faq_block   = g["faq_block"]
    breadcrumb  = g["breadcrumb"]
    org_schema  = g["org_schema"]
    website_schema = g["website_schema"]
    faq_schema  = g["faq_schema"]
    render_home_body = g["render_home_body"]
    BASE_URL = g["BASE_URL"]; SITE_NAME=g["SITE_NAME"]; BRAND=g["BRAND"]
    PHONE_TEL=g["PHONE_TEL"]; PHONE_DISP=g["PHONE_DISP"]; EMAIL=g["EMAIL"]
    ADDR_STREET=g["ADDR_STREET"]; ADDR_ZIP=g["ADDR_ZIP"]; ADDR_CITY=g["ADDR_CITY"]
    ADDR_PROV=g["ADDR_PROV"]; LEGAL_NAME=g["LEGAL_NAME"]; LEGAL_NIF=g["LEGAL_NIF"]
    ZONES=g["ZONES"]; BLOG_POSTS=g["BLOG_POSTS"]; YEAR=g["YEAR"]; OUT=g["OUT"]

    routes = [""]  # home ya generada

    # ============================== SERVICIOS ==============================
    px = prefix_for("servicios/")
    price_grid = '''<section class="section" aria-labelledby="precios-title">
      <div class="container">
        <span class="section__eyebrow">Tarifas orientativas</span>
        <h2 id="precios-title" class="section__title">Precios claros, desde el primer momento</h2>
        <p class="section__subtitle">Presupuestos cerrados y desglosados, sin cargos ocultos. Cada servicio se adapta a lo que su familia necesita.</p>
        <div class="price-grid">
          <div class="price-card price-card--featured">
            <h3>Incineración</h3>
            <p class="price-card__price">1.500€ <small>desde · IVA incluido</small></p>
            <ul>
              <li>Recogida y traslado del fallecido</li>
              <li>Féretro para incineración</li>
              <li>Trámites y licencia incluidos</li>
              <li>Coordinación del crematorio</li>
              <li>Urna básica para las cenizas</li>
            </ul>
            <a class="btn btn--primary btn--block" href="#formulario" data-track="serv-inci">Solicitar presupuesto</a>
          </div>
          <div class="price-card">
            <h3>Inhumación</h3>
            <p class="price-card__price">2.900€ <small>desde · sin sepultura</small></p>
            <ul>
              <li>Recogida y traslado del fallecido</li>
              <li>Féretro de inhumación</li>
              <li>Coche fúnebre</li>
              <li>Gestión de trámites y licencia</li>
              <li>Coordinación con el cementerio</li>
            </ul>
            <a class="btn btn--ghost btn--block" href="#formulario" data-track="serv-inhu">Solicitar presupuesto</a>
          </div>
          <div class="price-card">
            <h3>Servicio completo</h3>
            <p class="price-card__price">A medida <small>presupuesto personalizado</small></p>
            <ul>
              <li>Velatorio y sala tanatorio</li>
              <li>Ceremonia religiosa o civil</li>
              <li>Flores, esquelas y recordatorios</li>
              <li>Tanatoestética</li>
              <li>Atención personalizada 24h</li>
            </ul>
            <a class="btn btn--ghost btn--block" href="#formulario" data-track="serv-full">Solicitar presupuesto</a>
          </div>
        </div>
        <p class="price-note">Precios orientativos. El importe final depende de las prestaciones elegidas y de las tasas de cada municipio. Le entregamos siempre un presupuesto por escrito antes de contratar.</p>
      </div>
    </section>'''

    def serv(id_, title, text, points):
        pts = "".join(f"<li>{p}</li>" for p in points)
        return f'''<section class="section section--alt serv-block" id="{id_}">
      <div class="container">
        <h2>{title}</h2>
        <div class="serv-block__grid">
          <div>{text}</div>
          <ul class="serv-block__list">{pts}</ul>
        </div>
      </div>
    </section>'''

    serv_sections = "".join([
      serv("incineracion","Incineración (cremación)",
        "<p>La incineración es la opción más elegida en el sur de Madrid por su flexibilidad y su precio contenido. Nos encargamos de todo el proceso con el máximo respeto: recogida, preparación, coordinación del crematorio y entrega de las cenizas en la urna que elija. Le acompañamos también a la hora de decidir el destino de las cenizas.</p>",
        ["Incineración desde 1.500€","Amplia variedad de urnas","Cenizas entregadas con documentación oficial","Posibilidad de ceremonia previa"]),
      serv("inhumacion","Inhumación (entierro)",
        "<p>Para las familias que prefieren el entierro tradicional, gestionamos el servicio completo de inhumación, incluida la coordinación con el cementerio y, si lo necesita, la búsqueda y tramitación de la sepultura o nicho.</p>",
        ["Féretro y coche fúnebre","Gestión de sepultura o nicho","Coordinación con el cementerio","Lápidas y trabajos de marmolería"]),
      serv("traslados","Traslados nacionales e internacionales",
        "<p>Si el fallecimiento se produce lejos del lugar donde la familia desea la despedida, organizamos el traslado con todas las garantías legales y sanitarias, tanto dentro de España como al extranjero (repatriaciones).</p>",
        ["Traslado nacional desde 900€","Repatriaciones internacionales","Gestión documental completa","Coordinación puerta a puerta"]),
      serv("tanatorio","Tanatorio y velatorio",
        "<p>Coordinamos salas de velatorio en los tanatorios del sur de Madrid para que familiares y amigos puedan despedirse en un entorno digno y acogedor, con los tiempos que cada familia necesite.</p>",
        ["Salas de velatorio","Cafetería y espacios de descanso","Tanatoestética y tanatopraxia","Horarios flexibles"]),
      serv("ceremonias","Ceremonias religiosas y civiles",
        "<p>Organizamos la ceremonia de despedida según las creencias y deseos de cada familia: religiosa (de cualquier confesión) o civil, con música, lecturas y los detalles que hagan del adiós un homenaje personal.</p>",
        ["Ceremonias religiosas","Ceremonias civiles personalizadas","Música y proyección de recuerdos","Oficiante o maestro de ceremonias"]),
      serv("prevision","Previsión y planificación",
        "<p>Dejarlo todo previsto es un acto de amor hacia los suyos. Le ayudamos a planificar el servicio con antelación, fijando hoy las condiciones y evitando decisiones difíciles en el futuro.</p>",
        ["Planificación personalizada","Precio fijado por adelantado","Revisable en cualquier momento","Tranquilidad para su familia"]),
      serv("seguros","Seguros de decesos",
        "<p>¿Tiene un seguro de decesos y no sabe qué cubre? Lo revisamos por usted y gestionamos el servicio aprovechando al máximo su póliza. Recuerde: tiene derecho a elegirnos aunque su seguro sea de otra compañía.</p>",
        ["Revisión gratuita de su póliza","Gestión con la aseguradora","Libertad de elección garantizada","Sin coste añadido para usted"]),
      serv("tramites","Gestión de trámites",
        "<p>Nos ocupamos de toda la parte administrativa urgente —certificados, inscripción en el Registro Civil, licencias— y le orientamos sobre los trámites posteriores (pensiones, herencias, últimas voluntades).</p>",
        ["Certificado y Registro Civil","Licencias de enterramiento/incineración","Orientación sobre pensiones y herencias","Asesoramiento para familias sin seguro"]),
    ])

    serv_faq = [
      ("¿Cuánto cuesta una incineración?","Ofrecemos incineración desde 1.500 €, con trámites incluidos y presupuesto cerrado por escrito."),
      ("¿Puedo elegirles si tengo seguro de otra compañía?","Sí. La ley le garantiza la libertad de elección de funeraria, y la aseguradora debe abonar el importe cubierto."),
      ("¿Atienden fuera de Móstoles?","Sí, trabajamos en todo el sur de Madrid: Alcorcón, Fuenlabrada, Leganés, Getafe, Arroyomolinos y municipios cercanos."),
      ("¿Ofrecen facilidades de pago?","Sí. Valoramos con usted opciones de financiación, especialmente para familias sin seguro de decesos."),
    ]

    body = (
      page_hero("Servicios funerarios en Móstoles y Madrid Sur",
                "Un servicio completo, humano y transparente para acompañar a su familia en cada paso.") +
      crumbs_html(px, [("Inicio",""),("Servicios","servicios/")]) +
      '''<section class="section"><div class="container prose" style="text-align:center">
        <p class="prose-lead">Ofrecemos todos los servicios funerarios que su familia puede necesitar, con atención las 24 horas del día y precios claros desde el primer momento. Nos encargamos de absolutamente todo para que usted solo tenga que ocuparse de despedirse de su ser querido.</p>
      </div></section>''' +
      price_grid +
      serv_sections +
      cta_band(px) +
      faq_block("Preguntas sobre nuestros servicios", serv_faq) +
      lead_form(px, "Solicite presupuesto de cualquier servicio",
                "Cuéntenos qué necesita y le prepararemos un presupuesto claro y sin compromiso.")
    )
    page("servicios/",
         "Servicios Funerarios en Móstoles y Madrid Sur | Incineración desde 1.500€",
         "Todos los servicios funerarios en Móstoles y el sur de Madrid: incineración desde 1.500€, inhumación, traslados, tanatorio, ceremonias, previsión, seguros y trámites. Atención 24h.",
         "servicios funerarios, incineración Móstoles, inhumación, traslados funerarios, tanatorio Madrid sur, previsión funeraria",
         body,
         [org_schema(),
          breadcrumb([("Inicio",""),("Servicios","servicios/")]),
          {"@context":"https://schema.org","@type":"Service","name":"Servicios funerarios",
           "provider":{"@type":"FuneralHome","name":SITE_NAME},
           "areaServed":[{"@type":"City","name":z["name"]} for z in ZONES],
           "offers":{"@type":"Offer","price":"1500","priceCurrency":"EUR","description":"Incineración desde 1.500€"}},
          faq_schema(serv_faq)])
    routes.append("servicios/")

    # ============================== ZONAS (hub) ==============================
    px = prefix_for("zonas/")
    cards = "".join(
      f'''<a class="post-card zone-card" href="{L(px, z["slug"]+"/")}">
            <div class="post-card__body">
              <span class="post-card__tag">Madrid Sur</span>
              <h3>Funeraria en {z["name"]}</h3>
              <p>Servicios funerarios 24h en {z["name"]}: atención inmediata, precios transparentes y trato cercano.</p>
              <span class="readmore">Ver zona →</span>
            </div>
          </a>''' for z in ZONES)
    body = (
      page_hero("Zonas donde trabajamos","Servicios funerarios 24 horas en Móstoles y todo el sur de Madrid.") +
      crumbs_html(px, [("Inicio",""),("Zonas","zonas/")]) +
      '''<section class="section"><div class="container">
        <p class="section__subtitle">Damos servicio en los principales municipios del sur de Madrid. Elija su localidad para conocer cómo le atendemos en su zona.</p>
        <div class="post-grid">''' + cards + '''</div>
      </div></section>''' +
      cta_band(px)
    )
    page("zonas/",
         "Zonas | Servicios Funerarios 24h en el Sur de Madrid",
         "Zonas donde ofrecemos servicios funerarios 24h: Móstoles, Alcorcón, Fuenlabrada, Leganés, Getafe y Arroyomolinos. Atención inmediata en todo el sur de Madrid.",
         "funeraria sur de Madrid, funeraria Móstoles, funeraria Alcorcón, funeraria Fuenlabrada, funeraria Leganés, funeraria Getafe",
         body,
         [org_schema(), breadcrumb([("Inicio",""),("Zonas","zonas/")])])
    routes.append("zonas/")

    # ============================== PAGINAS DE ZONA ==============================
    for z in ZONES:
        route = z["slug"] + "/"
        px = prefix_for(route)
        if z.get("home_clone"):
            # Móstoles = idéntica a la home (mismo cuerpo y fotos)
            page(route,
                 "Servicios Funerarios en Móstoles 24h | Incineración desde 1.500€",
                 "Servicios funerarios en Móstoles 24 horas. Atención inmediata ante un fallecimiento, incineración desde 1.500€, trámites incluidos y precios transparentes.",
                 "funeraria Móstoles, servicios funerarios Móstoles, incineración Móstoles, tanatorio Móstoles, precio funeral Móstoles",
                 render_home_body(px),
                 [org_schema(),
                  breadcrumb([("Inicio",""),("Móstoles","mostoles/")]),
                  faq_schema([
                    ("¿Atienden las 24 horas en Móstoles?","Sí, estamos disponibles las 24 horas del día, los 365 días del año en Móstoles."),
                    ("¿Cuánto cuesta una incineración en Móstoles?","Ofrecemos incineración desde 1.500 €, con presupuesto claro y sin cargos ocultos."),
                  ])])
            routes.append(route)
            continue

        name = z["name"]
        zfaq = [
          (f"¿Atienden las 24 horas en {name}?", f"Sí. En {name} estamos disponibles las 24 horas del día, los 365 días del año. Ante un fallecimiento, llámenos y le atenderemos de inmediato."),
          (f"¿Cuánto cuesta un servicio funerario en {name}?", "Ofrecemos incineración desde 1.500 € y presupuestos cerrados y transparentes, adaptados a lo que su familia necesite."),
          (f"¿Qué hago si fallece un familiar en {name}?", f"Llámenos al {PHONE_DISP}. Le orientamos con calma sobre los primeros pasos y coordinamos el traslado y los preparativos en {name} de inmediato."),
          ("¿Trabajan con familias sin seguro de decesos?", "Sí. Le ayudamos a encontrar opciones ajustadas a su presupuesto y posibilidades de financiación."),
        ]
        benefits = '''<section class="section" aria-labelledby="b-title">
      <div class="container">
        <span class="section__eyebrow">Cómo le ayudamos</span>
        <h2 id="b-title" class="section__title">Un servicio completo en ''' + name + '''</h2>
        <div class="grid-3">
          <article class="card"><div class="card__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 1 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/></svg></div><h3 class="card__title">Atención inmediata</h3><p class="card__text">Un asesor le atiende al instante y coordina el traslado en ''' + name + ''' a cualquier hora.</p></article>
          <article class="card"><div class="card__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0l-7-7A2 2 0 0 1 3 12.2V4a1 1 0 0 1 1-1h8.2c.5 0 1 .2 1.4.6l7 7a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg></div><h3 class="card__title">Precios transparentes</h3><p class="card__text">Presupuestos claros y desglosados, sin cargos ocultos. Incineración desde 1.500€.</p></article>
          <article class="card"><div class="card__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6a1 1 0 0 1 1 1v1h2a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h2V4a1 1 0 0 1 1-1z"/><path d="M9 12h6M9 16h4"/></svg></div><h3 class="card__title">Trámites incluidos</h3><p class="card__text">Nos ocupamos del certificado, el Registro Civil y las licencias necesarias.</p></article>
        </div>
      </div>
    </section>'''
        urgency = f'''<section class="urgency urgency--photo">
      <div class="container urgency__inner">
        <p class="urgency__flag">Asistencia inmediata en {name} · 24h</p>
        <h2 class="urgency__title">¿Ha fallecido un ser querido en {name}?</h2>
        <p class="urgency__text">Le acompañamos en este momento. Un asesor le atenderá de inmediato y coordinará todo en {name}. Estamos disponibles a cualquier hora, todos los días.</p>
        <a class="btn-call" href="tel:{PHONE_TEL}" data-track="urgency-call"><span class="btn-call__icon" aria-hidden="true">📞</span><span class="btn-call__label"><strong>LLAMAR AHORA · 24H</strong><small>{PHONE_DISP} — Le atendemos ya</small></span></a>
        <p class="urgency__note">Llamada de orientación gratuita · También le devolvemos la llamada</p>
      </div>
    </section>'''
        local = f'''<section class="section section--alt">
      <div class="container media">
        <div class="media__img"><img src="{px}assets/camino-sereno.jpg" alt="Entorno sereno y tranquilo, luz cálida" loading="lazy" /></div>
        <div class="media__body">
          <span class="section__eyebrow" style="text-align:left">Servicio local en {name}</span>
          <h2>Cercanos a las familias de {name}</h2>
          <p>{z["intro"]}</p>
          <p>Atendemos con rapidez fallecimientos en {z["landmarks"]}. {z["extra"]}</p>
          <ul class="media__list">
            <li>Incineración e inhumación en {name} y alrededores</li>
            <li>Traslados nacionales e internacionales</li>
            <li>Gestión completa de trámites</li>
            <li>Atención a familias sin seguro de decesos</li>
          </ul>
        </div>
      </div>
    </section>'''
        body = (
          page_hero(f"Funeraria en {name} · 24 horas", z["hero_sub"]) +
          crumbs_html(px, [("Inicio",""),("Zonas","zonas/"),(name, route)]) +
          urgency + benefits + local +
          faq_block(f"Preguntas frecuentes en {name}", zfaq) +
          lead_form(px, f"Solicite información en {name}",
                    f"Déjenos sus datos y le contactaremos en unos minutos para orientarle en {name}.")
        )
        page(route,
             f"Funeraria en {name} 24h | Servicios Funerarios · Incineración desde 1.500€",
             f"Servicios funerarios en {name} 24 horas. Atención inmediata ante un fallecimiento, incineración desde 1.500€, trámites incluidos y precios transparentes en {name}.",
             f"funeraria {name}, servicios funerarios {name}, incineración {name}, tanatorio {name}, precio funeral {name}",
             body,
             [org_schema(),
              breadcrumb([("Inicio",""),("Zonas","zonas/"),(name,route)]),
              {"@context":"https://schema.org","@type":"FuneralHome","name":f"{SITE_NAME} · {name}",
               "areaServed":{"@type":"City","name":name},"telephone":PHONE_TEL,"url":BASE_URL+"/"+route,
               "priceRange":"€€"},
              faq_schema(zfaq)],
             og_image="assets/camino-sereno.jpg")
        routes.append(route)

    # ============================== NECESITO AYUDA ==============================
    px = prefix_for("necesito-ayuda/")
    def acc(title, pairs):
        items = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in pairs)
        return f'<h2 class="help-h2">{title}</h2><div class="faq">{items}</div>'

    help_body = (
      page_hero("Necesito ayuda","Respuestas claras a las dudas más frecuentes en un momento difícil.", photo=False) +
      crumbs_html(px, [("Inicio",""),("Necesito ayuda","necesito-ayuda/")]) +
      '<section class="section"><div class="container" style="max-width:820px">' +
      '<p class="prose-lead">Sabemos que cuando fallece un ser querido surgen muchas preguntas y pocas respuestas. Aquí reunimos, de forma breve y clara, lo que más nos consultan las familias. Y si necesita hablar con alguien ahora mismo, estamos a una llamada.</p>' +
      acc("Acaba de fallecer un familiar: ¿qué hago ahora?", [
        ("Ha fallecido en casa","Avise a un médico para que expida el certificado de defunción (su médico de cabecera o el 112). Hasta entonces, el cuerpo no puede trasladarse. Después, llámenos y nos ocupamos del traslado y de todo lo demás."),
        ("Ha fallecido en el hospital o residencia","El propio centro emite el certificado. Usted solo tiene que elegir la funeraria; no está obligado a aceptar la que le propongan. Avísenos y coordinamos la recogida."),
        ("¿Cuánto tiempo tengo para decidir?","No hay que precipitarse. La inscripción en el Registro Civil se realiza en 24-72 horas, y de eso nos encargamos nosotros. Usted decide el resto con calma."),
      ]) +
      acc("Dudas sobre el servicio", [
        ("No sé si incinerar o enterrar","Si la persona dejó su voluntad, se respeta. Si no, valore sus creencias, si disponen de sepultura y el presupuesto. Le orientamos sin presión."),
        ("No tengo seguro de decesos","Es muy habitual. Ofrecemos servicios desde 1.500 € y opciones de financiación. Nunca condicionamos la calidad del trato al presupuesto."),
        ("Tengo un seguro pero no sé qué cubre","Facilítenos los datos de la póliza y la revisamos gratis. Además, puede elegirnos aunque el seguro sea de otra compañía."),
      ]) +
      acc("Trámites y documentos", [
        ("¿Qué documentos necesito?","DNI del fallecido y de quien gestiona, certificado médico de defunción y, si existe, la póliza del seguro. Le ayudamos con todo lo demás."),
        ("¿Quién hace los trámites legales?","Nosotros gestionamos certificado, Registro Civil y licencias. Le orientamos también sobre pensiones, herencias y últimas voluntades."),
        ("¿Y los trámites posteriores (pensiones, herencia)?","Le indicamos plazos y dónde acudir: certificado de últimas voluntades (desde 15 días), pensión de viudedad, Impuesto de Sucesiones (6 meses), etc."),
      ]) +
      acc("Situaciones especiales", [
        ("El fallecimiento ha sido lejos de Madrid","Organizamos el traslado nacional o la repatriación internacional con todas las garantías, puerta a puerta."),
        ("Quiero dejarlo todo previsto","Le ayudamos a planificar el servicio con antelación, fijando hoy las condiciones para evitar cargas futuras a su familia."),
      ]) +
      '</div></section>' +
      cta_band(px, "¿Prefiere que le llamemos?") +
      # enlaces al blog
      '<section class="section section--alt"><div class="container">' +
      '<span class="section__eyebrow">Le puede interesar</span>' +
      '<h2 class="section__title">Guías que resuelven dudas</h2>' +
      '<div class="post-grid" style="margin-top:26px">' +
      "".join(
        f'''<a class="post-card" href="{L(px,'blog/'+p['slug']+'/')}">
              <img src="{px}{p['image']}" alt="{p['image_alt']}" loading="lazy" />
              <div class="post-card__body"><span class="post-card__tag">{p['category']}</span>
              <h3>{p['title']}</h3></div></a>''' for p in BLOG_POSTS[:3]) +
      '</div></div></section>'
    )
    help_faq = [(q,a) for (_,pairs) in [
        ("x",[("¿Atienden 24h?","Sí, las 24 horas los 365 días del año.")])] for (q,a) in pairs]
    page("necesito-ayuda/",
         "Necesito ayuda | Qué hacer ante un fallecimiento en Madrid Sur",
         "¿Necesita ayuda ante un fallecimiento? Respuestas claras: qué hacer si fallece un familiar en casa, hospital o residencia, trámites, documentos y qué hacer sin seguro de decesos.",
         "qué hacer ante un fallecimiento, necesito ayuda funeraria, fallecimiento en casa, trámites fallecimiento Madrid",
         help_body,
         [org_schema(), breadcrumb([("Inicio",""),("Necesito ayuda","necesito-ayuda/")]),
          faq_schema([
            ("¿Qué hago si fallece un familiar en casa?","Avise a un médico para el certificado de defunción y después llame a la funeraria, que se ocupa del traslado y los trámites."),
            ("¿Estoy obligado a contratar la funeraria del hospital?","No. Tiene derecho a elegir libremente la funeraria que desee."),
            ("¿Qué pasa si no tengo seguro de decesos?","Existen servicios ajustados desde 1.500€ y opciones de financiación."),
          ])])
    routes.append("necesito-ayuda/")

    # ============================== BLOG INDEX ==============================
    px = prefix_for("blog/")
    cards = "".join(
      f'''<a class="post-card" href="{L(px, 'blog/'+p['slug']+'/')}">
            <img src="{px}{p['image']}" alt="{p['image_alt']}" loading="lazy" />
            <div class="post-card__body">
              <span class="post-card__tag">{p['category']}</span>
              <h3>{p['title']}</h3>
              <p>{p['description']}</p>
              <span class="post-meta">{p['date_h']}</span>
            </div>
          </a>''' for p in BLOG_POSTS)
    body = (
      page_hero("Blog · Guías y consejos","Información útil y cercana para acompañarle en cada situación.", photo=False) +
      crumbs_html(px, [("Inicio",""),("Blog","blog/")]) +
      '<section class="section"><div class="container"><div class="post-grid">' + cards + '</div></div></section>' +
      cta_band(px)
    )
    page("blog/",
         "Blog | Guías Funerarias y Consejos · Madrid Sur",
         "Blog con guías y consejos funerarios: qué hacer ante un fallecimiento, incineración o entierro, precios, seguros de decesos y trámites. Información clara y cercana.",
         "blog funerario, guía fallecimiento, consejos funerarios, trámites defunción, incineración entierro",
         body,
         [org_schema(), website_schema(), breadcrumb([("Inicio",""),("Blog","blog/")]),
          {"@context":"https://schema.org","@type":"Blog","name":"Blog de "+SITE_NAME,"url":BASE_URL+"/blog/"}])
    routes.append("blog/")

    # ============================== ARTICULOS ==============================
    n = len(BLOG_POSTS)
    for i,p in enumerate(BLOG_POSTS):
        route = "blog/"+p["slug"]+"/"
        px = prefix_for(route)
        related = [BLOG_POSTS[(i+1)%n], BLOG_POSTS[(i+2)%n]]
        rel_html = "".join(
          f'''<a class="post-card" href="{L(px,'blog/'+r['slug']+'/')}">
                <img src="{px}{r['image']}" alt="{r['image_alt']}" loading="lazy" />
                <div class="post-card__body"><span class="post-card__tag">{r['category']}</span><h3>{r['title']}</h3></div>
              </a>''' for r in related)
        author = f'''<div class="author-box">
            <div class="author-box__ico">✦</div>
            <div><strong>Equipo de {SITE_NAME}</strong><br><span>Profesionales del sector funerario en el sur de Madrid. Escribimos para ayudar a las familias con información clara y honesta.</span></div>
          </div>'''
        body = (
          crumbs_html(px, [("Inicio",""),("Blog","blog/"),(p["title"], route)]) +
          f'''<article class="section"><div class="container prose">
            <p class="post-card__tag">{p['category']} · {p['date_h']}</p>
            <h1 class="article-title">{p['title']}</h1>
            <img class="article-hero" src="{px}{p['image']}" alt="{p['image_alt']}" />
            {p['body']}
            {author}
          </div></article>''' +
          cta_band(px) +
          '<section class="section section--alt"><div class="container"><span class="section__eyebrow">Seguir leyendo</span><h2 class="section__title">Artículos relacionados</h2><div class="post-grid" style="margin-top:26px">' + rel_html + '</div>' +
          f'<p style="text-align:center;margin-top:26px"><a href="{L(px,"blog/")}">← Volver al blog</a></p></div></section>'
        )
        page(route, f"{p['title']} | {SITE_NAME}", p["description"], p["keywords"], body,
             [org_schema(),
              breadcrumb([("Inicio",""),("Blog","blog/"),(p["title"],route)]),
              {"@context":"https://schema.org","@type":"BlogPosting","headline":p["title"],
               "description":p["description"],"image":BASE_URL+"/"+p["image"],
               "datePublished":p["date"],"dateModified":p["date"],"inLanguage":"es-ES",
               "mainEntityOfPage":{"@type":"WebPage","@id":BASE_URL+"/"+route},
               "author":{"@type":"Organization","name":SITE_NAME},
               "publisher":{"@type":"Organization","name":SITE_NAME,"logo":{"@type":"ImageObject","url":BASE_URL+"/assets/hero-serenidad.jpg"}}}],
             og_image=p["image"], og_type="article")
        routes.append(route)

    # ============================== CONTACTO / QUIENES SOMOS ==============================
    px = prefix_for("contacto/")
    body = (
      page_hero("Contacto","Estamos a su lado las 24 horas. Llámenos o escríbanos.", photo=False) +
      crumbs_html(px, [("Inicio",""),("Contacto","contacto/")]) +
      f'''<section class="section" id="quienes-somos"><div class="container media">
        <div class="media__img"><img src="{px}assets/equipo.jpg" alt="Espacio de atención sereno y acogedor con luz natural cálida" loading="lazy" /></div>
        <div class="media__body">
          <span class="section__eyebrow" style="text-align:left">Quiénes somos</span>
          <h2>Un equipo cercano en el sur de Madrid</h2>
          <p>Somos un equipo de profesionales dedicado a acompañar a las familias del sur de Madrid en uno de los momentos más difíciles de la vida. Creemos en un servicio funerario <strong>humano, transparente y sin sorpresas</strong>, disponible a cualquier hora del día.</p>
          <p>Nuestro compromiso es sencillo: estar a su lado, explicarle cada paso con claridad y ofrecerle siempre un precio justo. Porque una despedida digna no debería ser motivo de preocupación económica.</p>
        </div>
      </div></section>''' +
      f'''<section class="section section--alt"><div class="container contact-grid">
        <div>
          <h2>Datos de contacto</h2>
          <ul class="info-list">
            <li><span class="ico">📞</span><div><strong>Teléfono 24h</strong><br><a href="tel:{PHONE_TEL}">{PHONE_DISP}</a></div></li>
            <li><span class="ico">💬</span><div><strong>WhatsApp</strong><br><a href="https://wa.me/34600000000" data-track="wa">Escríbanos por WhatsApp</a></div></li>
            <li><span class="ico">✉</span><div><strong>Email</strong><br><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
            <li><span class="ico">📍</span><div><strong>Dirección</strong><br>{ADDR_STREET}, {ADDR_ZIP} {ADDR_CITY} ({ADDR_PROV})</div></li>
            <li><span class="ico">🕒</span><div><strong>Horario</strong><br>24 horas, los 365 días del año</div></li>
          </ul>
        </div>
        <form class="lead-form" id="leadForm" novalidate>
          <div class="field"><label for="nombre">Nombre completo</label><input type="text" id="nombre" name="nombre" placeholder="Su nombre" autocomplete="name" required /></div>
          <div class="field"><label for="telefono">Teléfono <span class="req">*</span></label><input type="tel" id="telefono" name="telefono" placeholder="6XX XXX XXX" inputmode="tel" pattern="[0-9\\s+]{{9,15}}" required /></div>
          <div class="field"><label for="ubicacion">¿En qué podemos ayudarle?</label><input type="text" id="ubicacion" name="ubicacion" placeholder="Cuéntenos brevemente" autocomplete="off" required /></div>
          <label class="consent"><input type="checkbox" id="rgpd" name="rgpd" required /><span>He leído y acepto la <a href="{L(px,'privacidad/')}">Política de Privacidad</a> y autorizo el tratamiento de mis datos para ser contactado.</span></label>
          <button type="submit" class="btn btn--primary btn--block" data-track="form-submit">Enviar mensaje</button>
          <div class="form-success" id="formSuccess" role="status" aria-live="polite" hidden></div>
        </form>
      </div></section>''' +
      cta_band(px)
    )
    page("contacto/",
         "Contacto | Servicios Funerarios 24h en Madrid Sur",
         "Contacte con nosotros las 24 horas. Teléfono, WhatsApp y email para servicios funerarios en Móstoles y el sur de Madrid. Atención inmediata y cercana.",
         "contacto funeraria Móstoles, teléfono funeraria 24h, servicios funerarios contacto Madrid sur",
         body,
         [org_schema(), breadcrumb([("Inicio",""),("Contacto","contacto/")]),
          {"@context":"https://schema.org","@type":"ContactPage","name":"Contacto · "+SITE_NAME,"url":BASE_URL+"/contacto/"}])
    routes.append("contacto/")

    # ============================== LEGALES ==============================
    def legal_page(route, h1, title, desc, prose_html):
        px = prefix_for(route)
        body = (page_hero(h1, "", photo=False).replace("<p></p>","") +
                crumbs_html(px, [("Inicio",""),(h1, route)]) +
                '<section class="section"><div class="container prose">' + prose_html + '</div></section>')
        page(route, title, desc, "aviso legal, privacidad, cookies, "+BRAND, body,
             [org_schema(), breadcrumb([("Inicio",""),(h1,route)])])
        routes.append(route)

    aviso = f'''
      <p><em>Última actualización: {YEAR}. ⚠ Datos del titular pendientes de completar.</em></p>
      <h2>1. Datos identificativos</h2>
      <p>En cumplimiento de la Ley 34/2002 (LSSI-CE), se informa de que este sitio web es titularidad de:</p>
      <ul>
        <li><strong>Titular:</strong> {LEGAL_NAME}</li>
        <li><strong>NIF/CIF:</strong> {LEGAL_NIF}</li>
        <li><strong>Domicilio:</strong> {ADDR_STREET}, {ADDR_ZIP} {ADDR_CITY} ({ADDR_PROV})</li>
        <li><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><strong>Teléfono:</strong> <a href="tel:{PHONE_TEL}">{PHONE_DISP}</a></li>
        <li><strong>Sitio web:</strong> {BRAND}</li>
      </ul>

      <h2>2. Aviso de transparencia</h2>
      <blockquote><strong>Aviso de transparencia:</strong> {BRAND} es un servicio independiente de orientación funeraria y no presta directamente servicios funerarios. Colaboramos con funerarias locales del sur de Madrid, que son quienes realizan el servicio contratado.</blockquote>

      <h2>3. Objeto</h2>
      <p>El presente aviso legal regula el uso del sitio web {BRAND}. La navegación por el sitio atribuye la condición de usuario e implica la aceptación plena de todas las cláusulas aquí recogidas.</p>

      <h2>4. Condiciones de uso</h2>
      <p>El usuario se compromete a hacer un uso adecuado de los contenidos y servicios y a no emplearlos para incurrir en actividades ilícitas o contrarias a la buena fe. La información publicada tiene carácter meramente orientativo y no sustituye el asesoramiento profesional individualizado.</p>

      <h2>5. Propiedad intelectual e industrial</h2>
      <p>Todos los contenidos del sitio (textos, imágenes, diseño, logotipos y código) están protegidos por los derechos de propiedad intelectual e industrial. Queda prohibida su reproducción, distribución o transformación sin autorización expresa del titular.</p>

      <h2>6. Responsabilidad</h2>
      <p>El titular no se hace responsable de los daños derivados del uso del sitio ni de la exactitud permanente de los contenidos, que pueden actualizarse sin previo aviso.</p>

      <h2>7. Legislación aplicable</h2>
      <p>Este aviso legal se rige por la legislación española. Para cualquier controversia serán competentes los juzgados y tribunales que correspondan conforme a derecho.</p>
    '''
    legal_page("aviso-legal/","Aviso Legal","Aviso Legal | "+BRAND,
               "Aviso legal de "+BRAND+": datos del titular, condiciones de uso, propiedad intelectual y aviso de transparencia del servicio.", aviso)

    priv = f'''
      <p><em>Última actualización: {YEAR}.</em></p>
      <h2>1. Responsable del tratamiento</h2>
      <p><strong>{LEGAL_NAME}</strong> (NIF {LEGAL_NIF}), con domicilio en {ADDR_STREET}, {ADDR_ZIP} {ADDR_CITY} ({ADDR_PROV}). Email: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>

      <h2>2. Finalidad del tratamiento</h2>
      <p>Tratamos los datos que nos facilita a través de los formularios o del teléfono con la finalidad de <strong>atender su solicitud de información o de servicio funerario</strong> y contactarle. Con su consentimiento, sus datos podrán comunicarse a la funeraria colaboradora encargada de prestar el servicio en su zona.</p>

      <h2>3. Legitimación</h2>
      <p>La base legal es el <strong>consentimiento</strong> del interesado, prestado al marcar la casilla correspondiente, y la aplicación de medidas precontractuales a petición del interesado.</p>

      <h2>4. Conservación de los datos</h2>
      <p>Conservaremos sus datos durante el tiempo necesario para atender su solicitud y, posteriormente, durante los plazos legalmente exigibles. Una vez cumplidas dichas finalidades, se suprimirán.</p>

      <h2>5. Destinatarios</h2>
      <p>Sus datos podrán cederse a las funerarias colaboradoras a efectos de prestar el servicio solicitado, así como a proveedores tecnológicos que actúan como encargados del tratamiento. No se realizan transferencias internacionales salvo las estrictamente necesarias con las garantías adecuadas.</p>

      <h2>6. Derechos</h2>
      <p>Puede ejercer sus derechos de <strong>acceso, rectificación, supresión, oposición, limitación y portabilidad</strong> escribiendo a <a href="mailto:{EMAIL}">{EMAIL}</a>, adjuntando copia de un documento identificativo. Asimismo, puede presentar una reclamación ante la Agencia Española de Protección de Datos (<a href="https://www.aepd.es" rel="nofollow">www.aepd.es</a>).</p>

      <h2>7. Medidas de seguridad</h2>
      <p>Aplicamos las medidas técnicas y organizativas necesarias para garantizar la seguridad de los datos y evitar su alteración, pérdida o acceso no autorizado.</p>
    '''
    legal_page("privacidad/","Política de Privacidad","Política de Privacidad | "+BRAND,
               "Política de privacidad de "+BRAND+": responsable, finalidad, legitimación, destinatarios y derechos sobre sus datos personales (RGPD).", priv)

    cookies = f'''
      <p><em>Última actualización: {YEAR}.</em></p>
      <h2>1. ¿Qué son las cookies?</h2>
      <p>Las cookies son pequeños archivos que se descargan en su dispositivo al visitar determinadas páginas web y permiten, entre otras cosas, almacenar y recuperar información sobre los hábitos de navegación.</p>

      <h2>2. Cookies que utilizamos</h2>
      <p>Este sitio utiliza únicamente <strong>cookies técnicas y de funcionamiento</strong> necesarias para la navegación. En caso de incorporar en el futuro cookies analíticas o de terceros (por ejemplo, de medición de tráfico), se solicitará su consentimiento previo mediante el banner correspondiente.</p>
      <table class="ptable">
        <thead><tr><th>Tipo</th><th>Finalidad</th></tr></thead>
        <tbody>
          <tr><td>Técnicas</td><td>Funcionamiento básico del sitio.</td></tr>
          <tr><td>Preferencias</td><td>Recordar opciones del usuario (p. ej. reparto interno).</td></tr>
        </tbody>
      </table>

      <h2>3. Cómo gestionar las cookies</h2>
      <p>Puede permitir, bloquear o eliminar las cookies instaladas en su equipo mediante la configuración de las opciones de su navegador. A continuación tiene los enlaces de ayuda de los principales navegadores: Chrome, Firefox, Safari y Edge.</p>

      <h2>4. Actualizaciones</h2>
      <p>Esta política puede modificarse en función de novedades legislativas o técnicas, por lo que se recomienda su consulta periódica.</p>
    '''
    legal_page("cookies/","Política de Cookies","Política de Cookies | "+BRAND,
               "Política de cookies de "+BRAND+": qué cookies utilizamos y cómo gestionarlas.", cookies)

    # ============================== SITEMAP + ROBOTS + CNAME ==============================
    today = g["datetime"].date.today().isoformat() if "datetime" in g else __import__("datetime").date.today().isoformat()
    urls=[]
    for r in routes:
        loc = BASE_URL + "/" + r
        pr = "1.0" if r=="" else ("0.9" if r in ("servicios/","zonas/","contacto/") else "0.7")
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority></url>")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    with open(os.path.join(OUT,"sitemap.xml"),"w",encoding="utf-8") as f: f.write(sitemap)

    robots = f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n"
    with open(os.path.join(OUT,"robots.txt"),"w",encoding="utf-8") as f: f.write(robots)

    with open(os.path.join(OUT,"CNAME"),"w",encoding="utf-8") as f: f.write("serviciosfunerarios24h.es\n")

    print(f"Total rutas: {len(routes)}  ->  sitemap.xml, robots.txt y CNAME generados.")
