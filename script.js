/* =========================================================
   serviciosfunerarios24h.es — script.js
   Captura de leads + Call Tracking + navegación + chat IA
   Vanilla JavaScript · sin dependencias
   ========================================================= */

(function () {
  "use strict";

  /* ---------- Año dinámico en el footer ---------- */
  var yearEl = document.getElementById("year");
  if (yearEl) { yearEl.textContent = new Date().getFullYear(); }

  /* ---------- Detección de zona según la página ---------- */
  function getZona() {
    var path = window.location.pathname.toLowerCase();
    if (path.indexOf("/mostoles") !== -1) { return "Móstoles"; }
    if (path.indexOf("/alcorcon") !== -1) { return "Alcorcón"; }
    if (path.indexOf("/fuenlabrada") !== -1) { return "Fuenlabrada"; }
    if (path.indexOf("/leganes") !== -1) { return "Leganés"; }
    if (path.indexOf("/getafe") !== -1) { return "Getafe"; }
    if (path.indexOf("/arroyomolinos") !== -1) { return "Arroyomolinos"; }
    if (path.indexOf("/villaviciosa") !== -1) { return "Villaviciosa de Odón"; }
    if (path.indexOf("/toledo") !== -1) { return "Toledo"; }
    if (path.indexOf("/madrid") !== -1) { return "Madrid"; }
    return "Madrid Sur";
  }
  var ZONA = getZona();

  /* =========================================================
     1) CALL TRACKING PROPIO + REPARTO INTERNO
     ========================================================= */
  var PARTNERS = {
    "Móstoles":   ["ayb-servicios", "el-recuerdo", "montero"],
    "Madrid Sur": ["ayb-servicios", "el-recuerdo"]
  };
  function asignarPartner(zona) {
    var pool = PARTNERS[zona] || PARTNERS["Madrid Sur"];
    var key = "sf24_rr_" + zona;
    var idx = 0;
    try {
      idx = parseInt(window.localStorage.getItem(key) || "0", 10) || 0;
      window.localStorage.setItem(key, String((idx + 1) % pool.length));
    } catch (e) {}
    return pool[idx % pool.length];
  }
  function getSource() {
    try {
      var params = new URLSearchParams(window.location.search);
      return params.get("utm_source") || "seo-organico";
    } catch (e) { return "seo-organico"; }
  }
  function trackEvent(action, extra) {
    var payload = { event: "conversion", action: action, zona: ZONA,
      timestamp: new Date().toISOString(), page: window.location.pathname, source: getSource() };
    if (extra) { Object.keys(extra).forEach(function (k) { payload[k] = extra[k]; }); }
    console.log("📊 [TRACKING]", payload);
    return payload;
  }
  var trackables = document.querySelectorAll("[data-track]");
  trackables.forEach(function (el) {
    el.addEventListener("click", function () {
      var action = el.getAttribute("data-track");
      var href = el.getAttribute("href") || "";
      var isCall = href.indexOf("tel:") === 0;
      var extra = { type: isCall ? "click_to_call" : "cta_click" };
      if (isCall) {
        extra.phone = href.replace("tel:", "");
        extra.partnerAsignado = asignarPartner(ZONA);
        console.log("☎️ [REPARTO LLAMADA] Zona " + ZONA + " → " + extra.partnerAsignado);
      }
      trackEvent(action, extra);
    });
  });

  /* =========================================================
     2) LÓGICA DEL FORMULARIO
     ========================================================= */
  var form = document.getElementById("leadForm");
  var successBox = document.getElementById("formSuccess");
  if (!form) { return; }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    clearErrors();
    var lead = {
      tipoServicio: getVal("tipoServicio"),
      ubicacion: getVal("ubicacion"),
      sepultura: getRadio("sepultura"),
      nombre: getVal("nombre"),
      telefono: getVal("telefono"),
      rgpd: document.getElementById("rgpd").checked,
      meta: { capturadoEn: new Date().toISOString(), fuente: getSource(), zona: ZONA }
    };
    var errors = validate(lead);
    if (errors.length > 0) {
      errors.forEach(function (name) { markError(name); });
      focusFirstError(errors[0]);
      return;
    }
    lead.meta.partnerAsignado = asignarPartner(ZONA);
    trackEvent("lead_form_submit", { type: "form_lead", tipoServicio: lead.tipoServicio,
      sepultura: lead.sepultura, partner: lead.meta.partnerAsignado });
    console.log("✅ [LEAD CAPTURADO]", JSON.stringify(lead, null, 2));
    sendToGoogleForms(lead);
    showSuccess(lead.nombre);
    Array.prototype.forEach.call(form.elements, function (el) {
      if (el.type !== "hidden") { el.style.display = "none"; }
    });
    var legal = form.querySelector(".lead-form__legal");
    if (legal) { legal.style.display = "none"; }
  });

  /* ---------- BACKEND: envío oculto a Google Forms ---------- */
  var GFORM_CONFIG = {
    action: "",  // "https://docs.google.com/forms/d/e/1FAIpQLSxxxx/formResponse"
    entries: {
      tipoServicio: "", ubicacion: "", sepultura: "",
      nombre: "", telefono: "", zona: "", fuente: ""
    }
  };
  function sendToGoogleForms(lead) {
    if (!GFORM_CONFIG.action) {
      console.log("ℹ️ Google Forms no configurado todavía (GFORM_CONFIG.action vacío).");
      return;
    }
    var fd = new FormData(); var E = GFORM_CONFIG.entries;
    if (E.tipoServicio) fd.append(E.tipoServicio, lead.tipoServicio);
    if (E.ubicacion)    fd.append(E.ubicacion,    lead.ubicacion);
    if (E.sepultura)    fd.append(E.sepultura,    lead.sepultura);
    if (E.nombre)       fd.append(E.nombre,       lead.nombre);
    if (E.telefono)     fd.append(E.telefono,     lead.telefono);
    if (E.zona)         fd.append(E.zona,         lead.meta.zona);
    if (E.fuente)       fd.append(E.fuente,       lead.meta.fuente);
    fetch(GFORM_CONFIG.action, { method: "POST", mode: "no-cors", body: fd })
      .then(function () { console.log("📨 Lead enviado a Google Forms."); })
      .catch(function (err) { console.warn("Fallo al enviar a Google Forms:", err); });
  }

  /* ---------- Helpers ---------- */
  function getVal(id) { var el = document.getElementById(id); return el ? el.value.trim() : ""; }
  function getRadio(name) {
    var c = form.querySelector('input[name="' + name + '"]:checked');
    return c ? c.value : "";
  }
  function validate(lead) {
    var errors = [];
    if (!lead.tipoServicio) { errors.push("tipoServicio"); }
    if (!lead.ubicacion) { errors.push("ubicacion"); }
    if (!lead.sepultura) { errors.push("sepultura"); }
    if (!lead.nombre) { errors.push("nombre"); }
    var digits = (lead.telefono || "").replace(/\D/g, "");
    if (digits.length < 9) { errors.push("telefono"); }
    if (!lead.rgpd) { errors.push("rgpd"); }
    return errors;
  }
  function markError(fieldName) {
    if (fieldName === "sepultura") {
      form.querySelectorAll(".field--radio .radio").forEach(function (r) { r.classList.add("invalid"); });
      return;
    }
    if (fieldName === "rgpd") {
      var c = form.querySelector(".consent");
      if (c) { c.classList.add("invalid"); }
      return;
    }
    var el = document.getElementById(fieldName);
    if (el) { el.classList.add("invalid"); }
  }
  function clearErrors() {
    form.querySelectorAll(".invalid").forEach(function (el) { el.classList.remove("invalid"); });
  }
  function focusFirstError(fieldName) {
    var el = document.getElementById(fieldName);
    if (el && typeof el.focus === "function") { el.focus(); }
  }
  function showSuccess(nombre) {
    if (!successBox) { return; }
    var saludo = nombre ? nombre.split(" ")[0] : "";
    successBox.innerHTML =
      '<span class="form-success__ico" aria-hidden="true">🕊️</span>' +
      '<h3>Solicitud recibida' + (saludo ? ", " + escapeHtml(saludo) : "") + '</h3>' +
      '<p>Gracias por confiar en nosotros en un momento tan delicado.</p>' +
      '<p>Le contactaremos <strong>en pocos minutos</strong> por teléfono o WhatsApp para ' +
      'atenderle con calma, sin ningún compromiso.</p>' +
      '<p>Si prefiere atención inmediata, puede llamarnos ahora al ' +
      '<a href="tel:+34910000000">910 000 000</a>.</p>';
    successBox.hidden = false;
    successBox.scrollIntoView({ behavior: "smooth", block: "center" });
  }
  function escapeHtml(str) {
    return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  form.addEventListener("input", function (e) {
    if (e.target.classList) { e.target.classList.remove("invalid"); }
  });
  form.addEventListener("change", function (e) {
    if (e.target.name === "sepultura") {
      form.querySelectorAll(".field--radio .radio").forEach(function (r) { r.classList.remove("invalid"); });
    }
    if (e.target.id === "rgpd") {
      var c = form.querySelector(".consent");
      if (c) { c.classList.remove("invalid"); }
    }
  });
})();

