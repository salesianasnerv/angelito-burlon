# Web «Angelito Burlón y la estrella de Navidad»

Borrador de la web del proyecto de Adviento 2026 (Pastoral · Escuelas Salesianas María Auxiliadora · Nervión).
Es una web estática: un solo `index.html` con su estilo y su código dentro, más las carpetas de imágenes y PDF.
Vercel la publica tal cual, sin compilar nada.

## Qué hay

| Carpeta / archivo | Contenido |
|---|---|
| `index.html` | Toda la web (secciones: portada, corona de Adviento, cuento, vídeo, proyectos, juego, recursos y pie). |
| `img/escenas/` | Ilustraciones limpias del cuento (las mismas del vídeo), a 1600 y 800 px. |
| `img/libro/` | Las 16 dobles páginas del libro para el hojeador. |
| `img/personaje/` | El angelito recortado (fondo transparente) para el juego y la estela. |
| `img/logos/` | Logo del colegio (Nervión) en color y en blanco. |
| `pdf/` | Cuento en PDF: vista previa de pantalla y A4 para imprimir. |
| `video/angelito_burlon.*` | Vídeo final (720p), subtítulos .vtt y póster. Se rehace con `fuentes/video_web.sh`. |
| `video/escenas/` | Clips animados del vídeo (Flow), mudos y ligeros, que se ven en la portada y en el cuento. |
| `icons/`, `favicon.ico`, `img/og.jpg` | Iconos de la app, favicon e imagen para compartir por WhatsApp. |
| `manifest.webmanifest`, `sw.js` | Hacen que la web se pueda instalar como app (PWA). Sube `VERSION` en `sw.js` en cada cambio. |
| `fuentes/` | Script que genera todas las imágenes a partir de los originales y el logo original. |

## Cómo añadir lo que vaya estando listo

Al final de `index.html` hay un bloque `ENLACES`. Escribe la ruta o el enlace entre las comillas y la tarjeta
pasa sola de «En preparación» a «Disponible»:

```js
const ENLACES = {
  video: 'video/angelito_burlon.mp4',   // o un enlace de YouTube
  infantil: 'pdf/proyecto_infantil.pdf',
  primaria: 'pdf/proyecto_primaria_1-3.pdf',
  familias: 'pdf/proyecto_familias.pdf',
  cuentoImprimir: 'pdf/Angelito_Burlon_A4.pdf'
};
```

Los recursos de la sección «Más cosas del Angelito» se editan directamente en el HTML (buscar `listaRecursos`).

## Volver a generar las imágenes

Desde esta carpeta:
- `python3 fuentes/preparar_imagenes.py fuentes/logo_nervion.png` (escenas, libro, personaje, logos)
- `python3 fuentes/iconos_y_og.py` (favicon, iconos e imagen para compartir)
- `bash fuentes/clips_web.sh "…/Angelito burlón/Montaje/Video/Flow/renombrados"` (clips animados; necesita ffmpeg)
(necesita Python con Pillow y `poppler-utils`; lee las escenas y los PDF del proyecto).

## Notas

- La imagen para compartir apunta a `https://angelito-burlon.vercel.app`. Si Vercel le da otra dirección, cámbiala en las etiquetas `og:` de `index.html`.
- La web lleva `noindex` para que Google no la indexe mientras es borrador (quitar la etiqueta `robots` cuando se publique).
- El cuento es una adaptación libre de «Rastro de Dios», de Montserrat del Amo (Ediciones SM): antes de difundir la web
  fuera del colegio conviene confirmar el permiso de uso público.
