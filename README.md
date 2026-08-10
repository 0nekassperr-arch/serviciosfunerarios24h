# serviciosfunerarios24h.es

Web de captación / orientación funeraria por **SEO local** en el sur de Madrid (empezando por **Móstoles**). Servicio independiente que pone en contacto a las familias con funerarias colaboradoras de la zona.

> ⚠️ **Aviso:** No somos una funeraria. Somos un servicio independiente de orientación funeraria.

## 🧱 Tecnología

- HTML5 semántico
- CSS3 moderno con variables (Mobile-First, responsive, sin desbordamiento lateral)
- JavaScript vanilla (sin dependencias)

## 📁 Estructura

```
.
├── index.html            # Home (marca genérica + zona sur de Madrid)
├── mostoles/
│   └── index.html        # Página de ciudad (SEO local: Móstoles)
├── style.css             # Estilos compartidos (paleta blanco roto + beige + dorado champagne)
├── script.js             # Captura de leads + simulación de call tracking y reparto
└── assets/               # Imágenes (serenas, luz natural)
    ├── hero-serenidad.jpg
    ├── apoyo-familiar.jpg
    └── camino-sereno.jpg
```

## 🎨 Identidad

- **Paleta:** blanco roto, beige cálido, dorado champagne mate, textos gris/marrón suave.
- **Tono:** empático, sereno, transparente y local.
- **Estructura de URLs:** carpetas por localidad (`/mostoles/`, `/alcorcon/`, …), sin subdominios.

## 🚀 Uso en local

Cualquier servidor estático sirve. Por ejemplo:

```bash
python3 -m http.server 8000
# abrir http://localhost:8000
```

## 📌 Pendiente para producción

- Sustituir el número de teléfono `+34910000000` por el número real de **call tracking** propio.
- Conectar el envío del formulario a un CRM/endpoint real (actualmente simulado en consola).
- Implementar el reparto real de llamadas/leads (el JS solo lo simula).
- Añadir banner de cookies (RGPD) y redactar los textos legales (Aviso Legal, Privacidad, Cookies).
- Verificar que la oferta "Cremación por 1.500€" es sostenible por alguna funeraria colaboradora.

---

© serviciosfunerarios24h.es
