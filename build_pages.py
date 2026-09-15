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
    address_line = g["address_line"]
    ZONES=g["ZONES"]; BLOG_POSTS=g["BLOG_POSTS"]; YEAR=g["YEAR"]; OUT=g["OUT"]

    routes = [""]  # home ya generada

    # Ciudades con página específica "Tanatorio en [ciudad]" (alta demanda en Search Console)
    TANATORIO = [
        {"slug":"mostoles","name":"Móstoles","hosp":"el Hospital Universitario de Móstoles","barrios":"El Soto, Parque Coimbra o Las Cumbres"},
        {"slug":"fuenlabrada","name":"Fuenlabrada","hosp":"el Hospital Universitario de Fuenlabrada","barrios":"Loranca, El Vivero o La Serna"},
        {"slug":"getafe","name":"Getafe","hosp":"el Hospital Universitario de Getafe","barrios":"Sector III, Las Margaritas o Getafe Norte"},
        {"slug":"alcorcon","name":"Alcorcón","hosp":"el Hospital Universitario Fundación Alcorcón","barrios":"Parque Lisboa, San José de Valderas o Las Retamas"},
        {"slug":"leganes","name":"Leganés","hosp":"el Hospital Severo Ochoa","barrios":"Zarzaquemada, Leganés Norte o San Nicasio"},
        {"slug":"madrid","name":"Madrid","hosp":"los grandes hospitales de la ciudad","barrios":"todos los distritos"},
        {"slug":"villaviciosa-de-odon","name":"Villaviciosa de Odón","hosp":"los hospitales de Alcorcón y Móstoles, muy próximos","barrios":"el casco urbano y las urbanizaciones residenciales"},
        {"slug":"arroyomolinos","name":"Arroyomolinos","hosp":"los hospitales cercanos de Móstoles y Alcorcón","barrios":"el centro y las urbanizaciones"},
        {"slug":"toledo","name":"Toledo","hosp":"el Hospital Universitario de Toledo","barrios":"Santa Bárbara, Buenavista o el Polígono"},
        {"slug":"parla","name":"Parla","hosp":"el Hospital Infanta Cristina","barrios":"el centro y Parla Este"},
        {"slug":"pinto","name":"Pinto","hosp":"el Hospital de Getafe, muy próximo","barrios":"el centro y las nuevas urbanizaciones"},
    ]

    PRECIOS = [
        {"slug":"madrid","name":"Madrid",
         "local":"En Madrid capital el precio final depende mucho del distrito, del tanatorio (M-30 o Sur) y de las tasas del cementerio elegido. La incineración parte de 1.500 €; un servicio con sala en tanatorio de la capital suele encarecerse por la hora de sala y el traslado."},
        {"slug":"mostoles","name":"Móstoles",
         "local":"En Móstoles el velatorio se coordina en el Tanatorio Municipal (Camino de los Leñeros). Las tasas de cementerio municipal y, si hay incineración, el crematorio de Fuenlabrada (M-506) entran como partidas aparte en el presupuesto. Incineración desde 1.500 €."},
        {"slug":"fuenlabrada","name":"Fuenlabrada",
         "local":"Fuenlabrada tiene tanatorio y crematorio en el mismo recinto (M-506, junto al cementerio). Eso suele abaratar respecto a municipios que tienen que desplazar el cuerpo a otro crematorio. Incineración desde 1.500 €, con sala en el propio recinto si hay disponibilidad."},
        {"slug":"getafe","name":"Getafe",
         "local":"En Getafe el tanatorio está en la Carretera del Cementerio. Las familias de Pinto y Parla también usan este recinto, así que en fechas señaladas conviene reservar sala cuanto antes. Incineración desde 1.500 €; el crematorio más cercano con horarios amplios es el de Fuenlabrada."},
        {"slug":"alcorcon","name":"Alcorcón",
         "local":"En Alcorcón el tanatorio está en la Av. de Villaviciosa, junto al cementerio. El Hospital Fundación Alcorcón es el origen más habitual de las recogidas. Incineración desde 1.500 €; el crematorio de Fuenlabrada queda a pocos minutos por la M-50."},
        {"slug":"leganes","name":"Leganés",
         "local":"En Leganés el coste varía si el velatorio es en el tanatorio municipal o se desplaza a Getafe/Fuenlabrada (más salas y crematorio). Recogidas frecuentes en el Hospital Severo Ochoa. Incineración desde 1.500 €."},
        {"slug":"toledo","name":"Toledo",
         "local":"En Toledo el presupuesto incluye a menudo un traslado desde el Hospital Universitario o desde pueblos de la comarca. Las tasas de cementerio y tanatorio de la provincia son distintas a las de Madrid Sur; se las desglosamos por escrito. Incineración desde 1.500 €."},
    ]

    TANATORIO_LOCAL = {
        "mostoles": {
            "place": "Tanatorio Municipal de Móstoles",
            "addr": "Camino de los Leñeros, s/n, 28938 Móstoles",
            "local": "El velatorio de Móstoles se celebra habitualmente en el Tanatorio Municipal (Camino de los Leñeros, s/n), junto al cementerio, abierto 24 horas. Coordinamos la reserva de sala, el traslado desde el Hospital Universitario de Móstoles, el domicilio o una residencia, y la incineración o el entierro. El crematorio más usado por las familias de Móstoles es el de Fuenlabrada (M-506), a unos 15–20 minutos.",
        },
        "fuenlabrada": {
            "place": "Tanatorio-crematorio de Fuenlabrada",
            "addr": "Carretera M-506, junto al cementerio municipal, 28946 Fuenlabrada",
            "local": "El tanatorio de Fuenlabrada está en la M-506, junto al cementerio municipal (salida Cementerio/Tanatorio). Tiene velatorio y crematorio en el mismo recinto, abierto 24 horas. Desde el centro son unos 10 minutos en coche. Recogemos en el Hospital Universitario de Fuenlabrada, en Loranca, El Vivero, La Serna o en el domicilio, y reservamos la sala el mismo día.",
        },
        "getafe": {
            "place": "Tanatorio de Getafe",
            "addr": "Carretera del Cementerio, s/n, 28905 Getafe",
            "local": "El tanatorio de Getafe está en la Carretera del Cementerio, s/n, junto al camposanto municipal. Acceso desde la A-42 y la M-406. Abierto 24 horas. También acuden familias de Pinto, Parla y Villaverde. Coordinamos la recogida en el Hospital Universitario de Getafe y la reserva de sala.",
        },
        "alcorcon": {
            "place": "Tanatorio de Alcorcón",
            "addr": "Avenida de Villaviciosa, s/n (junto al cementerio), 28922 Alcorcón",
            "local": "El tanatorio de Alcorcón está en la Avenida de Villaviciosa, s/n, junto al cementerio municipal. Recogemos en el Hospital Universitario Fundación Alcorcón, en Parque Lisboa, San José de Valderas, Las Retamas o en el domicilio. Coordinamos sala, ceremonia e incineración (el crematorio de Fuenlabrada queda a pocos minutos por la M-50).",
        },
        "leganes": {
            "place": "Tanatorio de Leganés",
            "addr": "Recinto del cementerio municipal de Leganés",
            "local": "En Leganés coordinamos el velatorio en el tanatorio municipal o, si lo prefiere la familia, en Getafe o Fuenlabrada, que tienen más salas y crematorio. Recogida 24 h en el Hospital Severo Ochoa, Zarzaquemada, Leganés Norte, San Nicasio o el domicilio.",
        },
        "parla": {
            "place": "Tanatorio / cementerio de Parla",
            "addr": "Avenida Juan Carlos I, s/n (recinto del cementerio), 28981 Parla",
            "local": "El velatorio en Parla se organiza en el recinto del cementerio municipal (Avenida Juan Carlos I, s/n). Muchas familias de Parla Este también eligen el tanatorio de Getafe, a unos 15 minutos, porque tiene más salas. Recogemos en el Hospital Infanta Cristina, en el domicilio o en residencias, las 24 horas.",
        },
        "pinto": {
            "place": "Tanatorio para familias de Pinto",
            "addr": "La mayoría de velatorios de Pinto se celebran en Getafe (Carretera del Cementerio, s/n)",
            "local": "Pinto no tiene un gran tanatorio-crematorio propio. Las familias velan casi siempre en el Tanatorio de Getafe (Carretera del Cementerio, s/n, 10–15 minutos) o en Fuenlabrada (M-506), que sí tiene crematorio. Hacemos la recogida en Pinto —domicilio, residencia o el Hospital de Getafe— y reservamos la sala en el recinto que elija la familia.",
        },
        "madrid": {
            "place": "Tanatorios de Madrid capital",
            "addr": "Tanatorio M-30 (Ciudad Lineal) y Tanatorio Sur; también salas en hospitales y distritos",
            "local": "En Madrid capital el velatorio se organiza sobre todo en el Tanatorio M-30 (Ciudad Lineal) o en el Tanatorio Sur, según el distrito y la disponibilidad. Recogemos en La Paz, Gregorio Marañón, 12 de Octubre, Clínico San Carlos, en residencias y en el domicilio, a cualquier hora. Coordinamos sala, traslado a crematorio e inhumación en el cementerio que indique la familia.",
        },
        "toledo": {
            "place": "Tanatorios de Toledo y comarca",
            "addr": "Tanatorios de Toledo capital y municipios de la provincia; Hospital Universitario de Toledo",
            "local": "En Toledo coordinamos el velatorio en las instalaciones de la capital o de la comarca, según donde esté la familia. Recogida 24 h en el Hospital Universitario de Toledo, en Santa Bárbara, Buenavista, el Polígono, el casco histórico, el domicilio o una residencia. Trámites, sala e incineración o entierro en el cementerio que elijan.",
        },
        "arroyomolinos": {
            "place": "Tanatorio para familias de Arroyomolinos",
            "addr": "El velatorio habitual es el Tanatorio Municipal de Móstoles (Camino de los Leñeros, s/n), a unos 10–15 minutos",
            "local": "Arroyomolinos no tiene un gran tanatorio-crematorio propio. Las familias velan casi siempre en Móstoles (Camino de los Leñeros) o en Alcorcón (Av. de Villaviciosa). Recogemos en el domicilio, urbanizaciones y residencias de Arroyomolinos las 24 horas y reservamos la sala. El crematorio más usado es el de Fuenlabrada (M-506).",
        },
        "villaviciosa-de-odon": {
            "place": "Tanatorio para familias de Villaviciosa de Odón",
            "addr": "Cementerio municipal de Villaviciosa y tanatorios de Alcorcón (Av. de Villaviciosa) y Móstoles",
            "local": "En Villaviciosa de Odón coordinamos el velatorio en el entorno del cementerio municipal o, si hace falta más sala o crematorio, en Alcorcón (Av. de Villaviciosa, s/n) o Móstoles (Camino de los Leñeros). Recogida 24 h en el casco, urbanizaciones y residencias. El Hospital Fundación Alcorcón queda a pocos minutos.",
        },
    }
    for c in TANATORIO:
        extra = TANATORIO_LOCAL.get(c["slug"])
        if extra:
            c.update(extra)

    # Foto de hero distinta por URL (no reutilizar la misma en todas las landings)
    CITY_HERO = {
        "mostoles": "assets/camino-sereno.jpg",
        "alcorcon": "assets/apoyo-familiar.jpg",
        "fuenlabrada": "assets/hero-serenidad.jpg",
        "leganes": "assets/blog-duelo-acompanar.jpg",
        "getafe": "assets/blog-elegir.jpg",
        "arroyomolinos": "assets/blog-incineracion.jpg",
        "villaviciosa-de-odon": "assets/blog-cenizas.jpg",
        "madrid": "assets/blog-duelo.jpg",
        "toledo": "assets/blog-repatriacion.jpg",
        "parla": "assets/blog-tramites.jpg",
        "pinto": "assets/blog-tiempos.jpg",
    }
    TAN_HERO = {
        "mostoles": "assets/blog-tanatorio.jpg",
        "fuenlabrada": "assets/blog-fallecimiento.jpg",
        "getafe": "assets/blog-esquela.jpg",
        "alcorcon": "assets/equipo.jpg",
        "leganes": "assets/blog-seguro-decesos.jpg",
        "madrid": "assets/blog-testamento.jpg",
        "parla": "assets/blog-ayudas.jpg",
        "pinto": "assets/blog-incineracion.jpg",
        "toledo": "assets/camino-sereno.jpg",
        "arroyomolinos": "assets/apoyo-familiar.jpg",
        "villaviciosa-de-odon": "assets/hero-serenidad.jpg",
    }
    PRECIO_HERO = {
        "madrid": "assets/blog-ayudas.jpg",
        "mostoles": "assets/blog-elegir.jpg",
        "fuenlabrada": "assets/blog-seguro-decesos.jpg",
        "getafe": "assets/blog-tramites.jpg",
        "alcorcon": "assets/blog-tiempos.jpg",
        "leganes": "assets/blog-cenizas.jpg",
        "toledo": "assets/blog-duelo.jpg",
    }

    # ============================== SERVICIOS ==============================
    BTN_CALL = (
        f'<a class="btn btn--primary btn--xl" href="tel:{PHONE_TEL}" data-track="hero-call">'
        f'📞 LLAMAR AHORA · 24h</a>'
    )
    px = prefix_for("servicios/")
    price_grid = '''<section class="section" id="precios" aria-labelledby="precios-title">
      <div class="container">
        <span class="section__eyebrow">Tarifas orientativas</span>
        <h2 id="precios-title" class="section__title">Precios claros, desde el primer momento</h2>
        <p class="section__subtitle">Presupuestos cerrados y desglosados, sin cargos ocultos. Cada servicio se adapta a lo que su familia necesita.</p>
        <div class="price-grid">
          <div class="price-card price-card--featured">
            <h3>Incineración</h3>
            <p class="price-card__price"><small>Desde</small> 1.500€ <small>IVA incluido</small></p>
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
            <p class="price-card__price"><small>Desde</small> 2.900€ <small>sin sepultura</small></p>
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
            <p class="price-card__price"><small>Desde</small> a medida <small>presupuesto personalizado</small></p>
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

    ICO = {
      "flame": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3c2 4 2 6 0 8 3-1 6 1 6 5a6 6 0 1 1-12 0c0-5 4-8 6-13z"/></svg>',
      "earth": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s7-4.4 7-11a7 7 0 1 0-14 0c0 6.6 7 11 7 11z"/><circle cx="12" cy="11" r="2.2"/></svg>',
      "truck": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7h11v8H3z"/><path d="M14 10h4l3 3v2h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="18" cy="18" r="2"/></svg>',
      "home": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V7l7-4 7 4v14M9 21v-6h6v6"/></svg>',
      "music": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>',
      "plan": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/></svg>',
      "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 4 7v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V7l-8-4z"/></svg>',
      "docs": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6a1 1 0 0 1 1 1v1h2a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h2V4a1 1 0 0 1 1-1z"/><path d="M9 12h6M9 16h4"/></svg>',
    }

    def serv_card(id_, title, text, points, icon, featured=False):
        pts = "".join(f"<li>{p}</li>" for p in points)
        feat = " serv-card--featured" if featured else ""
        return f'''<article class="serv-card{feat}" id="{id_}">
          <div class="serv-card__icon">{icon}</div>
          <h3>{title}</h3>
          <p>{text}</p>
          <ul>{pts}</ul>
          <a class="btn btn--ghost btn--block" href="#formulario">Pedir presupuesto</a>
        </article>'''

    serv_cards = "".join([
      serv_card("incineracion","Incineración (cremación)",
        "La opción más elegida en el sur de Madrid. Recogida, trámites, crematorio y urna, con respeto y precio claro.",
        ["Desde 1.500 €","Urnas a elegir","Documentación oficial","Ceremonia previa si lo desea"],
        ICO["flame"], featured=True),
      serv_card("inhumacion","Inhumación (entierro)",
        "Servicio completo de entierro tradicional, con cementerio, nicho o sepultura si la necesita.",
        ["Féretro y coche fúnebre","Gestión de sepultura","Coordinación con el cementerio","Lápidas y marmolería"],
        ICO["earth"]),
      serv_card("traslados","Traslados y repatriación",
        "Si el fallecimiento es lejos de casa, organizamos el traslado nacional o internacional puerta a puerta.",
        ["Nacional desde 900 €","Repatriaciones","Gestión documental","Coordinación 24 h"],
        ICO["truck"]),
      serv_card("tanatorio","Tanatorio y velatorio",
        "Reservamos sala en el recinto de su localidad para una despedida serena, con los tiempos que su familia necesite.",
        ["Sala de velatorio","Horarios flexibles","Tanatoestética","Cafetería y descanso"],
        ICO["home"]),
      serv_card("ceremonias","Ceremonias",
        "Religiosa o civil, con música, lecturas y los detalles que hagan del adiós un homenaje personal.",
        ["Cualquier confesión","Ceremonia civil","Música y recuerdos","Oficiante si lo precisa"],
        ICO["music"]),
      serv_card("prevision","Previsión",
        "Dejarlo previsto es un acto de amor. Fijamos hoy las condiciones para no dejar decisiones difíciles a los suyos.",
        ["A su medida","Precio acordado","Revisable","Tranquilidad para la familia"],
        ICO["plan"]),
      serv_card("seguros","Seguros de decesos",
        "Revisamos su póliza sin coste. Puede elegirnos aunque el seguro sea de otra compañía.",
        ["Revisión gratuita","Trato con la aseguradora","Libertad de elección","Sin coste añadido"],
        ICO["shield"]),
      serv_card("tramites","Gestión de trámites",
        "Certificado, Registro Civil y licencias. Le orientamos también en pensiones, herencias y últimas voluntades.",
        ["Registro Civil","Licencias","Pensiones y herencias","Familias sin seguro"],
        ICO["docs"]),
    ])

    serv_sections = f'''<section class="section section--alt" aria-labelledby="serv-detalle-title">
      <div class="container">
        <span class="section__eyebrow">Qué cubrimos</span>
        <h2 id="serv-detalle-title" class="section__title">Cada servicio, con calma y claridad</h2>
        <p class="section__subtitle">Atención 24 horas. Usted elige; nosotros coordinamos.</p>
        <div class="serv-grid">{serv_cards}</div>
      </div>
    </section>'''

    serv_faq = [
      ("¿Cuánto cuesta una incineración?","Ofrecemos incineración desde 1.500 €, con trámites incluidos y presupuesto cerrado por escrito."),
      ("¿Puedo elegirles si tengo seguro de otra compañía?","Sí. La ley le garantiza la libertad de elección de funeraria, y la aseguradora debe abonar el importe cubierto."),
      ("¿Atienden fuera de Móstoles?","Sí, trabajamos en todo el sur de Madrid: Alcorcón, Fuenlabrada, Leganés, Getafe, Arroyomolinos y municipios cercanos."),
      ("¿Ofrecen facilidades de pago?","Sí. Valoramos con usted opciones de financiación, especialmente para familias sin seguro de decesos."),
    ]

    body = (
      page_hero("Servicios funerarios en Móstoles y Madrid Sur",
                "Un servicio completo, humano y transparente para acompañar a su familia en cada paso.",
                image="assets/apoyo-familiar.jpg",
                actions=BTN_CALL + '<a class="btn btn--offer" href="#precios">Ver precios <small>Desde 1.500 €</small></a>') +
      crumbs_html(px, [("Inicio",""),("Servicios","servicios/")]) +
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
      page_hero("Zonas donde trabajamos","Servicios funerarios 24 horas en Móstoles y todo el sur de Madrid.",
                image="assets/camino-sereno.jpg",
                actions=BTN_CALL + '<a class="btn btn--offer" href="#tanatorios">Tanatorios cercanos</a>') +
      crumbs_html(px, [("Inicio",""),("Zonas","zonas/")]) +
      '''<section class="section"><div class="container">
        <p class="section__subtitle">Damos servicio en los principales municipios del sur de Madrid. Elija su localidad para conocer cómo le atendemos en su zona.</p>
        <div class="post-grid">''' + cards + '''</div>
      </div></section>''' +
      ('<section class="section section--alt" id="tanatorios"><div class="container" style="text-align:center">'
       '<span class="section__eyebrow">Tanatorios por ciudad</span>'
       '<h2 class="section__title">Velatorio y tanatorio en su localidad</h2>'
       '<p class="section__subtitle">Coordinamos la sala de velatorio y todo el servicio en el tanatorio de su ciudad.</p>'
       '<p style="line-height:2.4">'
       + " · ".join(f'<a href="{L(px, "tanatorio-"+c["slug"]+"/")}">Tanatorio en {c["name"]}</a>' for c in TANATORIO)
       + '</p></div></section>') +
      ('<section class="section"><div class="container" style="text-align:center">'
       '<span class="section__eyebrow">Precios por ciudad</span>'
       '<h2 class="section__title">Precios funerarios por localidad</h2>'
       '<p class="section__subtitle">Tarifas claras de incineración, entierro y traslados en su ciudad.</p>'
       '<p style="line-height:2.4">'
       + " · ".join(f'<a href="{L(px, "precios-funeraria-"+c["slug"]+"/")}">Precios en {c["name"]}</a>' for c in PRECIOS)
       + '</p></div></section>') +
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
        slug = z["slug"]
        tan_href = L(px, f"tanatorio-{slug}/")
        has_precios = any(p["slug"] == slug for p in PRECIOS)
        pre_href = L(px, f"precios-funeraria-{slug}/") if has_precios else L(px, "servicios/")
        pre_label = f"Precios funerarios en {name}" if has_precios else "Ver tarifas de servicios"
        zfaq = [
          (f"¿Qué hago si fallece un familiar en {name}?",
           f"Si es en casa, avise al médico o al 112 para el certificado. Si es en hospital o residencia, lo emite el centro. Después llámenos al {PHONE_DISP}: no está obligado a contratar la funeraria que le ofrezcan allí. Coordinamos recogida, tanatorio y trámites en {name}."),
          (f"¿Dónde se vela en {name}?",
           f"Le indicamos el recinto y reservamos sala. Detalle de dirección y cómo llegar: <a href=\"{tan_href}\">tanatorio en {name}</a>."),
          (f"¿Cuánto cuesta un servicio en {name}?",
           f"Incineración desde 1.500 €. El total depende de sala, tasas y si hay sepultura. <a href=\"{pre_href}\">{pre_label}</a>."),
          ("¿Atienden sin seguro de decesos?",
           "Sí. Es habitual. Presupuesto por escrito y, si lo necesita, facilidades de pago."),
        ]
        urgency = f'''<section class="urgency urgency--photo">
      <div class="container urgency__inner">
        <p class="urgency__flag">Asistencia inmediata en {name} · 24h</p>
        <h2 class="urgency__title">¿Ha fallecido un ser querido en {name}?</h2>
        <p class="urgency__text">Le atendemos ahora. Recogida, tanatorio y trámites en {name}. No está obligado a contratar la funeraria del hospital.</p>
        <a class="btn-call" href="tel:{PHONE_TEL}" data-track="urgency-call"><span class="btn-call__icon" aria-hidden="true">📞</span><span class="btn-call__label"><strong>LLAMAR AHORA · 24H</strong><small>{PHONE_DISP} — Le atendemos ya</small></span></a>
        <p class="urgency__note">Llamada de orientación gratuita · También le devolvemos la llamada</p>
      </div>
    </section>'''
        pasos = f'''<section class="section">
      <div class="container">
        <span class="section__eyebrow">Primeros pasos en {name}</span>
        <h2 class="section__title">Qué hacer ahora mismo</h2>
        <div class="steps" style="margin-top:26px">
          <article class="step"><div class="step__num">1</div><h3>Certificado</h3><p>En casa: médico o 112. En hospital o residencia de {name}: lo emite el centro.</p></article>
          <article class="step"><div class="step__num">2</div><h3>Elija funeraria</h3><p>Libertad de elección. Llámenos al {PHONE_DISP}. No firme en el hospital si no quiere.</p></article>
          <article class="step"><div class="step__num">3</div><h3>Nos ocupamos</h3><p>Recogida, sala, Registro Civil e incineración o entierro. Usted decide con calma.</p></article>
        </div>
      </div>
    </section>'''
        cobertura = f'''<section class="section section--alt">
      <div class="container">
        <span class="section__eyebrow">En {name}</span>
        <h2 class="section__title">Tanatorio, precios y trámites</h2>
        <div class="grid-3" style="margin-top:26px">
          <article class="card"><div class="card__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V7l7-4 7 4v14M9 21v-6h6v6"/></svg></div>
            <h3 class="card__title">Tanatorio</h3>
            <p class="card__text">Reservamos sala en {name} o en el recinto más cercano.</p>
            <p class="readmore" style="margin-top:12px"><a href="{tan_href}">Tanatorio en {name} →</a></p></article>
          <article class="card"><div class="card__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0l-7-7A2 2 0 0 1 3 12.2V4a1 1 0 0 1 1-1h8.2c.5 0 1 .2 1.4.6l7 7a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg></div>
            <h3 class="card__title">Precios</h3>
            <p class="card__text">Incineración desde 1.500 €. Tasas de {name} desglosadas.</p>
            <p class="readmore" style="margin-top:12px"><a href="{pre_href}">{pre_label} →</a></p></article>
          <article class="card"><div class="card__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6a1 1 0 0 1 1 1v1h2a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h2V4a1 1 0 0 1 1-1z"/><path d="M9 12h6M9 16h4"/></svg></div>
            <h3 class="card__title">Trámites</h3>
            <p class="card__text">Certificado, Registro Civil y licencias en {name}.</p>
            <p class="readmore" style="margin-top:12px"><a href="{L(px,'necesito-ayuda/')}">Guía de primeros pasos →</a></p></article>
        </div>
      </div>
    </section>'''
        local = f'''<section class="section">
      <div class="container media">
        <div class="media__img"><img src="{px}assets/camino-sereno.jpg" alt="Entorno sereno en {name}" loading="lazy" /></div>
        <div class="media__body">
          <span class="section__eyebrow" style="text-align:left">Servicio local</span>
          <h2>Cercanos a las familias de {name}</h2>
          <p>{z["intro"]}</p>
          <p>Atendemos fallecimientos en {z["landmarks"]}. {z["extra"]}</p>
        </div>
      </div>
    </section>'''
        body = (
          page_hero(f"Funeraria en {name} · 24 horas", z["hero_sub"],
                    image=CITY_HERO.get(slug, "assets/camino-sereno.jpg")) +
          urgency + pasos + cobertura + local +
          faq_block(f"Preguntas frecuentes · funeraria en {name}", zfaq) +
          lead_form(px, f"Pida orientación en {name}",
                    f"Situación no urgente o previsión. Le llamamos para {name}.")
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

    # ============================== TANATORIO EN [CIUDAD] ==============================
    for c in TANATORIO:
        route = f"tanatorio-{c['slug']}/"
        px = prefix_for(route)
        name = c["name"]
        tfaq = [
          (f"¿Dónde está el tanatorio de {name}?",
           (f"El recinto de referencia es {c.get('place')}: {c.get('addr')}. Coordinamos la sala y le confirmamos disponibilidad al momento en el {PHONE_DISP}."
            if c.get("addr") else
            f"En {name} coordinamos la sala de velatorio que mejor se adapte a su familia; llámenos al {PHONE_DISP} y le informamos de las opciones y la disponibilidad al momento.")),
          (f"¿Cuánto cuesta un velatorio en {name}?", "Depende de la sala, la duración y las prestaciones. Le ofrecemos un presupuesto cerrado y transparente; la incineración parte desde 1.500 €, siempre sin cargos ocultos."),
          (f"¿Atienden las 24 horas en {name}?", f"Sí. En {name} estamos disponibles las 24 horas, los 365 días del año. Ante un fallecimiento, le atendemos y coordinamos el traslado de inmediato."),
          ("¿Puedo elegir el tanatorio?", "Sí. Tiene total libertad para elegir la funeraria y el tanatorio, tanto si el fallecimiento se produce en el hospital como en una residencia o en el domicilio."),
        ]
        has_precios = any(p["slug"] == c["slug"] for p in PRECIOS)
        pre_href = L(px, f"precios-funeraria-{c['slug']}/") if has_precios else L(px, "servicios/")
        urg_t = f'''<section class="urgency urgency--photo">
      <div class="container urgency__inner">
        <p class="urgency__flag">Velatorio en {name} · 24h</p>
        <h2 class="urgency__title">¿Necesita reservar sala ahora?</h2>
        <p class="urgency__text">Confirmamos disponibilidad en el tanatorio de {name} y organizamos la recogida desde {c["hosp"]} o el domicilio.</p>
        <a class="btn-call" href="tel:{PHONE_TEL}" data-track="urgency-call"><span class="btn-call__icon" aria-hidden="true">📞</span><span class="btn-call__label"><strong>RESERVAR SALA · 24H</strong><small>{PHONE_DISP}</small></span></a>
        <p class="urgency__note">Le indicamos dirección y cómo llegar al recinto</p>
      </div>
    </section>'''
        lugar = f'''<section class="section">
      <div class="container media">
        <div class="media__img"><img src="{px}assets/blog-tanatorio.jpg" alt="Sala de velatorio en {name}" loading="lazy" /></div>
        <div class="media__body">
          <span class="section__eyebrow" style="text-align:left">El recinto</span>
          <h2>Dónde está el tanatorio de {name}</h2>
          <p><strong>{c.get("place", f"Tanatorio de {name}")}</strong><br>{c.get("addr", "")}</p>
          <p>{c.get("local", f"Coordinamos la sala de velatorio en {name} o en el recinto más cercano.")}</p>
          <ul class="media__list">
            <li>Recogida 24 h desde {c["hosp"]}</li>
            <li>Barrios: {c["barrios"]}</li>
            <li>Ceremonia religiosa o civil en sala</li>
            <li>Salida a crematorio o cementerio</li>
          </ul>
          <p style="margin-top:14px">
            <a href="{L(px, c['slug']+'/')}">Funeraria en {name} →</a><br>
            <a href="{pre_href}">Precios en {name} →</a>
          </p>
        </div>
      </div>
    </section>'''
        body = (
          page_hero(f"Tanatorio en {name}",
                    f"Dirección del recinto, cómo llegar y reserva de sala 24 h en {name}.",
                    image=TAN_HERO.get(c["slug"], "assets/blog-tanatorio.jpg")) +
          urg_t + lugar +
          faq_block(f"Tanatorio de {name}: dudas frecuentes", tfaq) +
          lead_form(px, f"Reserva de sala en {name}",
                    f"Indíquenos hospital o domicilio en {name} y le confirmamos sala.")
        )
        page(route,
             f"Tanatorio en {name} 24h | Velatorio y Servicios Funerarios",
             f"Tanatorio en {name} 24 horas: coordinamos sala de velatorio, incineración desde 1.500€, trámites y traslado. Atención inmediata y precios transparentes en {name}.",
             f"tanatorio {name}, tanatorio de {name}, velatorio {name}, funeraria {name}, sala velatorio {name}",
             body,
             [org_schema(),
              breadcrumb([("Inicio",""),("Zonas","zonas/"),(f"Tanatorio en {name}", route)]),
              {"@context":"https://schema.org","@type":"FuneralHome","name":f"{SITE_NAME} · Tanatorio en {name}",
               "areaServed":{"@type":"City","name":name},"telephone":PHONE_TEL,"url":BASE_URL+"/"+route,"priceRange":"€€"},
              faq_schema(tfaq)],
             og_image="assets/blog-tanatorio.jpg")
        routes.append(route)

    # ============================== PRECIOS FUNERARIOS POR CIUDAD ==============================
    for c in PRECIOS:
        route = f"precios-funeraria-{c['slug']}/"
        px = prefix_for(route); name = c["name"]
        pgrid = f'''<section class="section"><div class="container">
          <span class="section__eyebrow">Tarifas orientativas en {name}</span>
          <h2 class="section__title">Precios funerarios en {name}</h2>
          <p class="section__subtitle">Presupuesto cerrado y por escrito, sin cargos ocultos. Estas son las tarifas orientativas para {name}.</p>
          <div class="price-grid">
            <div class="price-card price-card--featured"><h3>Incineración</h3><p class="price-card__price"><small>Desde</small> 1.500€ <small>IVA incluido</small></p><ul><li>Recogida y traslado</li><li>Féretro para incineración</li><li>Trámites y licencia</li><li>Coordinación del crematorio</li><li>Urna básica</li></ul><a class="btn btn--primary btn--block" href="#formulario" data-track="precio-inci">Pedir presupuesto</a></div>
            <div class="price-card"><h3>Inhumación</h3><p class="price-card__price"><small>Desde</small> 2.900€ <small>sin sepultura</small></p><ul><li>Féretro de inhumación</li><li>Coche fúnebre</li><li>Trámites y licencia</li><li>Coordinación con el cementerio</li></ul><a class="btn btn--ghost btn--block" href="#formulario" data-track="precio-inhu">Pedir presupuesto</a></div>
            <div class="price-card"><h3>Traslado</h3><p class="price-card__price"><small>Desde</small> 900€ <small>nacional</small></p><ul><li>Traslado a otra localidad</li><li>Repatriación (a medida)</li><li>Gestión documental</li><li>Coordinación puerta a puerta</li></ul><a class="btn btn--ghost btn--block" href="#formulario" data-track="precio-tras">Pedir presupuesto</a></div>
          </div>
          <p class="price-note">Precios orientativos. El importe final depende de las prestaciones y de las tasas de {name}. Le entregamos siempre el presupuesto por escrito antes de contratar.</p>
        </div></section>'''
        info = f'''<section class="section section--alt">
      <div class="container">
        <span class="section__eyebrow">En {name}</span>
        <h2 class="section__title">Qué está incluido (y qué no)</h2>
        <p class="section__subtitle">{c.get("local", f"En {name} el importe final depende del tipo de despedida, la sala y las tasas municipales.")}</p>
        <div class="grid-3">
          <article class="card"><h3 class="card__title">Incineración sin seguro</h3><p class="card__text">Desde 1.500 €: recogida, féretro de incineración, trámites y urna básica. Sala y tasa de crematorio, aparte si las hay.</p></article>
          <article class="card"><h3 class="card__title">Entierro con nicho propio</h3><p class="card__text">Desde 2.900 € más tasas del cementerio de {name}. Sin compra de sepultura nueva.</p></article>
          <article class="card"><h3 class="card__title">Hospital + velatorio</h3><p class="card__text">Se suma la sala. Cifra cerrada por escrito antes de reservar en {name}.</p></article>
        </div>
        <p class="price-note">No incluido en el «desde»: tasas municipales, horas extra de sala, flores, esquelas y urna distinta de la básica. <a href="{L(px,'blog/ayudas-gastos-funerarios/')}">Ayudas para gastos funerarios</a> · <a href="{L(px, c['slug']+'/')}">Funeraria en {name}</a> · <a href="{L(px, 'tanatorio-'+c['slug']+'/')}">Tanatorio</a></p>
      </div>
    </section>'''
        pfaq = [
          (f"¿Cuánto cuesta una incineración en {name}?", "La incineración parte desde 1.500 €, con trámites incluidos y presupuesto cerrado por escrito."),
          (f"¿Cuánto cuesta un entierro en {name}?", "La inhumación parte desde 2.900 € (sin contar la sepultura). Le detallamos cada concepto, sin cargos ocultos."),
          (f"¿Hay ayudas para pagar el funeral en {name}?", "Sí: el auxilio por defunción de la Seguridad Social y ayudas de servicios sociales. Le orientamos sobre cuáles puede solicitar."),
          ("¿Puedo pagar a plazos?", "Sí, ofrecemos opciones de financiación, especialmente para familias sin seguro de decesos."),
        ]
        body = (page_hero(f"Precios funerarios en {name}", f"Tarifas claras de incineración, entierro y traslados en {name}. Presupuesto por escrito y sin cargos ocultos.",
                    image=PRECIO_HERO.get(c["slug"], "assets/blog-ayudas.jpg"))
                + pgrid + info + cta_band(px)
                + faq_block(f"Preguntas sobre precios en {name}", pfaq)
                + lead_form(px, f"Pida su presupuesto en {name}", f"Cuéntenos qué necesita y le preparamos un presupuesto claro para {name}, sin compromiso."))
        page(route,
             f"Precios Funerarios en {name} | Incineración desde 1.500€ y Entierro",
             f"Precios funerarios en {name}: incineración desde 1.500€, inhumación desde 2.900€ y traslados. Presupuesto por escrito, sin cargos ocultos y con ayudas si las necesita.",
             f"precios funeraria {name}, incineración {name} precio, coste entierro {name}, cuánto cuesta un funeral {name}",
             body,
             [org_schema(),
              breadcrumb([("Inicio",""),("Zonas","zonas/"),(f"Precios en {name}", route)]),
              {"@context":"https://schema.org","@type":"Service","name":f"Servicios funerarios en {name}","areaServed":{"@type":"City","name":name},"provider":{"@type":"FuneralHome","name":SITE_NAME},"offers":{"@type":"Offer","price":"1500","priceCurrency":"EUR"}},
              faq_schema(pfaq)])
        routes.append(route)

    # ============================== NECESITO AYUDA ==============================
    px = prefix_for("necesito-ayuda/")
    def acc(title, pairs):
        items = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in pairs)
        return f'<h2 class="help-h2">{title}</h2><div class="faq">{items}</div>'

    help_body = (
      page_hero("Necesito ayuda","Respuestas claras a las dudas más frecuentes en un momento difícil.",
                image="assets/blog-fallecimiento.jpg",
                actions='<a class="btn btn--primary btn--xl" href="#llamamos">Te guiamos paso a paso</a>') +
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
      cta_band(px, "¿Prefiere que le llamemos?", section_id="llamamos") +
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
      page_hero("Blog · Guías y consejos","Información útil y cercana para acompañarle en cada situación.",
                image="assets/blog-duelo.jpg") +
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
      page_hero("Contacto","Estamos a su lado las 24 horas. Llámenos o escríbanos.",
                image="assets/equipo.jpg",
                actions=BTN_CALL) +
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
            <li><span class="ico">📍</span><div><strong>Zona</strong><br>{address_line()}</div></li>
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
             [org_schema(), breadcrumb([("Inicio",""),(h1,route)])],
             robots="noindex, follow")
        routes.append(route)

    aviso = f'''
      <p><em>Última actualización: {YEAR}. ⚠ Datos del titular pendientes de completar.</em></p>
      <h2>1. Datos identificativos</h2>
      <p>En cumplimiento de la Ley 34/2002 (LSSI-CE), se informa de que este sitio web es titularidad de:</p>
      <ul>
        <li><strong>Titular:</strong> {LEGAL_NAME}</li>
        <li><strong>NIF/CIF:</strong> {LEGAL_NIF}</li>
        <li><strong>Domicilio:</strong> {address_line()}</li>
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
    # Excluir del sitemap las páginas legales (no interesa priorizar su indexación)
    EXCLUDE = {"aviso-legal/", "privacidad/", "cookies/"}
    urls=[]
    for r in routes:
        if r in EXCLUDE:
            continue
        loc = BASE_URL + "/" + r
        pr = "1.0" if r=="" else ("0.9" if r in ("servicios/","zonas/","contacto/") else "0.7")
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority></url>")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    with open(os.path.join(OUT,"sitemap.xml"),"w",encoding="utf-8") as f: f.write(sitemap)

    robots = f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n"
    with open(os.path.join(OUT,"robots.txt"),"w",encoding="utf-8") as f: f.write(robots)

    with open(os.path.join(OUT,"CNAME"),"w",encoding="utf-8") as f: f.write("serviciosfunerarios24h.es\n")

    # ---- FEED RSS (blog) ----
    import email.utils, datetime as _dt
    def rfc822(datestr):
        try:
            d = _dt.datetime.strptime(datestr, "%Y-%m-%d").replace(hour=9, tzinfo=_dt.timezone.utc)
        except Exception:
            d = _dt.datetime.now(_dt.timezone.utc)
        return email.utils.format_datetime(d)
    def esc(s):
        return (s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))
    items = []
    for p in BLOG_POSTS:
        link = f"{BASE_URL}/blog/{p['slug']}/"
        items.append(
            "    <item>\n"
            f"      <title>{esc(p['title'])}</title>\n"
            f"      <link>{link}</link>\n"
            f"      <guid isPermaLink=\"true\">{link}</guid>\n"
            f"      <pubDate>{rfc822(p['date'])}</pubDate>\n"
            f"      <description>{esc(p['description'])}</description>\n"
            "    </item>")
    feed = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0"><channel>\n'
            f"  <title>Blog · {SITE_NAME}</title>\n"
            f"  <link>{BASE_URL}/blog/</link>\n"
            f"  <description>Guías y consejos funerarios en Móstoles y el sur de Madrid.</description>\n"
            "  <language>es-ES</language>\n"
            f"  <lastBuildDate>{email.utils.format_datetime(_dt.datetime.now(_dt.timezone.utc))}</lastBuildDate>\n"
            + "\n".join(items) + "\n</channel></rss>\n")
    with open(os.path.join(OUT,"feed.xml"),"w",encoding="utf-8") as f: f.write(feed)

    print(f"Total rutas: {len(routes)}  ->  sitemap.xml, robots.txt, feed.xml y CNAME generados.")
