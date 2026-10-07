# Validación de la entrega local

## Archivos y contenido

- Los 26 SVG se parsearon como XML válido y tienen `viewBox`, título y descripción.
- Se comprobaron los 12 pares claro/oscuro usados por el README y sus dimensiones.
- Todos los assets referenciados existen; el respaldo de cada imagen es local.
- El HTML del README está balanceado y usa `picture`, `source`, `img`, `a`, `p`,
  `details`, `summary` y `code`. No contiene CSS ni JavaScript personalizado.
- Los enlaces de navegación coinciden con los títulos del documento.
- Los enlaces públicos coinciden con los destinos autorizados por el usuario.
- El stack contiene las tecnologías proporcionadas; los mapas no inventan niveles.
- BJJ está en un desplegable al final. No se incluyeron apellidos, ubicación,
  teléfono, institución académica ni otros datos identificables adicionales.

## Comprobación visual

La vista previa se renderizó en Chromium con 320, 375, 768 y 1000 px de ancho,
para los dos esquemas de color. Las ocho combinaciones cargaron las 12 imágenes,
eligieron los assets del tema correcto y no presentaron desbordamiento horizontal.
También se abrieron los desplegables para verificar que el código permaneciera
dentro de su contenedor. Se comprobaron los botones de cambio de tema.

Se revisaron capturas de escritorio y móvil y hojas con todos los SVG de ambos
temas. Se midieron los límites de cada texto SVG: ninguno se sale del lienzo.
Los colores de texto, texto secundario y acento tienen contraste de al menos
5.15:1 contra el fondo de los SVG, según el cálculo de luminancia relativa.

Esta comprobación utiliza un layout local basado en el comportamiento de GitHub.
No es una prueba de un perfil publicado ni una ejecución del sanitizador de GitHub.
El patrón de imágenes por tema está documentado por
[GitHub](https://docs.github.com/es/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github).

## Enlaces externos

| Destino | Resultado |
| --- | --- |
| GitHub / flaco332 | Usuario y URL confirmados en los metadatos de sus repositorios públicos. |
| Packet Tracer Security | Repositorio público confirmado; README leído. |
| Grep-C | Repositorio público confirmado; README leído. |
| ONCA | Repositorio público confirmado; README leído. |
| Portafolio | Repositorio público `carlos-portafolio` confirmado con GitHub Pages habilitado. El acceso HTTP a la página no pudo verificarse. |
| Telegram | URL revisada, pero el acceso HTTP no pudo verificarse. |
| Email | Sintaxis `mailto:` y dirección autorizada comprobadas; no se envió correo. |

La consulta web y la conexión HTTP del entorno no pudieron acceder al portafolio
ni a Telegram. No se clasificaron esos enlaces como rotos ni se confirmó que
funcionen. Comprueba esos dos destinos en tu navegador antes de publicar.

## Estado de publicación

Se crearon únicamente archivos locales. No se inicializó Git, no se creó un
repositorio remoto y no se ejecutó push. Las instrucciones para publicar están
en `PUBLISHING.md`.
