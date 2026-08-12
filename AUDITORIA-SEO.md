# Auditoría SEO + CRO y plan de negocio — serviciosfunerarios24h.es
*Fecha: agosto 2026 · Web recién lanzada y verificada en Search Console*

---

## 0. Resumen ejecutivo

La web parte de una **base técnica excelente** para un proyecto recién nacido: HTML semántico, SEO on‑page completo, schema, sitemap, dominio con HTTPS, chat con IA y estructura escalable por carpetas. La nota técnica de salida es alta.

**Pero el dinero en este nicho NO lo da (solo) la web: lo da el SEO LOCAL + la conversión de llamadas.** Las 3 palancas que más ingresos generarán, por orden:

1. **Google Business Profile (ficha de empresa)** → aparecer en el "mapa" (pack local) de Móstoles. Es lo #1 en funerarias.
2. **Conversión de urgencia** (llamada/WhatsApp) + medición de leads → saber qué genera dinero.
3. **Contenido local de alta intención** → captar búsquedas de gente que necesita el servicio ya.

| Área | Nota | Estado |
|---|---|---|
| SEO técnico | 9/10 | Muy bueno |
| SEO on‑page | 9/10 | Muy bueno |
| Rendimiento / Core Web Vitals | 7/10 | Mejorable (imágenes) |
| **SEO local (GBP, NAP, reseñas)** | **2/10** | **Crítico — sin explotar** |
| Conversión (CRO) + medición | 5/10 | A medias (falta analítica/GA4) |
| Contenido | 6/10 | Buena base, ampliable |
| Confianza / E‑E‑A‑T (nicho YMYL) | 4/10 | Faltan datos reales y prueba social |
| Legal / RGPD | 4/10 | Datos placeholder + falta banner cookies |

---

## 1. SEO técnico — lo que YA está bien ✅
- Títulos y meta descriptions únicos por página.
- Canonicals correctos, Open Graph + Twitter Cards.
- **Schema.org** completo (FuneralHome, Service, FAQPage, BlogPosting, BreadcrumbList, ContactPage, WebSite).
- **sitemap.xml** (17 URLs, sin legales) + **robots.txt** + **feed RSS**.
- `noindex` en páginas legales.
- 1 solo `<h1>` por página; todas las imágenes con `alt`.
- Enlazado interno correcto (38 enlaces en la home) y estructura por carpetas escalable.
- HTTPS + dominio propio verificado.

### Ajustes técnicos menores recomendados
- **Dimensiones (`width`/`height`) en imágenes de contenido** (media/prose) para evitar saltos de diseño (CLS). Hoy solo el logo las lleva.
- **Preload de la imagen del hero** (`hero-serenidad.jpg`) para mejorar el LCP en la home.

---

## 2. Rendimiento / Core Web Vitals — mejorable (7/10)
- Imágenes en JPEG de ~1408×768 y **80–300 KB**. La más pesada: `camino-sereno.jpg` (302 KB).
- **Acción de alto impacto:** convertir a **WebP/AVIF** (ahorro del 30–60% de peso) y servir a ~1200 px. Bajaría el tiempo de carga en móvil (recuerda: gran parte del tráfico llega desde el móvil en momentos de urgencia).
- `favicon-512.png` (104 KB) y `logo-*.png`: se pueden comprimir.
- CSS 32 KB y JS 28 KB: perfectos, sin dependencias externas.

> **Puedo optimizar todas las imágenes a WebP y añadir preload/dimensiones automáticamente en el generador.** Es una mejora rápida.

---

## 3. SEO LOCAL — CRÍTICO y donde está el dinero (2/10) 🔴
En funerarias, **la mayoría de conversiones vienen del pack local (mapa) y de búsquedas "funeraria + ciudad"**. Hoy no se está explotando nada de esto.

**Acciones (por orden de impacto):**
1. **Crear/optimizar Google Business Profile** (ficha de empresa). *Requisito: dirección física real y verificación por Google (postal/vídeo).* Sin ficha, no apareces en el mapa.
   - Categoría principal: *Funeraria*. Categorías secundarias: *Servicio de cremación*, *Tanatorio*.
   - Teléfono, horario 24 h, zona de servicio (Móstoles + municipios), fotos, enlace a la web.
2. **Reseñas**: pedir sistemáticamente reseñas a familias atendidas. Es el factor #1 de ranking local y de conversión.
3. **NAP consistente** (Nombre‑Dirección‑Teléfono idéntico en web, GBP y directorios). ⚠️ Hoy la web tiene **teléfono/dirección placeholder en las 20 páginas** → hay que poner los reales.
4. **Citations/directorios** locales (páginas amarillas, directorios funerarios, cámara de comercio, etc.) con el mismo NAP.
5. Añadir schema **LocalBusiness con `geo` (lat/long)** y `hasMap` cuando haya dirección real.

---

## 4. Conversión (CRO) y medición — a medias (5/10)
Tienes CTAs potentes (llamar 24 h, botón sticky, formulario, chat). Falta lo que convierte visitas en **dinero medible**:

