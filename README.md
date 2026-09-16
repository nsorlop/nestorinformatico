# Néstor el Informático · web del servicio a domicilio

Web estática, bilingüe (castellano y valenciano), para el servicio informático a
domicilio en La Font de la Figuera. El nicho es el pueblo; a los de alrededor se
va avisando con antelación, y la web lo dice así.

No usa cookies, no lleva analítica, no carga nada de servidores ajenos y
funciona entera sin JavaScript. Eso no es un capricho: es lo que permite que la
política de cookies diga la verdad y que no haga falta banner de consentimiento.

---

## Cómo se edita

**No toques el HTML.** El HTML se genera. Todos los textos están en
`_contenido/*.json`, en castellano y valenciano a la vez.

1. Abre el JSON que toque y cambia el texto.
2. Ejecuta:

```bash
python build.py
```

3. Eso vuelve a escribir las catorce páginas (siete en castellano y siete en
   valenciano), más `sitemap.xml`, `robots.txt` y `favicon.svg`.

Así el castellano y el valenciano no se pueden quedar descuadrados: si cambias
uno y olvidas el otro, se ve al momento porque están en la misma línea del JSON.

| Fichero | Qué contiene |
|---|---|
| `_contenido/servicios.json` | Los tres bloques de servicios y «lo que no hago» |
| `_contenido/precios_zona.json` | Tarifas orientativas y pueblos donde vas |
| `_contenido/confianza.json` | Cómo funciona, compromisos, aviso de estafas y preguntas frecuentes |
| `_contenido/sobre_mi.json` | Tu biografía, credenciales y proyectos |
| `_contenido/marca.json` | Nombre, lema y todos los textos de botones y etiquetas |
| `_contenido/seo.json` | Títulos, descripciones y los datos estructurados de Google |
| `_contenido/legal_aviso.json` | Aviso legal |
| `_contenido/legal_privacidad.json` | Política de privacidad y protección de datos |
| `_contenido/legal_cookies.json` | Política de cookies |
| `_contenido/legal_condiciones.json` | Condiciones del servicio: desistimiento, presupuesto, garantía |

Los datos del negocio (teléfono, correo, población, URL) están arriba del todo
de `build.py`, en el diccionario `NEGOCIO`. Ahí se cambian una vez y salen en
todas las páginas.

---

## Versión de prueba: sin datos fiscales

De momento la web funciona como prueba. Por eso los textos legales identifican
al titular solo con el nombre completo, el pueblo, el teléfono y el correo. No
aparecen NIF, DNI, domicilio, epígrafe del IAE ni la condición de autónomo, y
no hay huecos pendientes de rellenar.

El aviso legal, las condiciones del servicio, la privacidad y las cookies siguen
completos.

Si un día la actividad pasa a ser real, la LSSI obliga a poner el NIF en el
aviso legal. El sitio es el apartado 1 de `_contenido/legal_aviso.json`, y las
fichas equivalentes de `legal_condiciones.json` y `legal_privacidad.json`.

---

## Cómo se publica

Ya tienes GitHub Pages funcionando en `nsorlop.github.io`, así que lo más
rápido es un repositorio nuevo:

```bash
cd C:/Users/nesto/web-informatica
git init
git add .
git commit -m "Web del servicio informatico a domicilio"
git branch -M main
git remote add origin https://github.com/nsorlop/nestorinformatico.git
git push -u origin main
```

Después, en GitHub: *Settings* → *Pages* → *Source: Deploy from a branch* →
`main` / `(root)`. En un minuto está en
`https://nsorlop.github.io/nestorinformatico/`.

Si más adelante compras un dominio propio (algo del estilo
`informaticanestor.es`, que se dice bien por teléfono), añade un fichero
`CNAME` con el dominio dentro y apunta el DNS a GitHub Pages. Y acuérdate de
cambiar `NEGOCIO['url']` en `build.py`, porque de ahí salen el `canonical`, el
`sitemap.xml` y los datos estructurados.

---

## Para verla en local

```bash
python -m http.server 8787
```

Y abre `http://localhost:8787`. Ábrela con `http://`, no con doble clic en el
fichero: con `file://` el navegador bloquea las fuentes y se ve sin estilos.

---

## Estructura

```
index.html          portada, corta y directa
servicios.html      el catálogo completo, en tres bloques
precios.html        tarifas, cómo funciona y compromisos
sobre-mi.html       quién eres, formación y proyectos
preguntas.html      preguntas frecuentes y aviso de estafas
contacto.html       teléfono, formulario, horario y zona
legal.html          aviso legal, condiciones, privacidad y cookies
va/                 las mismas siete en valenciano

css/estilos.css     el diseño entero
css/fuentes.css     declaración de las fuentes locales
fonts/              Atkinson Hyperlegible y Bitter (licencia SIL OFL 1.1)
js/app.js           aviso de idioma y el formulario
img/portada.png     la imagen que sale al compartir el enlace por WhatsApp
_contenido/*.json   todos los textos
build.py            el generador
```

---

## Decisiones de diseño que conviene no deshacer

- **La portada es corta a propósito.** Su único trabajo es que alguien llame y
  que se entienda de un vistazo qué haces. Todo lo que no sirva para eso va a
  una página interior.
- **La lista de "¿Te suena alguno de estos?"** sale sola de los ejemplos de
  `servicios.json`. Son las averías dichas con las palabras de la gente, que es
  lo que hace que alguien se reconozca y descuelgue el teléfono. Si añades un
  servicio nuevo con buenos ejemplos, aparece ahí solo.
- **La letra base es de 18 px** y todo está en rem, así que el zoom del
  navegador agranda la página entera sin romper nada.
- **La tipografía del texto es Atkinson Hyperlegible**, diseñada por el Braille
  Institute para gente con poca visión: distingue la I de la l y el 0 de la O.
- **El botón de llamar está siempre a la vista** en el móvil, fijo abajo. La
  barra de arriba no se queda pegada en el móvil para no comerse la pantalla.
- **No hay menú desplegable.** El menú está siempre visible y se parte en dos
  filas si hace falta. Una hamburguesa es justo lo que no encuentra la gente mayor.
- **Un solo color manda.** El verde de persiana es el color de la marca y el del
  botón de llamar. El ocre sólo aparece en detalles y el rojo está reservado al
  aviso de estafas. Si metes un cuarto color, el botón de llamar deja de destacar.
- **En la portada sólo hay un botón relleno**, el de llamar. WhatsApp va
  contorneado. Es lo que hace que la vista vaya al teléfono.
- **Los idiomas son dos páginas distintas**, no un botón que cambia el texto con
  JavaScript. Así Google indexa las dos y funciona aunque el JavaScript falle.
- **El formulario no envía nada a ningún servidor.** Prepara el mensaje y abre
  el WhatsApp o el correo del visitante. Por eso no hace falta ni servidor ni
  consentimiento de tratamiento en el propio formulario.

---

## Qué falta por hacer tú

Está detallado en `LANZAMIENTO.md`. Ese fichero y los informes de `_revision/`
no se suben al repositorio, que es público: se quedan solo en tu ordenador.
