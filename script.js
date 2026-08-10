/* =========================================================
   serviciosfunerarios24h.es — script.js
   Captura de leads + simulación de Call Tracking propio
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
    return "Madrid Sur";
  }
  var ZONA = getZona();

  /* =========================================================
     1) SIMULACIÓN DE CALL TRACKING PROPIO
     El número del Hero es un número PROPIO trackeado. Nosotros
     controlamos el reparto de la llamada entre las funerarias
     colaboradoras (rotación / por zona / disponibilidad).
     En producción esto lo gestiona el proveedor de call tracking
     y una centralita; aquí solo simulamos el registro y el reparto.
     ========================================================= */

  // Cartera de funerarias colaboradoras (demo). En real vendría de un backend.
  var PARTNERS = {
    "Móstoles":   ["ayb-servicios", "el-recuerdo", "montero"],
    "Madrid Sur": ["ayb-servicios", "el-recuerdo"]
  };

  // Reparto por rotación simple (round-robin) persistido en el navegador
  function asignarPartner(zona) {
    var pool = PARTNERS[zona] || PARTNERS["Madrid Sur"];
    var key = "sf24_rr_" + zona;
    var idx = 0;
    try {
      idx = parseInt(window.localStorage.getItem(key) || "0", 10) || 0;
      window.localStorage.setItem(key, String((idx + 1) % pool.length));
    } catch (e) { /* localStorage no disponible: usamos 0 */ }
    return pool[idx % pool.length];
  }

  function getSource() {
    try {
      var params = new URLSearchParams(window.location.search);
      return params.get("utm_source") || "seo-organico";
    } catch (e) { return "seo-organico"; }
  }

  function trackEvent(action, extra) {
    var payload = {
      event: "conversion",
      action: action,
      zona: ZONA,
      timestamp: new Date().toISOString(),
      page: window.location.pathname,
      source: getSource()
    };
    if (extra) { Object.keys(extra).forEach(function (k) { payload[k] = extra[k]; }); }
    // En producción: gtag('event', ...) / dataLayer.push(...) / API call tracking
    console.log("📊 [TRACKING]", payload);
    return payload;
  }

  // Registrar TODAS las llamadas (Click-to-Call) y CTAs marcados
  var trackables = document.querySelectorAll("[data-track]");
  trackables.forEach(function (el) {
    el.addEventListener("click", function () {
      var action = el.getAttribute("data-track");
      var href = el.getAttribute("href") || "";
      var isCall = href.indexOf("tel:") === 0;
      var extra = { type: isCall ? "click_to_call" : "cta_click" };
      if (isCall) {
        extra.phone = href.replace("tel:", "");
        // Simulamos el reparto interno de la llamada hacia una funeraria
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
    e.preventDefault(); // Evita la recarga de la página
    clearErrors();

    var lead = {
      tipoServicio: getVal("tipoServicio"),
      ubicacion: getVal("ubicacion"),
      sepultura: getRadio("sepultura"),
      nombre: getVal("nombre"),
      telefono: getVal("telefono"),
      rgpd: document.getElementById("rgpd").checked,
      meta: {
        capturadoEn: new Date().toISOString(),
        fuente: getSource(),
        zona: ZONA
      }
    };

    var errors = validate(lead);
    if (errors.length > 0) {
      errors.forEach(function (name) { markError(name); });
      focusFirstError(errors[0]);
      return;
    }

    // Asignar funeraria colaboradora al lead (reparto interno)
    lead.meta.partnerAsignado = asignarPartner(ZONA);

    trackEvent("lead_form_submit", {
      type: "form_lead",
      tipoServicio: lead.tipoServicio,
      sepultura: lead.sepultura,
      partner: lead.meta.partnerAsignado
    });

    console.log("✅ [LEAD CAPTURADO]", JSON.stringify(lead, null, 2));

    showSuccess(lead.nombre);

    // Ocultar campos tras el éxito
    Array.prototype.forEach.call(form.elements, function (el) {
      if (el.type !== "hidden") { el.style.display = "none"; }
    });
    var legal = form.querySelector(".lead-form__legal");
    if (legal) { legal.style.display = "none"; }
  });

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
      '<p>Una <strong>funeraria colaboradora de ' + escapeHtml(ZONA) + '</strong> revisará su ' +
      'solicitud y le contactará <strong>en pocos minutos</strong> por teléfono o WhatsApp para ' +
      'orientarle con calma, sin ningún compromiso.</p>' +
      '<p>Si prefiere atención inmediata, puede llamarnos ahora al ' +
      '<a href="tel:+34910000000">910 000 000</a>.</p>';
    successBox.hidden = false;
    successBox.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  // Limpiar errores al corregir
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
   NAVEGACIÓN MÓVIL (menú hamburguesa) — IIFE independiente
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
  // Cerrar al pulsar un enlace (mejor UX en móvil)
  menu.querySelectorAll("a").forEach(function (a) {
    a.addEventListener("click", function () {
      menu.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });
})();

/* =========================================================
   CHAT IA FLOTANTE
   Listo para conectar con Gemma (Google AI Studio).
   Mientras no haya API key, responde con una base local.
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

  /* ---------- CONFIGURACIÓN (rellenar cuando tengas la API) ---------- */
  var CHAT_CONFIG = {
    // ⚠ Pega aquí tu API key de Google AI Studio. Déjalo vacío para usar el modo local.
    // NOTA DE SEGURIDAD: exponer la key en el navegador es aceptable solo para
    // la capa gratuita. En producción, lo ideal es un pequeño proxy en tu backend.
    apiKey: "",
    // Modelo de Gemma en Google AI Studio (ajústalo al que uses, p.ej. gemma-3-27b-it)
    model: "gemma-3-27b-it",
    endpoint: "https://generativelanguage.googleapis.com/v1beta/models/",
    // Base de conocimiento (la rellenará la funeraria). Se envía como contexto.
    knowledgeBase: [
      "Servicios Funerarios 24h atiende Móstoles y el sur de Madrid las 24 horas.",
      "Ofrecemos incineración desde 1.500€, inhumación desde 2.900€ y traslados.",
      "Teléfono de contacto 24h: 910 000 000.",
      "Trabajamos con familias con y sin seguro de decesos, con opciones de financiación.",
      "Nos encargamos de todos los trámites: certificado, Registro Civil y licencias."
    ].join(" ")
  };

  /* ---------- Respuestas locales (fallback sin API) ---------- */
  var LOCAL_FAQ = [
    { k: ["precio","cuesta","cuánto","cuanto","tarifa","incinera","cremaci"],
      a: "Ofrecemos incineración desde 1.500€ e inhumación desde 2.900€, siempre con presupuesto cerrado y sin cargos ocultos. ¿Quiere que le preparemos uno sin compromiso? Puede llamarnos al 910 000 000." },
    { k: ["24","hora","noche","ahora","urg","fallec","muerto","murió","murio"],
      a: "Sí, atendemos las 24 horas, los 365 días del año. Si acaba de producirse un fallecimiento, lo mejor es llamarnos ahora mismo al 910 000 000 y le orientamos de inmediato." },
    { k: ["seguro","decesos","póliza","poliza"],
      a: "Trabajamos con y sin seguro de decesos. Si tiene póliza, la revisamos gratis; y recuerde que puede elegirnos aunque el seguro sea de otra compañía. ¿Le ayudo con algo más?" },
    { k: ["trámite","tramite","papeleo","registro","certificado","document"],
      a: "Nos encargamos de todos los trámites urgentes: certificado de defunción, inscripción en el Registro Civil y licencias. También le orientamos sobre pensiones y herencias." },
    { k: ["zona","mostoles","móstoles","alcorc","fuenlab","legan","getafe","arroyo","dónde","donde"],
      a: "Damos servicio en Móstoles, Alcorcón, Fuenlabrada, Leganés, Getafe, Arroyomolinos y todo el sur de Madrid. ¿En qué localidad se encuentra?" }
  ];

  function localAnswer(text) {
    var t = (text || "").toLowerCase();
    for (var i = 0; i < LOCAL_FAQ.length; i++) {
      for (var j = 0; j < LOCAL_FAQ[i].k.length; j++) {
        if (t.indexOf(LOCAL_FAQ[i].k[j]) !== -1) { return LOCAL_FAQ[i].a; }
      }
    }
    return "Gracias por su mensaje. Para darle la mejor atención, puede llamarnos al 910 000 000 (24 horas) y le ayudamos personalmente. ¿Desea que le llamemos nosotros?";
  }

  /* ---------- Integración con Gemma (Google AI Studio) ---------- */
  async function askGemma(userText) {
    if (!CHAT_CONFIG.apiKey) { return localAnswer(userText); }
    var url = CHAT_CONFIG.endpoint + CHAT_CONFIG.model + ":generateContent?key=" + CHAT_CONFIG.apiKey;
    var prompt =
      "Eres el asistente de una funeraria del sur de Madrid. Responde en español, " +
      "de forma breve, empática y respetuosa. Usa esta información:\n" +
      CHAT_CONFIG.knowledgeBase + "\n\nPregunta del usuario: " + userText;
    try {
      var res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ contents: [{ role: "user", parts: [{ text: prompt }] }] })
      });
      var data = await res.json();
      var out = data && data.candidates && data.candidates[0] &&
                data.candidates[0].content && data.candidates[0].content.parts[0].text;
      return out || localAnswer(userText);
    } catch (e) {
      console.warn("Chat: fallo API, usando respuesta local.", e);
      return localAnswer(userText);
    }
  }

  function addMsg(text, who) {
    var el = document.createElement("div");
    el.className = "chat-msg chat-msg--" + who;
    el.textContent = text;
    body.appendChild(el);
    body.scrollTop = body.scrollHeight;
    return el;
  }

  var greeted = false;
  function openPanel() {
    panel.classList.add("is-open");
    fab.setAttribute("aria-expanded", "true");
    if (!greeted) {
      addMsg("Hola, soy el asistente de Servicios Funerarios 24h. ¿En qué puedo ayudarle? Estamos disponibles las 24 horas.", "bot");
      greeted = true;
    }
    setTimeout(function () { input.focus(); }, 100);
  }
  function closePanel() {
    panel.classList.remove("is-open");
    fab.setAttribute("aria-expanded", "false");
  }

  fab.addEventListener("click", function () {
    panel.classList.contains("is-open") ? closePanel() : openPanel();
  });
  if (closeBtn) { closeBtn.addEventListener("click", closePanel); }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    var text = input.value.trim();
    if (!text) { return; }
    addMsg(text, "user");
    input.value = "";
    var thinking = addMsg("…", "bot");
    var reply = await askGemma(text);
    thinking.textContent = reply;
    body.scrollTop = body.scrollHeight;
  });
})();
