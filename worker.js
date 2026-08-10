/**
 * Cloudflare Worker — Proxy seguro para el chat IA (Gemma / Google AI Studio)
 * =========================================================================
 * Mantiene la API KEY en el servidor (NUNCA en el navegador).
 *
 * CÓMO DESPLEGARLO (gratis, ~5 min):
 * 1. Entra en https://dash.cloudflare.com  ->  Workers & Pages  ->  Create Worker.
 * 2. Pega este archivo completo y pulsa "Deploy".
 * 3. En el Worker -> Settings -> Variables -> "Add variable" (tipo Secret):
 *       Nombre:  GEMINI_API_KEY
 *       Valor:   (tu API key de Google AI Studio)
 *    Guarda y vuelve a desplegar.
 * 4. (Opcional) Ajusta ALLOWED_ORIGINS a tu dominio.
 * 5. Copia la URL del Worker (p.ej. https://chat-sf24.tuusuario.workers.dev)
 *    y ponla en /chat-config.json  ->  { "proxyUrl": "<esa URL>" }
 */

const MODEL = "gemma-4-31b-it"; // si no existe, cae a gemma-3-27b-it (ver más abajo)
const ALLOWED_ORIGINS = [
  "https://serviciosfunerarios24h.es",
  "https://www.serviciosfunerarios24h.es",
];

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const cors = {
      "Access-Control-Allow-Origin": ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0],
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };
    if (request.method === "OPTIONS") return new Response(null, { headers: cors });
    if (request.method !== "POST") return new Response("Method not allowed", { status: 405, headers: cors });

    let prompt = "";
    try { prompt = (await request.json()).prompt || ""; } catch (e) {}
    if (!prompt) return json({ text: "" }, cors);

    const body = JSON.stringify({
      contents: [{ role: "user", parts: [{ text: prompt }] }],
      generationConfig: { temperature: 0.6, maxOutputTokens: 400 },
    });

    async function call(model) {
      const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${env.GEMINI_API_KEY}`;
      return fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body });
    }

    try {
      let res = await call(MODEL);
      if (res.status === 404) res = await call("gemma-3-27b-it"); // fallback
      const data = await res.json();
      const text =
        data?.candidates?.[0]?.content?.parts?.[0]?.text ||
        (data?.error ? "" : "");
      return json({ text }, cors);
    } catch (e) {
      return json({ text: "" }, cors);
    }
  },
};

function json(obj, cors) {
  return new Response(JSON.stringify(obj), {
    headers: { "Content-Type": "application/json", ...cors },
  });
}
