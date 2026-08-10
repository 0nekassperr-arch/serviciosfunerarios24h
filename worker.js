/**
 * Cloudflare Worker — Proxy seguro para el chat IA (Google AI Studio)
 * =========================================================================
 * Mantiene la API KEY en el servidor (NUNCA en el navegador).
 *
 * CÓMO ACTUALIZARLO:
 * 1. dash.cloudflare.com -> tu Worker -> Edit code.
 * 2. Borra todo y pega este archivo -> Deploy.
 * 3. Comprueba el secreto GEMINI_API_KEY (Settings -> Variables and Secrets).
 */

const MODEL = "gemma-4-31b-it";              // principal (14.400 RPD gratis)
const FALLBACK = "gemini-3.5-flash-lite";    // reserva (menos RPD)

const ALLOWED_ORIGINS = [
  "https://serviciosfunerarios24h.es",
  "https://www.serviciosfunerarios24h.es",
];

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const allow = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
    const cors = {
      "Access-Control-Allow-Origin": allow,
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };
    if (request.method === "OPTIONS") return new Response(null, { headers: cors });
    if (request.method !== "POST") return new Response("Method not allowed", { status: 405, headers: cors });

    let prompt = "";
    let model = MODEL;
    try {
      const b = await request.json();
      prompt = b.prompt || "";
      if (b.model) model = b.model;   // override opcional (pruebas)
    } catch (e) {}
    if (!prompt) return json({ text: "" }, cors);

    // Construye el cuerpo. useThinking=false intenta DESACTIVAR el razonamiento.
    function bodyFor(useNoThinking) {
      const gc = { temperature: 0.6, maxOutputTokens: 2048 };
      if (useNoThinking) gc.thinkingConfig = { thinkingBudget: 0 };
      return JSON.stringify({ contents: [{ role: "user", parts: [{ text: prompt }] }], generationConfig: gc });
    }
    async function raw(m, useNoThinking) {
      const url = `https://generativelanguage.googleapis.com/v1beta/models/${m}:generateContent?key=${env.GEMINI_API_KEY}`;
      return fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: bodyFor(useNoThinking) });
    }
    async function callModel(m) {
      let res = await raw(m, true);            // 1º: intenta sin "pensamiento"
      if (res.status === 400) res = await raw(m, false); // si no lo soporta, reintenta normal
      return res;
    }

    try {
      let res = await callModel(model);
      if (res.status === 404) res = await callModel(FALLBACK);
      const data = await res.json();
      if (data && data.error) return json({ text: "", error: data.error.message }, cors);
      const cand = (data.candidates && data.candidates[0]) || {};
      const parts = (cand.content && cand.content.parts) || [];
      // descarta las partes marcadas como "pensamiento"
      let text = parts.filter(p => !p.thought).map(p => p.text || "").join(" ").trim();
      if (!text) text = parts.map(p => p.text || "").join(" ").trim();
      return json({ text: extractFinal(text) }, cors);
    } catch (e) {
      return json({ text: "" }, cors);
    }
  },
};

/* Extrae solo el mensaje final: prioriza lo que va entre <R> y </R>. */
function extractFinal(t) {
  if (!t) return t;
  const all = t.match(/<R>([\s\S]*?)<\/R>/gi);
  if (all && all.length) {
    const inner = all[all.length - 1].replace(/<\/?R>/gi, "").trim();
    if (inner) return inner;
  }
  const open = t.toLowerCase().lastIndexOf("<r>");
  if (open > -1) {
    const after = t.slice(open + 3).replace(/<\/?R>/gi, "").trim();
    if (after) return after;
  }
  // Sin etiquetas: intenta recuperar el último "borrador/draft"
  const drafts = t.match(/(?:draft|borrador)\s*\d*\s*:?\*?\s*(.+)/gi);
  if (drafts && drafts.length) {
    const last = drafts[drafts.length - 1]
      .replace(/^[\s\S]*?(?:draft|borrador)\s*\d*\s*:?\*?\s*/i, "")
      .replace(/[*"]/g, "").trim();
    if (last) return last;
  }
  return t.trim();
}

function json(obj, cors) {
  return new Response(JSON.stringify(obj), { headers: { "Content-Type": "application/json", ...cors } });
}
