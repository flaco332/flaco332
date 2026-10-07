# Diseño y mantenimiento

La identidad combina una terminal con un panel de infraestructura: negro grafito,
acentos azul grisáceo, retículas discretas, líneas finas y tipografía de sistema.
La variante clara utiliza fondo marfil, texto azul oscuro y cian de mayor contraste.
El símbolo propio combina una F geométrica, un chevron y el cursor de una terminal.

El banner abre el perfil con el usuario y su foco profesional. `whoami` presenta
la idea de entender sistemas, seguir señales y asegurar caminos. Cuatro tarjetas
organizan el stack y tres tarjetas enlazadas muestran proyectos reales.
Los mapas radiales usan radios iguales: indican áreas de práctica e interés,
sin atribuir niveles, porcentajes ni años de experiencia. BJJ queda como un
detalle personal dentro del desplegable final.
Un banner de seis líneas de arte de bloques, proporcionado por el usuario,
aparece debajo de los mapas. Utiliza un fondo oscuro en ambos temas.
Cada carácter se dibuja con formas SVG, conservando los espacios y la alineación
sin depender de fuentes. El sombreado utiliza patrones locales de puntos.
La fuente `scripts/terminal-banner.html` conserva el HTML proporcionado: se
leen por separado el color y el fondo de cada carácter. Al generar el SVG,
sus colores se adaptan a gris, grafito y azul marino mediante `BANNER_COLORS`.

## Archivos

```text
README.md
.gitattributes
.gitignore
assets/
  banner-dark.svg
  banner-light.svg
  skills-banner.svg
  skills-banner-light.svg
  whoami.svg
  whoami-light.svg
  tech-stack-{security,cloud,code,systems}.svg
  tech-stack-{security,cloud,code,systems}-light.svg
  radar-skills.svg
  radar-skills-light.svg
  radar-langs.svg
  radar-langs-light.svg
  project-card-{packet-tracer-security,grep-c,onca}.svg
  project-card-{packet-tracer-security,grep-c,onca}-light.svg
  logo.svg
  logo-light.svg
docs/
  DESIGN.md
  PUBLISHING.md
  VALIDATION.md
  preview.html
scripts/
  build_assets.py
  preview.py
  validate.py
  terminal-banner.html
```

## Compatibilidad

Cada ilustración está en un `<picture>` con dos fuentes por tema y una imagen
de respaldo. Este patrón está documentado por
[GitHub](https://docs.github.com/es/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github).
Se usa `prefers-color-scheme`: la elección depende del esquema de color que
el navegador exponga para la página. Si no coincide ninguna fuente, aparece
la versión oscura, con su propio fondo y contraste.

El README no necesita CSS personalizado, JavaScript, fuentes remotas, animaciones
ni servicios de badges. Los SVG tienen `viewBox`, título y descripción; las
imágenes tienen texto alternativo. Las tarjetas se colocan en flujo normal:
caben en dos columnas cuando hay espacio y pasan a una en pantallas estrechas.
No se utiliza una tabla que obligue a conservar columnas. GitHub limita las
imágenes al ancho disponible; los bloques de código se pueden desplazar.

Los enlaces y las descripciones de proyectos también están en Markdown, y el
stack completo está en un desplegable YAML. Los datos personales se limitan
al usuario, al rol genérico y a los contactos expresamente autorizados.

## Fuentes de las tarjetas

Se leyeron los README de
[Packet Tracer Security](https://github.com/flaco332/packet-tracer-security),
[Grep-C](https://github.com/flaco332/grep-c) y
[ONCA](https://github.com/flaco332/Onca).
Grep-C se describe como Mini Grep en Python. Packet Tracer Security usa Scapy
y reglas Prolog; no se presenta como un IDS de producción ni como un modelo
entrenado de ML. ONCA se describe como una aplicación local con SQLite.

## Vista previa

Abre `preview.html` desde esta carpeta para comparar Auto, Dark y Light.
La vista previa es offline y utiliza únicamente los SVG del repositorio.
Su renderizador soporta el subconjunto de Markdown usado por este README;
no reproduce el servicio ni el sanitizador de GitHub. La comprobación final
del perfil real se realiza después de que publiques el repositorio.