/* =========================================================
   NAVEGACIÓN MÓVIL (menú hamburguesa)
   ========================================================= */
(function () {
  "use strict";
  var toggle = document.getElementById("navToggle");
  var menu = document.getElementById("navMenu");
  if (!toggle || !menu) { return; }
  toggle.addEventListener("click", function () {
    var open = menu.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  });
  menu.querySelectorAll("a").forEach(function (a) {
    a.addEventListener("click", function () {
      menu.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });
})();

/* =========================================================
   CHAT IA (Gemma · Google AI Studio)
   - Responde SOLO sobre la funeraria y sus servicios.
   - Personas por horario: Paula / Carlos / Susana.
   - Cadencia humana 20-30 s por respuesta, máx. 3/min.
   ========================================================= */
(function () {
  "use strict";
  var fab = document.getElementById("chatFab");
  var panel = document.getElementById("chatPanel");
  var closeBtn = document.getElementById("chatClose");
  var form = document.getElementById("chatForm");
  var input = document.getElementById("chatText");
  var body = document.getElementById("chatBody");
  if (!fab || !panel || !form) { return; }

  /* ------------------------------------------------------------------
     CONFIGURACIÓN
     ⚠ SEGURIDAD: la API key va en el navegador y es visible en el código
     fuente. Es aceptable para la capa gratuita, pero cualquiera podría
     usarla. Recomendado: restringir la key en Google Cloud o usar un
     pequeño proxy propio. Revócala/rótala si detectas uso indebido.
     ------------------------------------------------------------------ */
  var CHAT_CONFIG = {
    // Opción A (RECOMENDADA y segura): proxy propio (Cloudflare Worker) que guarda la
    // API key en el servidor. Así la clave NUNCA aparece en el navegador.
    proxyUrl: "",   // p.ej. "https://chat-sf24.tuusuario.workers.dev"
    // Opción B (rápida, MENOS segura): key directa en el navegador (será pública).
    // No la pongas aquí: colócala en /chat-config.json (ver más abajo) bajo tu responsabilidad.
    apiKey: "",
    model: "gemma-4-31b-it",   // si el ID no existe, se auto-corrige al Gemma disponible
    endpoint: "https://generativelanguage.googleapis.com/v1beta/",
    // Base de conocimiento: fichero de texto editable en la raíz del sitio.
    knowledgeBaseUrl: "/chat-kb.txt",
    knowledgeBase: [
      "Servicios Funerarios 24h atiende Móstoles y el sur de Madrid las 24 horas.",
      "Ofrecemos incineración desde 1.500€, inhumación desde 2.900€ y traslados.",
      "Teléfono de contacto 24h: 910 000 000.",
      "Trabajamos con familias con y sin seguro de decesos, con opciones de financiación.",
      "Nos encargamos de todos los trámites: certificado, Registro Civil y licencias."
    ].join(" "),
    // Cadencia humana y límite de ritmo
    minDelayMs: 20000,   // 20 s mínimo por respuesta
    maxDelayMs: 30000,   // 30 s máximo
    maxPerMinute: 3,     // como máximo 3 respuestas de la IA por minuto
    // Identidades por franja horaria
    agents: [
      { name: "Paula",  from: 6,  to: 14 },
      { name: "Carlos", from: 14, to: 22 },
      { name: "Susana", from: 22, to: 6  }
    ]
  };

  /* ---------- Persona activa según la hora ---------- */
  function agentName() {
    var h = new Date().getHours();
    var ag = CHAT_CONFIG.agents;
    for (var i = 0; i < ag.length; i++) {
      var a = ag[i];
      if (a.from < a.to) { if (h >= a.from && h < a.to) return a.name; }
      else { if (h >= a.from || h < a.to) return a.name; } // franja que cruza medianoche
    }
    return "Nuestro equipo";
  }

  /* ---------- Base de conocimiento (carga desde fichero) ---------- */
  var kbCache = null;
  async function loadKB() {
    if (kbCache !== null) { return kbCache; }
    kbCache = CHAT_CONFIG.knowledgeBase || "";
    if (CHAT_CONFIG.knowledgeBaseUrl) {
      try {
        var r = await fetch(CHAT_CONFIG.knowledgeBaseUrl, { cache: "no-store" });
        if (r.ok) { var t = await r.text(); if (t && t.trim()) { kbCache = t.trim(); } }
      } catch (e) {}
    }
    return kbCache;
  }

  /* ---------- Respuestas locales (si la API falla / no hay key) ---------- */
  var LOCAL_FAQ = [
    { k: ["precio","cuesta","cuánto","cuanto","tarifa","incinera","cremaci"],
      a: "Ofrecemos incineración desde 1.500€ e inhumación desde 2.900€, siempre con presupuesto cerrado y sin cargos ocultos. ¿Quiere que le preparemos uno sin compromiso? Puede llamarnos al 910 000 000." },
    { k: ["24","hora","noche","ahora","urg","fallec","muerto","murió","murio"],
      a: "Sí, atendemos las 24 horas, los 365 días del año. Si acaba de producirse un fallecimiento, lo mejor es llamarnos ahora mismo al 910 000 000 y le orientamos de inmediato." },
    { k: ["seguro","decesos","póliza","poliza"],
      a: "Trabajamos con y sin seguro de decesos. Si tiene póliza, la revisamos gratis; y recuerde que puede elegirnos aunque el seguro sea de otra compañía." },
    { k: ["trámite","tramite","papeleo","registro","certificado","document"],
      a: "Nos encargamos de todos los trámites urgentes: certificado de defunción, inscripción en el Registro Civil y licencias. También le orientamos sobre pensiones y herencias." },
    { k: ["zona","mostoles","móstoles","alcorc","fuenlab","legan","getafe","arroyo","dónde","donde"],
      a: "Damos servicio en Móstoles, Alcorcón, Fuenlabrada, Leganés, Getafe, Arroyomolinos y todo el sur de Madrid. ¿En qué localidad se encuentra?" }
  ];
  function localAnswer(text) {
    var t = (text || "").toLowerCase();
    // Despedidas / agradecimientos: respuesta humana y variada
    if (/(gracias|nada m[aá]s|hasta luego|adi[oó]s|un saludo|buenas noches|eso es todo|de acuerdo|vale$|okay|ok$|perfecto)/.test(t)) {
      return pickVaried([
        "Gracias a usted. Quedamos a su entera disposición para lo que necesite. Un fuerte abrazo.",
        "A usted. Si más adelante necesita cualquier cosa, aquí estaremos, día y noche. Cuídese mucho.",
        "Ha sido un placer ayudarle. No dude en escribirnos cuando lo desee. Le deseamos lo mejor.",
        "Estamos a su lado para lo que haga falta. Le mando un saludo muy cordial."
      ]);
    }
    for (var i = 0; i < LOCAL_FAQ.length; i++) {
      for (var j = 0; j < LOCAL_FAQ[i].k.length; j++) {
        if (t.indexOf(LOCAL_FAQ[i].k[j]) !== -1) { return LOCAL_FAQ[i].a; }
      }
    }
    // Respuesta por defecto: variada (nunca la misma dos veces seguidas)
    return pickVaried([
      "Con mucho gusto le ayudo. ¿Puede contarme un poco más? Si lo prefiere, también estamos en el 910 000 000, las 24 horas.",
      "Estoy aquí para ayudarle con lo que necesite sobre nuestros servicios. ¿En qué puedo orientarle?",
      "Claro, dígame en qué puedo ayudarle. Si en algún momento lo prefiere, puede llamarnos al 910 000 000.",
      "Por supuesto. Cuénteme qué necesita y le oriento con mucho gusto."
    ]);
  }
  var _lastLocal = "";
  function pickVaried(arr) {
    var opts = arr.filter(function (x) { return x !== _lastLocal; });
    var chosen = opts[Math.floor(Math.random() * opts.length)] || arr[0];
    _lastLocal = chosen;
    return chosen;
  }

  /* ---------- Llamadas a la API (key o token Bearer) ---------- */
  function isApiKey() { return CHAT_CONFIG.apiKey && CHAT_CONFIG.apiKey.indexOf("AIza") === 0; }
  function apiUrl(path) {
    var u = CHAT_CONFIG.endpoint + path;
    if (isApiKey()) { u += (u.indexOf("?") > -1 ? "&" : "?") + "key=" + CHAT_CONFIG.apiKey; }
    return u;
  }
  function apiHeaders() {
    var h = { "Content-Type": "application/json" };
    if (CHAT_CONFIG.apiKey && !isApiKey()) { h["Authorization"] = "Bearer " + CHAT_CONFIG.apiKey; }
    return h;
  }
  async function listGemmaModel() {
    try {
      var r = await fetch(apiUrl("models"), { headers: apiHeaders() });
      var d = await r.json();
      if (d && d.models) {
        var gs = d.models.filter(function (m) {
          return m.name.indexOf("gemma") > -1 &&
                 (m.supportedGenerationMethods || []).indexOf("generateContent") > -1;
        });
        gs.sort(function (a, b) { return b.name.length - a.name.length; });
        if (gs.length) { return gs[0].name.replace("models/", ""); }
      }
    } catch (e) {}
    return null;
  }

  /* ---------- Configuración en tiempo de ejecución (opcional) ---------- */
  // Permite definir proxyUrl / apiKey / model sin tocar el código, en /chat-config.json
  var cfgLoaded = false;
  async function loadRuntimeConfig() {
    if (cfgLoaded) { return; }
    cfgLoaded = true;
    try {
      var r = await fetch("/chat-config.json", { cache: "no-store" });
      if (r.ok) {
        var c = await r.json();
        if (c.proxyUrl) { CHAT_CONFIG.proxyUrl = c.proxyUrl; }
        if (c.apiKey)   { CHAT_CONFIG.apiKey   = c.apiKey; }
        if (c.model)    { CHAT_CONFIG.model    = c.model; }
      }
    } catch (e) {}
  }

  async function askGemma(userText) {
    await loadRuntimeConfig();
    if (!CHAT_CONFIG.apiKey && !CHAT_CONFIG.proxyUrl) { return localAnswer(userText); }
    var kb = await loadKB();
    var name = agentName();
    var prompt =
      "Eres " + name + ", asesor/a de la funeraria \"Servicios Funerarios 24h\" (Madrid Sur). " +
      "Hablas en español, con un tono humano, cercano, empático y breve (2 a 4 frases). " +
      "Responde SIEMPRE en español, aunque el cliente escriba en otro idioma. " +
      "REGLA ESTRICTA: solo puedes hablar sobre esta funeraria y sus servicios (precios, zonas, " +
      "trámites, incineración, inhumación, traslados, tanatorio, seguros de decesos, previsión) " +
      "basándote ÚNICAMENTE en la INFORMACIÓN de abajo. Si te preguntan sobre cualquier otro tema " +
      "ajeno a la funeraria (política, deportes, tecnología, etc.), responde amablemente que solo " +
      "puedes ayudar con temas relacionados con nuestros servicios funerarios y no facilites ninguna " +
      "otra información. No inventes datos que no aparezcan en la INFORMACIÓN; si no lo sabes, invita " +
      "a llamar al 910 000 000. " +
      "Si el cliente se despide, da las gracias o dice que no necesita nada más, respóndele con una " +
      "despedida cálida y humana (agradece, ofrécete para lo que necesite), variando las palabras y " +
      "SIN repetir siempre la misma frase ni forzar que llame por teléfono. " +
      "FORMATO OBLIGATORIO: razona lo mínimo y escribe tu respuesta final para el cliente ENVUELTA " +
      "entre las etiquetas <R> y </R>. Dentro de <R>...</R> pon SOLO el mensaje para el cliente, sin " +
      "tu razonamiento.\n\nINFORMACIÓN:\n" + kb + "\n\nMensaje del cliente: " + userText;

    // Opción A: proxy propio (la key vive en el servidor, no aquí)
    if (CHAT_CONFIG.proxyUrl) {
      try {
        var pr = await fetch(CHAT_CONFIG.proxyUrl, {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt: prompt })
        });
        var pd = await pr.json();
        return (pd && pd.text && pd.text.trim()) ? pd.text.trim() : localAnswer(userText);
      } catch (e) { console.warn("Chat: fallo proxy, respuesta local.", e); return localAnswer(userText); }
    }

    // Opción B: llamada directa con key en el navegador
    function call(model) {
      return fetch(apiUrl("models/" + model + ":generateContent"), {
        method: "POST", headers: apiHeaders(),
        body: JSON.stringify({
          contents: [{ role: "user", parts: [{ text: prompt }] }],
          generationConfig: { temperature: 0.6, maxOutputTokens: 400 }
        })
      });
    }
    try {
      var res = await call(CHAT_CONFIG.model);
      if (res.status === 404) {                    // ID de modelo incorrecto -> auto-resolver
        var alt = await listGemmaModel();
        if (alt) { CHAT_CONFIG.model = alt; console.info("Chat: usando modelo " + alt); res = await call(alt); }
      }
      var data = await res.json();
      if (data && data.error) { console.warn("Chat API:", data.error.message); return localAnswer(userText); }
      var out = data && data.candidates && data.candidates[0] &&
                data.candidates[0].content && data.candidates[0].content.parts &&
                data.candidates[0].content.parts[0].text;
      return (out && out.trim()) ? out.trim() : localAnswer(userText);
    } catch (e) {
      console.warn("Chat: fallo API, respuesta local.", e);
      return localAnswer(userText);
    }
  }

  /* ---------- UI del chat ---------- */
  function sanitizeReply(t) {
    if (!t) { return t; }
    // 1) Prioriza el contenido entre <R> y </R>
    var tags = t.match(/<R>([\s\S]*?)<\/R>/ig);
    if (tags && tags.length) {
      var inner = tags[tags.length - 1].replace(/<\/?R>/ig, "").trim();
      if (inner) { return inner; }
    }
    var open = t.toLowerCase().lastIndexOf("<r>");
    if (open > -1) {
      var after = t.slice(open + 3).replace(/<\/?R>/ig, "").trim();
      if (after) { return after; }
    }
    // 2) Sin etiquetas: recupera el último "borrador/draft"
    var drafts = t.match(/(?:draft|borrador)\s*\d*\s*:?\*?\s*(.+)/ig);
    if (drafts && drafts.length) {
      var last = drafts[drafts.length - 1]
        .replace(/^[\s\S]*?(?:draft|borrador)\s*\d*\s*:?\*?\s*/i, "")
        .replace(/[*"]/g, "").trim();
      if (last) { return last; }
    }
    // 3) Heurística final
    if (/persona:|constraint:|\byes\.\b|^\s*\*/im.test(t)) {
      var lines = t.split(/\n/).map(function (s) { return s.replace(/[*]/g, "").trim(); }).filter(Boolean);
      for (var i = lines.length - 1; i >= 0; i--) {
        if (/^(hola|buenos|buenas|gracias|le invito|estamos|el (precio|coste|servicio)|s[ií] )/i.test(lines[i]) && lines[i].length > 15) {
          return lines[i].replace(/^["']|["']$/g, "").trim();
        }
      }
    }
    return t.trim();
  }
  function addMsg(text, who) {
    var el = document.createElement("div");
    el.className = "chat-msg chat-msg--" + who;
    el.textContent = text;
    body.appendChild(el);
    body.scrollTop = body.scrollHeight;
    return el;
  }
  function showTyping(name) {
    var el = document.createElement("div");
    el.className = "chat-msg chat-msg--bot chat-typing";
    var span = document.createElement("span");
    span.className = "chat-typing__name";
    span.textContent = name + " está escribiendo";
    var dots = document.createElement("span");
    dots.className = "chat-typing__dots";
    dots.innerHTML = "<i></i><i></i><i></i>";
    el.appendChild(span); el.appendChild(dots);
    body.appendChild(el);
    body.scrollTop = body.scrollHeight;
    return el;
  }
  function setInputEnabled(on) {
    input.disabled = !on;
    var btn = form.querySelector("button");
    if (btn) { btn.disabled = !on; }
    input.placeholder = on ? "Escriba su duda…" : "Un momento, le respondo…";
  }

  /* ---------- Cadencia + límite de ritmo ---------- */
  var responseTimes = [];   // marcas de tiempo de respuestas de la IA
  var pending = false;
  var firstReply = true;    // el primer mensaje tiene tiempos especiales
  function computeDelay() {
    var now = Date.now();
    var base = CHAT_CONFIG.minDelayMs + Math.random() * (CHAT_CONFIG.maxDelayMs - CHAT_CONFIG.minDelayMs);
    var target = now + base;
    responseTimes = responseTimes.filter(function (t) { return now - t < 60000; });
    if (responseTimes.length >= CHAT_CONFIG.maxPerMinute) {
      var oldest = responseTimes[responseTimes.length - CHAT_CONFIG.maxPerMinute];
      target = Math.max(target, oldest + 60000);   // respeta el máx/min
    }
    return target - now;
  }

  var greeted = false;
  function openPanel() {
    panel.classList.add("is-open");
    fab.setAttribute("aria-expanded", "true");
    if (!greeted) {
      addMsg("Hola, soy " + agentName() + ", de Servicios Funerarios 24h. ¿En qué puedo ayudarle? Estamos disponibles las 24 horas.", "bot");
      greeted = true;
    }
    setTimeout(function () { if (!input.disabled) { input.focus(); } }, 100);
  }
  function closePanel() {
    panel.classList.remove("is-open");
    fab.setAttribute("aria-expanded", "false");
  }
  fab.addEventListener("click", function () {
    panel.classList.contains("is-open") ? closePanel() : openPanel();
  });
  if (closeBtn) { closeBtn.addEventListener("click", closePanel); }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (pending) { return; }
    var text = input.value.trim();
    if (!text) { return; }
    addMsg(text, "user");
    input.value = "";
    pending = true;
    setInputEnabled(false);

    var replyPromise = askGemma(text);   // se pide ya; se muestra con cadencia humana

    // Primer mensaje: "escribiendo" a los 15 s y respuesta a los 20 s.
    // A partir de ahí: cadencia habitual 20-30 s (máx. 3/min).
    var typingDelay, replyDelay;
    if (firstReply) { typingDelay = 15000; replyDelay = 20000; }
    else { typingDelay = 0; replyDelay = computeDelay(); }

    var typingEl = null;
    var typingTimer = setTimeout(function () { typingEl = showTyping(agentName()); }, typingDelay);

    setTimeout(function () {
      replyPromise.then(function (reply) {
        clearTimeout(typingTimer);
        if (typingEl && typingEl.parentNode) { typingEl.parentNode.removeChild(typingEl); }
        addMsg(sanitizeReply(reply), "bot");
        responseTimes.push(Date.now());
        firstReply = false;
        pending = false;
        setInputEnabled(true);
        input.focus();
      });
    }, replyDelay);
  });
})();