1. **Analítica: instalar GA4** (y opcional Microsoft Clarity para mapas de calor). Sin medición, no sabes qué funciona.
2. **Marcar conversiones**: clic en "Llamar", clic en WhatsApp, envío de formulario → eventos en GA4. Ya hay `data-track` en el código listo para engancharlo.
3. **Call tracking real**: sustituir el `910 000 000` por un número de seguimiento propio para atribuir cada llamada a su origen (SEO, campaña, página).
4. **Conectar el formulario** a Google Forms/CRM (ya está preparado en el código; falta el enlace prerrellenado) + **aviso por email** de cada lead.
5. **WhatsApp Business** con respuesta rápida (muchas familias prefieren escribir).
6. Micro‑mejoras: mostrar el teléfono aún más arriba en móvil; añadir "prueba social" cerca de los CTAs (reseñas, años de experiencia, "X familias atendidas").

---

## 5. Contenido para generar negocio (6/10)
Tienes 5 artículos sólidos. Para captar tráfico de **alta intención** (el que llama), amplía con:

**Páginas de servicio/ciudad de alta conversión:**
- "Incineración en Móstoles precio", "Tanatorio Móstoles", "Funeraria económica Móstoles".
- Réplicas de páginas de ciudad para más municipios (Parla, Pinto, Humanes, Navalcarnero…). El generador ya lo permite en 1 minuto.

**Artículos informativos (captación + confianza):**
- "Ayudas del Ayuntamiento para gastos funerarios en Móstoles".
- "Cuánto tarda una incineración", "Qué es la tanatopraxia", "Cómo elegir funeraria".
- "Repatriación de fallecidos" (alto valor).

**Estrategia:** cada artículo/página enlaza al formulario y al teléfono, y enlaza internamente a servicios y a la ciudad correspondiente.

---

## 6. Confianza / E‑E‑A‑T (nicho YMYL) — importante (4/10)
Funerarias = tema sensible ("Your Money or Your Life"): Google exige **señales de confianza reales**.
- **Datos reales de empresa** visibles (razón social, dirección, teléfono) → hoy son placeholder.
- **Reseñas/testimonios** reales en la web.
- **Página "Quiénes somos"** con equipo/experiencia real, años, colaboraciones.
- Sellos: pertenencia a asociaciones del sector, licencias.

---

## 7. Legal / RGPD — a resolver (4/10) ⚠️
- **Aviso Legal y Privacidad con datos placeholder** (`[Razón social]`, `[NIF]`) → completar con datos reales (obligatorio en España).
- **Banner de cookies** (RGPD/LSSI): necesario **antes** de instalar GA4/analítica.
- Coherencia del posicionamiento: la web transmite "funeraria"; asegúrate de que el acuerdo con la funeraria colaboradora y las condiciones de servicio lo respaldan, y de que reclamos como **"Cremación por 1.500€"** son reales y sostenibles (o usar "desde").

---

## 8. Plan de acción priorizado

### 🔴 AHORA (semana 1) — máxima rentabilidad
1. **Crear Google Business Profile** (necesita dirección real) + primeras fotos.
2. **Poner NAP real** en toda la web (teléfono, WhatsApp, email, dirección) — *lo hago yo en cuanto me des los datos*.
3. **Completar datos legales** (razón social + NIF) — *lo hago yo*.
4. **Instalar GA4 + banner de cookies** y marcar conversiones (llamada, WhatsApp, formulario) — *lo hago yo*.
5. **Conectar el formulario** a Google Forms + email de aviso — *lo hago yo con tu enlace prerrellenado*.
6. **Enviar sitemap en Search Console** y "Solicitar indexación" de las páginas top — *lo haces tú en GSC*.

### 🟠 2–4 SEMANAS
7. **Optimizar imágenes a WebP** + preload del hero — *lo hago yo*.
8. **Pedir reseñas** a las primeras familias (plantilla + enlace directo a reseñar).
9. **Publicar 3–4 páginas nuevas** (incineración Móstoles precio, tanatorio Móstoles, +1 ciudad) — *lo hago yo*.
10. **Alta en 5–10 directorios** locales con NAP idéntico.

### 🟢 CONTINUO
11. 2–4 contenidos/mes de alta intención.
12. Revisar en GSC consultas e indexación (cuando haya datos) y optimizar.
13. Vigilar KPIs de negocio (abajo).

---

## 9. KPIs para ganar dinero (lo que hay que medir)
- **Llamadas** desde la web (nº y origen).
- **Leads de formulario/WhatsApp**.
- **Tasa de conversión** visita → lead.
- **Leads cualificados** y **servicios cerrados** por la funeraria colaboradora.
- **Ingreso por lead / por cierre** y **coste** (hosting ~0, tiempo).
- Posición media y clics en Search Console (cuando acumule datos).

> Con el modelo de comisión por lead/cierre, el objetivo del trimestre debería ser: **aparecer en el pack local de Móstoles + medir cada llamada + cerrar 2‑3 acuerdos con funerarias** para monetizar el volumen.

---

## 10. Qué puedo hacer YO ahora mismo (sin esperar datos)
- ✅ Optimizar imágenes a **WebP** + preload/dimensiones (rendimiento).
- ✅ Instalar **GA4** + **banner de cookies** + eventos de conversión.
- ✅ Poner **NAP real** y **datos legales** (cuando me los pases).
- ✅ Conectar **Google Forms** (con tu enlace prerrellenado) + email de aviso.
- ✅ Crear **nuevas páginas** de servicio/ciudad de alta intención.
- ✅ Añadir **testimonios/reseñas** y señales de confianza a la web.

**Lo que necesita tu cuenta/negocio:** crear el Google Business Profile, conseguir reseñas, y darme los datos reales (NAP, razón social/NIF) y el enlace del Google Form.
