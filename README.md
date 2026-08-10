# serviciosfunerarios24h.es

Web de captación de servicios funerarios por **SEO local** en el sur de Madrid (Móstoles, Alcorcón, Fuenlabrada, Leganés, Getafe, Arroyomolinos).

- **Web en vivo:** https://serviciosfunerarios24h.es
- **Repositorio:** GitHub (rama `main`) → despliegue automático con **GitHub Pages**.
- **Tecnología:** HTML5 + CSS3 (mobile-first) + JavaScript vanilla. Sitio **estático** generado con Python.

---

## 🚀 Cómo se publica

Cada `git push` a `main` publica automáticamente en GitHub Pages (dominio propio vía `CNAME`).

```bash
python3 build.py      # regenera todo el HTML + sitemap.xml + robots.txt + CNAME
git add -A && git commit -m "..." && git push
```

---

## 🗂️ Estructura

```
build.py            # Motor: componentes (cabecera, footer, SEO, chat) + Home
build_pages.py      # Genera servicios, zonas, ayuda, blog, contacto, legales, sitemap
content_blog.py     # Contenido de los 5 artículos del blog
style.css           # Estilos (variables CSS, mobile-first)
script.js           # Formulario + call tracking + menú + chat IA
chat-kb.txt         # Base de conocimiento del chat (EDITABLE)
chat-config.json    # { proxyUrl } del chat (URL del Cloudflare Worker)
worker.js           # Código del Cloudflare Worker (proxy seguro de la IA)
assets/             # Imágenes, logo y favicons
index.html, mostoles/, servicios/, zonas/, <ciudades>/, blog/, ...  ← generados
```

> ⚠️ Los `.html` son **generados**: no los edites a mano; cambia `build.py` / `build_pages.py` / `content_blog.py` y ejecuta `python3 build.py`.

---

## ✏️ Tareas frecuentes

### Añadir una ciudad/zona
En `build.py`, añade un dict a la lista `ZONES` (con `slug`, `name`, `hero_sub`, `landmarks`, `intro`, `extra`). Ejecuta `python3 build.py`. Se crea la landing, se enlaza en menú/footer/zonas y entra en el sitemap.

### Añadir un artículo de blog
En `content_blog.py`, añade un dict a `BLOG_POSTS` (con `slug`, `title`, `description`, `category`, `date`, `image`, `body` en HTML). Ejecuta `python3 build.py`.

### Cambiar textos/NAP/precios
- NAP y datos de negocio: variables al inicio de `build.py` (`PHONE_DISP`, `EMAIL`, `ADDR_*`, `LEGAL_NAME`, `LEGAL_NIF`).
- Contenido de servicios/legales: funciones en `build_pages.py`.

---

## 🤖 Chat IA (Gemma 4 31B vía Google AI Studio)

- **Modelo:** `gemma-4-31b-it` (14.400 RPD) con `gemini-3.5-flash-lite` de reserva. Config en `worker.js`.
- **Proxy seguro:** la API key vive en el **Cloudflare Worker** (`chat-sf24`), nunca en el navegador. El front-end llama al Worker (`chat-config.json` → `proxyUrl`).
- **Base de conocimiento:** edita **`chat-kb.txt`** (el chat responde SOLO con esa info y solo sobre la funeraria).
- **Personas por horario** (en `script.js` → `CHAT_CONFIG.agents`): Paula (6–14 h), Carlos (14–22 h), Susana (22–6 h).
- **Tiempos:** primer mensaje → "escribiendo" a 15 s y respuesta a 20 s; después 20–30 s, máx. 3/min (`CHAT_CONFIG.minDelayMs/maxDelayMs/maxPerMinute`).
- **Anti-razonamiento:** `thinkingBudget:0` + tokens ampliados + extracción de la respuesta entre etiquetas `<R>…</R>` (en `worker.js` y `script.js`).

### Actualizar el Worker
Editar `worker.js` y volver a desplegar (panel de Cloudflare → Edit code → Deploy, o vía API de Cloudflare). El secreto `GEMINI_API_KEY` se conserva.

---

## 📨 Formulario → Google Forms (PENDIENTE de conectar)

El envío del formulario está preparado para ir, de forma **oculta**, a un Google Form (`GFORM_CONFIG` en `script.js`). Falta pegar la URL `formResponse` y los IDs `entry.XXXX` (se obtienen del "enlace prerrellenado" del formulario).

---

## ✅ SEO incluido

Títulos y meta descriptions únicos, canonical, Open Graph + Twitter Cards, Schema.org (FuneralHome, Service, BreadcrumbList, FAQPage, BlogPosting, ContactPage, WebSite), `sitemap.xml`, `robots.txt`, NAP consistente, favicons y logo, imágenes con `alt`, mobile-first sin desbordamiento.

---

## 🔒 Pendientes / recordatorios

- [ ] **Google Forms:** pegar enlace prerrellenado para volcar los leads.
- [ ] **NAP real:** sustituir teléfono, WhatsApp, email y dirección (placeholder) en `build.py`.
- [ ] **Datos legales:** `LEGAL_NAME` y `LEGAL_NIF` en `build.py`.
- [ ] **HTTPS:** activar "Enforce HTTPS" en GitHub → Settings → Pages.
- [ ] **Seguridad:** regenerar la API key de Google y rotar tokens/credenciales usados durante el desarrollo.
- [ ] Confirmar que el reclamo "Cremación por 1.500€" es sostenible (o cambiar a "desde").

---

© serviciosfunerarios24h.es
