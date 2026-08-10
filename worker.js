/**
 * Cloudflare Worker — Proxy seguro para el chat IA (Gemma / Google AI Studio)
 * =========================================================================
 * Mantiene la API KEY en el servidor (NUNCA en el navegador).
 *
 * CÓMO ACTUALIZARLO:
 * 1. Abre tu Worker en dash.cloudflare.com -> Edit code.
 * 2. Borra todo y pega este archivo completo -> Deploy.
 * 3. Comprueba que el secreto GEMINI_API_KEY sigue configurado
 *    (Settings -> Variables and Secrets).
 */

// gemma-3-27b-it = modelo de instrucción, responde limpio y directo (recomendado).
// (gemma-4-31b-it devuelve su "razonamiento", no sirve para chat de cliente.)
const MODEL = "gemma-3-27b-it";
const FALLBACK = "gemma-3-12b-it";

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
      if (b.model) model = b.model;              // override opcional para pruebas
    } catch (e) {}
    if (!prompt) return json({ text: "" }, cors);

    const payload = JSON.stringify({
      contents: [{ role: "user", parts: [{ text: prompt }] }],
      generationConfig: { temperature: 0.6, maxOutputTokens: 400 },
    });

    async function call(m) {
      const url = `https://generativelanguage.googleapis.com/v1beta/models/${m}:generateContent?key=${env.GEMINI_API_KEY}`;
      return fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: payload });
    }

    try {
      let res = await call(model);
      if (res.status === 404) res = await call(FALLBACK);
      const data = await res.json();
      let text = data?.candidates?.[0]?.content?.parts?.[0]?.text || "";
      return json({ text: sanitize(text) }, cors);
    } catch (e) {
      return json({ text: "" }, cors);
    }
  },
};

/* Limpia posibles "razonamientos" de modelos verbosos y deja solo el mensaje final. */
function sanitize(t) {
  if (!t) return t;
  const drafts = t.match(/(?:draft|borrador)\s*\d*\s*:?\*?\s*(.+)/ig);
  if (drafts && drafts.length) {
    let last = drafts[drafts.length - 1]
      .replace(/^[\s\S]*?(?:draft|borrador)\s*\d*\s*:?\*?\s*/i, "")
      .replace(/[*"]/g, "").trim();
    if (last) return last;
  }
  if (/persona:|constraint:|\byes\.\b|^\s*\*/im.test(t)) {
    const lines = t.split(/\n/).map(s => s.replace(/[*]/g, "").trim()).filter(Boolean);
    for (let i = lines.length - 1; i >= 0; i--) {
      if (/^(hola|buenos|buenas|gracias|le invito|estamos|el (precio|coste|servicio)|si )/i.test(lines[i]) && lines[i].length > 15) {
        return lines[i].replace(/^["']|["']$/g, "").trim();
      }
    }
  }
  return t.trim();
}

function json(obj, cors) {
  return new Response(JSON.stringify(obj), {
    headers: { "Content-Type": "application/json", ...cors },
  });
}
