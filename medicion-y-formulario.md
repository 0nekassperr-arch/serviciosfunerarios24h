# Medición de leads + Formulario de Google (guía)

## A. Cómo voy a montar la medición

### 1. GA4 (Google Analytics 4) — gratis
- Instalo el código de GA4 en las 53 páginas (desde el generador, con una variable `GA4_ID`).
- Configuro estos **eventos de conversión**:
  - `click_llamar` → cada vez que alguien pulsa un botón de teléfono (con datos: zona, página, origen).
  - `click_whatsapp` → clic en WhatsApp.
  - `generate_lead` → envío del formulario (con tipo de servicio y zona).
  - `cta_click` → clics en botones destacados.
- En GA4 los marco como **"Eventos clave/Conversiones"** para que veas cuántas llamadas y leads genera la web y **desde qué página/origen**.

> Nota: GA4 cuenta la **intención de llamada** (el clic). El **número real de quien llama y la duración** solo se consiguen con un número de call‑tracking (Twilio/CallRail), que montaremos más adelante con los primeros beneficios.

### 2. Banner de cookies (RGPD) — obligatorio antes de GA4
- Añado un banner simple: GA4 **solo se activa si el usuario acepta** (Consent Mode). Cumple RGPD/LSSI.

### 3. Formulario → Google Forms (oculto) — tu registro maestro
- El formulario de la web ya está preparado para enviar los datos **por detrás** a tu Google Form (el usuario no ve nada de Google).
- Las respuestas caen en una **Hoja de cálculo de Google** (tu registro maestro) + **aviso por email**.
- Flujo completo de un lead: el usuario envía → se valida → se manda oculto a tu Google Form (Hoja + email) → se dispara `generate_lead` en GA4 → se muestra el mensaje de éxito.

### Qué necesito de ti (2 datos)
1. **ID de GA4** (formato `G-XXXXXXXXXX`).
2. **Enlace prerrellenado** de tu Google Form (para sacar los IDs de cada campo).

---

## B. Qué formulario crear EXACTAMENTE (Google Forms)

1. Entra en **forms.google.com** → **Formulario en blanco**.
2. Título: **"Solicitudes web – serviciosfunerarios24h"**.
3. Añade **7 preguntas**, TODAS de tipo **"Respuesta corta"** y **NO obligatorias**:

   | # | Pregunta | Tipo |
   |---|----------|------|
   | 1 | Tipo de servicio | Respuesta corta |
   | 2 | Ubicación / Localidad | Respuesta corta |
   | 3 | ¿Dispone de nicho o sepultura? | Respuesta corta |
   | 4 | Nombre completo | Respuesta corta |
   | 5 | Teléfono | Respuesta corta |
   | 6 | Zona | Respuesta corta |
   | 7 | Origen (fuente) | Respuesta corta |

   ⚠️ **Importante:** que sean "Respuesta corta" y NO obligatorias. Si fueran "opción múltiple" u obligatorias con validación, Google rechazaría el envío automático.

4. **Conecta las respuestas a una Hoja de cálculo:** pestaña *Respuestas* → icono de Sheets → "Crear hoja de cálculo". (Ese será tu registro maestro.)
5. **Activa el aviso por email:** pestaña *Respuestas* → menú ⋮ → "Recibir notificaciones por correo de las respuestas nuevas".
6. **Saca los IDs (esto es lo que me pasas):** menú ⋮ (arriba a la derecha) → **"Obtener enlace prerrellenado"** → escribe "PRUEBA" en cada campo → **"Obtener enlace"** → **Copiar enlace** → pégamelo aquí.

Con ese enlace, yo relleno la configuración (URL de envío + los `entry.XXXX` de cada pregunta) y queda todo conectado.

---

## Resumen de lo que hago yo vs. lo que haces tú
- **Tú:** crear la propiedad GA4 (me pasas el `G-...`) y el Google Form (me pasas el enlace prerrellenado).
- **Yo:** instalar GA4 + banner de cookies + eventos de conversión, y conectar el formulario a tu Google Form. Todo desplegado.
