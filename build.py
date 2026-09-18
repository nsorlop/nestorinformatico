#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de la web de Néstor Soriano · Informática a domicilio.

Cómo funciona
-------------
Todo el texto de la web vive en los ficheros JSON de _contenido/, en castellano
y en valenciano a la vez. Este script los lee y escribe las páginas:

    index.html      servicios.html   precios.html
    sobre-mi.html   preguntas.html   contacto.html   legal.html

y las mismas en valenciano dentro de va/.

Para cambiar un texto NO toques el HTML: toca el JSON y vuelve a ejecutar

    python build.py

Así el castellano y el valenciano nunca se quedan descuadrados.
"""

import html
import json
import os
import re
from datetime import date
from urllib.parse import quote

RAIZ = os.path.dirname(os.path.abspath(__file__))
CONT = os.path.join(RAIZ, '_contenido')

# ---------------------------------------------------------------------------
# DATOS DEL NEGOCIO. Esto es lo único que tendrás que tocar tú.
# ---------------------------------------------------------------------------
NEGOCIO = {
    'marca':        'Néstor el Informático',
    'marca_va':     "Néstor l'Informàtic",
    'titular':      'Néstor Soriano López',
    'tel_humano':   '644 21 91 18',
    'tel_link':     '+34644219118',
    'tel_wa':       '34644219118',
    'correo':       'nestorlafont@gmail.com',
    'poblacion':    'La Font de la Figuera',
    'poblacion_va': 'la Font de la Figuera',
    'provincia':    'València',
    'cp':           '46630',
    'github':       'https://github.com/nsorlop',
    'portfolio':    'https://nsorlop.github.io',
    # Cambia esta URL por la definitiva cuando publiques la web.
    'url':          'https://nestorinformatico.es/',
}

HERO = {
    'h1':   {'es': 'Voy yo a tu casa',
             'va': 'Vaig jo a casa teua'},
    'lead': {'es': 'Informática a domicilio en La Font de la Figuera. Hago de todo: desde '
                   'mirarte el ordenador en tu casa hasta hacerte una aplicación propia o '
                   'tu propia inteligencia artificial para el negocio.',
             'va': "Informàtica a domicili a la Font de la Figuera. Faig de tot: des de "
                   "mirar-te l'ordinador a ta casa fins a fer-te una aplicació pròpia o la "
                   "teua pròpia intel·ligència artificial per al negoci."},
}

HORARIO = {
    'es': ['Lunes a viernes, de 9:00 a 14:00 y de 16:00 a 20:00.',
           'Sábados por la mañana, de 10:00 a 13:00.',
           'Fuera de ese horario, llama igual y lo miramos.'],
    'va': ['De dilluns a divendres, de 9:00 a 14:00 i de 16:00 a 20:00.',
           'Dissabtes de matí, de 10:00 a 13:00.',
           "Fora d'eixe horari, crida'm igual i ho mirem."],
}

CAPA1_ES = {'c_tit': 'Información básica sobre protección de datos', 'c1': 'Responsable', 'v1': 'Néstor Soriano López.', 'c2': 'Finalidad', 'v2': 'Contestarte y, si quieres, prestarte el servicio que me pidas.', 'c3': 'Legitimación', 'v3': 'Tu petición, que es una medida previa al contrato (artículo 6.1.b del RGPD).', 'c4': 'Destinatarios', 'v4': 'Nadie, salvo obligación legal. Si me escribes por WhatsApp o por correo, el mensaje pasa por Meta o por Google.', 'c5': 'Derechos', 'v5': 'Acceder, rectificar, suprimir, oponerte, limitar y portar tus datos, y reclamar ante la Agencia Española de Protección de Datos.', 'ver_priv': 'Leer la política de privacidad completa'}

CAPA1_VA = {'c_tit': 'Informació bàsica sobre protecció de dades', 'c1': 'Responsable', 'v1': 'Néstor Soriano López.', 'c2': 'Finalitat', 'v2': 'Contestar-te i, si vols, prestar-te el servici que em demanes.', 'c3': 'Legitimació', 'v3': 'La teua petició, que és una mesura prèvia al contracte (article 6.1.b del RGPD).', 'c4': 'Destinataris', 'v4': "Ningú, menys quan ho mana la llei. Si m'escrius per WhatsApp o per correu, el missatge passa per Meta o per Google.", 'c5': 'Drets', 'v5': "Accedir, rectificar, suprimir, oposar-te, limitar i portar les teues dades, i reclamar davant de l'Agència Espanyola de Protecció de Dades.", 'ver_priv': 'Llegir la política de privacitat completa'}

IDIOMAS = {
    'es': {'lang': 'es-ES', 'otro': 'va', 'raiz': ''},
    'va': {'lang': 'ca-ES-valencia', 'otro': 'es', 'raiz': '../'},
}

# Páginas del sitio y su nombre en el menú
PAGINAS = [
    ('index.html',     {'es': 'Inicio',     'va': 'Inici'}),
    ('servicios.html', {'es': 'Qué hago',   'va': 'Què faig'}),
    ('precios.html',   {'es': 'Precios',    'va': 'Preus'}),
    ('sobre-mi.html',  {'es': 'Quién soy',  'va': 'Qui soc'}),
    ('preguntas.html', {'es': 'Preguntas',  'va': 'Preguntes'}),
    ('contacto.html',  {'es': 'Contacto',   'va': 'Contacte'}),
]

HOY = date.today()
MESES_ES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
            'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
MESES_VA = ['gener', 'febrer', 'març', 'abril', 'maig', 'juny', 'juliol',
            'agost', 'setembre', 'octubre', 'novembre', 'desembre']


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def cargar(nombre, obligatorio=True):
    ruta = os.path.join(CONT, nombre + '.json')
    if not os.path.exists(ruta):
        if obligatorio:
            raise SystemExit('Falta el fichero de contenido %s' % ruta)
        return None
    with open(ruta, encoding='utf-8') as fh:
        return json.load(fh)


def t(obj, lang, defecto=''):
    """Saca el texto del idioma pedido de un {"es": ..., "va": ...}."""
    if obj is None:
        return defecto
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        return obj.get(lang, obj.get('es', defecto))
    return defecto


def e(texto):
    return html.escape(str(texto), quote=True)


def parrafos(obj, lang, clase=''):
    # Acepta un {"es": ..., "va": ...} o directamente una lista ya elegida por idioma
    lista = obj if isinstance(obj, list) else t(obj, lang, [])
    if isinstance(lista, str):
        lista = [lista]
    c = ' class="%s"' % clase if clase else ''
    return '\n'.join('<p%s>%s</p>' % (c, e(p)) for p in lista if p)


def lista_ul(obj, lang, clase=''):
    items = t(obj, lang, [])
    if not items:
        return ''
    c = ' class="%s"' % clase if clase else ''
    return '<ul%s>\n%s\n</ul>' % (c, '\n'.join('  <li>%s</li>' % e(i) for i in items))


def fecha_larga(lang):
    meses = MESES_VA if lang == 'va' else MESES_ES
    return '%d de %s de %d' % (HOY.day, meses[HOY.month - 1], HOY.year)


def marcar_huecos(texto):
    """Resalta los [DATOS PENDIENTES] para que canten a la vista."""
    return re.sub(r'\[([^\]]*PENDIENTE[^\]]*)\]',
                  lambda m: '<mark class="hueco">[%s]</mark>' % e(m.group(1)),
                  e(texto))


def wa_url(lang):
    return 'https://wa.me/%s?text=%s' % (
        NEGOCIO['tel_wa'], quote(t(MARCA['mensaje_whatsapp_prellenado'], lang)))


# ---------------------------------------------------------------------------
# Iconos (SVG en línea: ni una petición a servidores de fuera)
# ---------------------------------------------------------------------------
def icono(nombre, tam=24):
    base = ('<svg viewBox="0 0 24 24" width="%d" height="%d" aria-hidden="true" '
            'focusable="false" fill="none" stroke="currentColor" stroke-width="2.2" '
            'stroke-linecap="round" stroke-linejoin="round">%%s</svg>') % (tam, tam)
    formas = {
        'tel': '<path d="M6.5 3h3l1.5 4.5-2 1.4a13 13 0 0 0 6.1 6.1l1.4-2L21 14.5v3a2.5 2.5 0 0 1-2.7 2.5A16.8 16.8 0 0 1 4 5.7 2.5 2.5 0 0 1 6.5 3Z"/>',
        'mail': '<rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="m3 7 9 6 9-6"/>',
        'check': '<path d="M4 12.5 9.5 18 20 6.5"/>',
        'lugar': '<path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/>',
        'reloj': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.2 2"/>',
        'aviso': '<path d="M12 3.5 22 20H2L12 3.5Z"/><path d="M12 9.5v4.2"/><circle cx="12" cy="17" r="1" fill="currentColor" stroke="none"/>',
        'escudo': '<path d="M12 2.8 20 6v5.5c0 4.7-3.3 8.3-8 9.7-4.7-1.4-8-5-8-9.7V6l8-3.2Z"/><path d="m8.6 12 2.4 2.4 4.4-4.6"/>',
        'casa': '<path d="M3.5 10.5 12 3.5l8.5 7"/><path d="M5.5 12v8.5h13V12"/><path d="M10 20.5v-5h4v5"/>',
        'tienda': '<path d="M4 9.5h16V20H4z"/><path d="M3 9.5 5 4h14l2 5.5"/><path d="M9.5 20v-5h5v5"/>',
        'chip': '<rect x="7" y="7" width="10" height="10" rx="2"/><path d="M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4"/>',
        'euro': '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.6a4.4 4.4 0 0 0-6.4 1.3 5.5 5.5 0 0 0 0 4.2 4.4 4.4 0 0 0 6.4 1.3"/><path d="M7.4 11h5.2M7.4 13.4h5.2"/>',
        'persona': '<circle cx="12" cy="8" r="3.6"/><path d="M4.8 20.2a7.4 7.4 0 0 1 14.4 0"/>',
        'chat': '<path d="M20.5 12.3c0 4-3.8 7.2-8.5 7.2a9.9 9.9 0 0 1-2.9-.4L4 20.8l1.4-3.6a6.9 6.9 0 0 1-1.9-4.7c0-4 3.8-7.3 8.5-7.3s8.5 3.2 8.5 7.1Z"/>',
        'flecha': '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
        'cerrar': '<path d="M6 6l12 12M18 6 6 18"/>',
    }
    if nombre == 'wa':
        return ('<svg viewBox="0 0 24 24" width="%d" height="%d" aria-hidden="true" '
                'focusable="false" fill="currentColor"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.26-.47-2.39-1.48-.89-.79-1.48-1.76-1.66-2.06-.17-.3-.02-.46.13-.6.14-.14.3-.35.45-.52.15-.18.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.91-2.21-.25-.58-.49-.5-.67-.51h-.57c-.2 0-.52.08-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.87 1.22 3.07c.15.2 2.1 3.2 5.08 4.49.7.3 1.26.49 1.69.62.71.23 1.36.2 1.87.12.57-.08 1.76-.72 2-1.41.25-.7.25-1.29.18-1.42-.08-.12-.28-.2-.57-.34M12.05 21.8a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26C2.17 6.45 6.6 2.02 12.05 2.02c2.64 0 5.12 1.03 6.99 2.9a9.83 9.83 0 0 1 2.89 6.99c0 5.45-4.43 9.89-9.88 9.89m8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.69 1.45c6.55 0 11.89-5.34 11.89-11.9 0-3.17-1.24-6.16-3.48-8.4Z"/></svg>') % (tam, tam)
    return base % formas.get(nombre, '')


LOGO_SVG = '''<svg class="marca__icono" viewBox="0 0 64 64" role="img" aria-label="%s">
  <rect width="64" height="64" rx="13" fill="#16483a"/>
  <path d="M11 30 32 13l21 17" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="19.5" y="32" width="25" height="17" rx="2.5" fill="none" stroke="#fff" stroke-width="4"/>
  <path d="M32 49v4M27 54h10" stroke="#fff" stroke-width="4" stroke-linecap="round"/>
</svg>'''


# ---------------------------------------------------------------------------
# Cabecera, menú y pie
# ---------------------------------------------------------------------------
def menu(lang, pagina_actual):
    enlaces = []
    for archivo, nombres in PAGINAS:
        actual = ' aria-current="page"' if archivo == pagina_actual else ''
        enlaces.append('      <li><a href="%s"%s>%s</a></li>'
                       % (archivo, actual, e(t(nombres, lang))))
    etiqueta = 'Menú principal' if lang == 'es' else 'Menú principal'
    return '<nav class="nav" aria-label="%s">\n  <div class="env">\n    <ul>\n%s\n    </ul>\n  </div>\n</nav>' % (
        e(etiqueta), '\n'.join(enlaces))


def cabecera_html(lang, mc, pagina):
    raiz = IDIOMAS[lang]['raiz']
    marca = NEGOCIO['marca_va'] if lang == 'va' else NEGOCIO['marca']
    destino_otro = ('va/' + pagina) if lang == 'es' else ('../' + pagina)

    return '''<a class="saltar" href="#contenido">%(saltar)s</a>

<header class="barra">
  <div class="env barra__int">
    <a class="marca" href="index.html">
      %(logo)s
      <span class="marca__txt">
        <span class="marca__nom">%(marca)s</span>
        <span class="marca__sub">%(claim)s</span>
      </span>
    </a>

    <div class="controles">
      <div class="grupo idioma">
        <span class="grupo__et">Idioma</span>
        <a href="%(es_href)s" hreflang="es" lang="es"%(es_actual)s>Castellano</a>
        <a href="%(va_href)s" hreflang="ca-ES-valencia" lang="ca-ES-valencia"%(va_actual)s>Valencià</a>
      </div>
      <a class="barra__tel" href="tel:%(tel_link)s">%(ic_tel)s %(tel)s</a>
    </div>
  </div>
  %(menu)s
</header>

<div class="aviso-idioma" id="aviso-idioma" hidden>
  <div class="env aviso-idioma__int">
    <p>%(aviso_idioma)s</p>
    <a class="btn btn--linea" href="%(destino_otro)s" hreflang="%(otro_lang)s">%(ir_otro)s</a>
    <button type="button" data-cerrar-aviso aria-label="%(cerrar)s">%(ic_cerrar)s</button>
  </div>
</div>
''' % {
        'saltar': e(mc['saltar_al_contenido']),
        'raiz': raiz,
        'logo': LOGO_SVG % e(marca),
        'marca': e(marca),
        'claim': e(t(MARCA['claim'], lang)),
        'es_href': (raiz + pagina) if lang == 'va' else '#',
        'va_href': ('va/' + pagina) if lang == 'es' else '#',
        'es_actual': ' aria-current="true"' if lang == 'es' else '',
        'va_actual': ' aria-current="true"' if lang == 'va' else '',
        'tel_link': NEGOCIO['tel_link'],
        'tel': NEGOCIO['tel_humano'],
        'ic_tel': icono('tel', 19),
        'menu': menu(lang, pagina),
        'aviso_idioma': e(mc['aviso_idioma']),
        'destino_otro': destino_otro,
        'otro_lang': IDIOMAS[IDIOMAS[lang]['otro']]['lang'],
        'ir_otro': e(mc['boton_idioma_va'] if lang == 'es' else mc['boton_idioma_es']),
        'cerrar': 'Cerrar' if lang == 'es' else 'Tancar',
        'ic_cerrar': icono('cerrar', 20),
    }


def franja_movil(lang):
    llamar = 'Llamar' if lang == 'es' else 'Cridar'
    return '''<div class="franja">
  <a class="f-tel" href="tel:%s">%s <span>%s<br><strong>%s</strong></span></a>
  <a class="f-wa" href="%s" target="_blank" rel="noopener">%s <span>WhatsApp</span></a>
</div>''' % (NEGOCIO['tel_link'], icono('tel', 24), e(llamar), e(NEGOCIO['tel_humano']),
             wa_url(lang), icono('wa', 24))


def pie_html(lang, mc):
    raiz = IDIOMAS[lang]['raiz']
    marca = NEGOCIO['marca_va'] if lang == 'va' else NEGOCIO['marca']
    sin_cookies = ('Esta web no usa cookies, no lleva publicidad y no te sigue el rastro.'
                   if lang == 'es' else
                   'Esta web no usa cookies, no porta publicitat i no et seguix el rastre.')
    paginas = '\n'.join('          <li><a href="%s">%s</a></li>' % (a, e(t(n, lang)))
                        for a, n in PAGINAS)
    return '''<footer class="pie">
  <div class="env">
    <div class="pie__grid">
      <div>
        <p class="pie__marca">%(marca)s</p>
        <p>%(claim)s</p>
        <p class="pie__tel"><a href="tel:%(tel_link)s">%(tel)s</a></p>
        <p><a href="mailto:%(correo)s">%(correo)s</a></p>
      </div>
      <div>
        <h3>%(t_paginas)s</h3>
        <ul>
%(paginas)s
        </ul>
      </div>
      <div>
        <h3>%(t_legal)s</h3>
        <ul>
          <li><a href="legal.html#aviso-legal">%(l_aviso)s</a></li>
%(li_cond)s          <li><a href="legal.html#privacidad">%(l_priv)s</a></li>
          <li><a href="legal.html#cookies">%(l_cook)s</a></li>
        </ul>
      </div>
    </div>
    <div class="pie__legal">
      <p>&copy; <span id="anyo">%(anyo)d</span> %(derechos)s</p>
      <p>%(sin_cookies)s %(hecha)s</p>
    </div>
  </div>
</footer>''' % {
        'marca': e(marca),
        'claim': e(t(MARCA['claim'], lang)),
        'tel_link': NEGOCIO['tel_link'],
        'tel': e(NEGOCIO['tel_humano']),
        'correo': e(NEGOCIO['correo']),
        't_paginas': e('La web' if lang == 'es' else 'La web'),
        'paginas': paginas,
        't_legal': e('Información legal' if lang == 'es' else 'Informació legal'),
        'raiz': raiz,
        'l_aviso': e(mc['enlace_aviso_legal']),
        'li_cond': (('          <li><a href="legal.html#condiciones">%s</a></li>\n'
                    % (e('Condiciones del servicio' if lang == 'es'
                              else 'Condicions del servici')))
                   if CONDICIONES else ''),
        'l_priv': e(mc['enlace_privacidad']),
        'l_cook': e(mc['enlace_cookies']),
        'anyo': HOY.year,
        'derechos': e(mc['pie_derechos']),
        'sin_cookies': e(sin_cookies),
        'hecha': e(mc['pie_hecho_por']),
    }


def documento(lang, pagina, titulo, descripcion, cuerpo, jsonld=None, og=None):
    raiz = IDIOMAS[lang]['raiz']
    base = NEGOCIO['url'].rstrip('/') + '/'
    ruta = '' if pagina == 'index.html' else pagina
    url_es = base + ruta
    url_va = base + 'va/' + ruta
    canonical = url_va if lang == 'va' else url_es

    extra = ''
    if jsonld:
        extra = '\n<script type="application/ld+json">\n%s\n</script>' % json.dumps(
            jsonld, ensure_ascii=False, indent=2)

    og = og or {}
    return '''<!DOCTYPE html>
<html lang="%(lang)s" id="top">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titulo)s</title>
<meta name="description" content="%(desc)s">
<meta name="author" content="%(titular)s">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="%(canonical)s">
<link rel="alternate" hreflang="es-ES" href="%(url_es)s">
<link rel="alternate" hreflang="ca-ES-valencia" href="%(url_va)s">
<link rel="alternate" hreflang="x-default" href="%(url_es)s">
<meta property="og:type" content="website">
<meta property="og:locale" content="%(oglocale)s">
<meta property="og:site_name" content="%(marca)s">
<meta property="og:title" content="%(og_titulo)s">
<meta property="og:description" content="%(og_desc)s">
<meta property="og:url" content="%(canonical)s">
<meta property="og:image" content="%(og_img)s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#16483a">
<link rel="icon" href="%(raiz)sfavicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="%(raiz)sicono-180.png">
<link rel="stylesheet" href="%(raiz)scss/fuentes.css">
<link rel="stylesheet" href="%(raiz)scss/estilos.css">
<script>document.documentElement.className+=' js';</script>%(extra)s
</head>
<body>
%(cuerpo)s
<script src="%(raiz)sjs/app.js" defer></script>
</body>
</html>
''' % {
        'lang': IDIOMAS[lang]['lang'],
        'titulo': e(titulo),
        'desc': e(descripcion),
        'titular': e(NEGOCIO['titular']),
        'canonical': e(canonical),
        'url_es': e(url_es),
        'url_va': e(url_va),
        'oglocale': 'es_ES' if lang == 'es' else 'ca_ES',
        'marca': e(NEGOCIO['marca_va'] if lang == 'va' else NEGOCIO['marca']),
        'og_titulo': e(og.get('titulo', titulo)),
        'og_desc': e(og.get('desc', descripcion)),
        'og_img': e(base + 'img/portada.png'),
        'raiz': raiz,
        'extra': extra,
        'cuerpo': cuerpo,
    }


def envoltorio(lang, pagina, titulo, descripcion, secciones, jsonld=None, og=None):
    mc = MARCA['microcopy'][lang]
    cuerpo = '\n\n'.join(
        [cabecera_html(lang, mc, pagina), '<main id="contenido">'] +
        secciones +
        ['</main>', pie_html(lang, mc), franja_movil(lang)])
    return documento(lang, pagina, titulo, descripcion, cuerpo, jsonld=jsonld, og=og)


# ---------------------------------------------------------------------------
# Piezas reutilizables
# ---------------------------------------------------------------------------
def cabecera_pagina(lang, eyebrow, titulo, entradilla=''):
    """El antetítulo sólo se pinta si dice algo distinto del título."""
    partes = []
    if eyebrow and eyebrow.strip().lower() != titulo.strip().lower():
        partes.append('      <p class="eyebrow">%s</p>' % e(eyebrow))
    partes.append('      <h1>%s</h1>' % e(titulo))
    if entradilla:
        partes.append('      <p>%s</p>' % e(entradilla))
    return '<div class="seccion__cab">\n%s\n    </div>' % '\n'.join(partes)


def bloque_cta(lang, cta, nivel='h2'):
    return '''<div class="cta">
  <div>
    <%(n)s>%(tit)s</%(n)s>
    <p>%(txt)s</p>
  </div>
  <div class="cta__botones">
    <a class="btn btn--tel" href="tel:%(tel_link)s">%(ic_tel)s %(tel)s</a>
    <a class="btn btn--linea" href="%(wa)s" target="_blank" rel="noopener">%(ic_wa)s WhatsApp</a>
  </div>
</div>''' % {
        'n': nivel,
        'tit': e(t(cta['titulo'], lang)),
        'txt': e(t(cta['texto'], lang)),
        'tel_link': NEGOCIO['tel_link'],
        'ic_tel': icono('tel', 21),
        'tel': e(NEGOCIO['tel_humano']),
        'wa': wa_url(lang),
        'ic_wa': icono('wa', 21),
    }


def placa_telefono(lang, nota=None):
    et = 'Llámame y hablamos' if lang == 'es' else "Crida'm i parlem"
    nota = nota or (MARCA['microcopy'][lang]['urgencias'])
    if lang == 'es':
        filas = [
            (icono('reloj', 19), 'De lunes a viernes, de 9 a 14 y de 16 a 20. '
                                 'Sábados de 10 a 13.'),
            (icono('tel', 19),   'Si no te lo cojo es que estoy en casa de otro cliente. '
                                 'Te devuelvo la llamada el mismo día.'),
            (icono('persona', 19), 'Puede llamarme un hijo o un nieto por ti. '
                                   'No hace falta que llames tú.'),
            (icono('casa', 19),  'Voy yo a tu casa. No tienes que mover el ordenador.'),
        ]
    else:
        filas = [
            (icono('reloj', 19), 'De dilluns a divendres, de 9 a 14 i de 16 a 20. '
                                 'Dissabtes de 10 a 13.'),
            (icono('tel', 19),   "Si no t'ho agafe, és que estic fent faena en una altra casa. "
                                 'Et torne a cridar el mateix dia.'),
            (icono('persona', 19), 'Em pot cridar un fill o un net per tu. '
                                   'No cal que em crides tu.'),
            (icono('casa', 19),  "Vaig jo a casa teua. No has de moure l'ordinador."),
        ]
    return '''<div class="placa">
  <p class="placa__et">%(et)s</p>
  <a class="placa__num" href="tel:%(tel_link)s">%(tel)s</a>
  <p class="placa__nota">%(nota)s</p>
  <div class="placa__botones">
    <a class="btn btn--tel btn--ancho" href="tel:%(tel_link)s">%(ic_tel)s %(b_llamar)s</a>
    <a class="btn btn--linea btn--ancho" href="%(wa)s" target="_blank" rel="noopener">%(ic_wa)s WhatsApp</a>
  </div>
  <div class="placa__pie">
%(filas)s
  </div>
</div>''' % {
        'et': e(et),
        'tel_link': NEGOCIO['tel_link'],
        'tel': e(NEGOCIO['tel_humano']),
        'nota': e(nota),
        'ic_tel': icono('tel', 21),
        'b_llamar': e('Llamar ahora' if lang == 'es' else "Crida'm ara"),
        'wa': wa_url(lang),
        'ic_wa': icono('wa', 21),
        'filas': '\n'.join('<div>%s<span>%s</span></div>' % (ic, e(x)) for ic, x in filas),
    }


def seccion_hero(lang):
    pueblo = NEGOCIO['poblacion_va'] if lang == 'va' else NEGOCIO['poblacion']
    return '''<section class="hero">
  <div class="env hero__grid">
    <div>
      <p class="hero__ubi">%s %s</p>
      <h1>%s</h1>
      <p class="hero__sub">%s</p>
    </div>
    %s
  </div>
</section>''' % (icono('lugar', 17), e(pueblo),
                 e(t(HERO['h1'], lang)), e(t(HERO['lead'], lang)),
                 placa_telefono(lang))


def seccion_problemas(lang):
    """Cuatro categorías amplias. Antes había frases de ejemplo, pero prometían
    cosas que Néstor no hace y otras que no aportaban nada."""
    if lang == 'es':
        tit = '¿Qué necesitas?'
        pie = 'Si no sabes en cuál entra lo tuyo, llámame y te lo digo yo.'
        ver = 'Ver todo lo que hago'
        items = [
            ('herramienta', 'casa', 'Algo va mal en el ordenador o en el móvil',
             'Va lento, no arranca, se llena de anuncios o no imprime. Voy a tu casa, lo miro y te lo dejo funcionando.'),
            ('chat', 'casa', 'Necesitas algo concreto con un programa',
             'Instalar, configurar, recuperar una cuenta, guardar las fotos o aprender a manejarlo tú.'),
            ('chip', 'medida', 'Quieres algo hecho a medida',
             'Una página web, una tienda o una aplicación pensada para tu manera de trabajar.'),
            ('flecha', 'medida', 'Inteligencia artificial para tu negocio',
             'Un asistente que responde con tus propios documentos, o automatizar lo que ahora haces a mano.'),
        ]
    else:
        tit = 'Què necessites?'
        pie = "Si no saps en quina entra això teu, crida'm i t'ho dic jo."
        ver = 'Vore tot el que faig'
        items = [
            ('herramienta', 'casa', "Alguna cosa va mal en l'ordinador o en el mòbil",
             "Va lent, no arranca, s'ompli d'anuncis o no imprimix. Vaig a ta casa, ho mire i t'ho deixe funcionant."),
            ('chat', 'casa', 'Necessites alguna cosa concreta amb un programa',
             "Instal·lar, configurar, recuperar un compte, guardar les fotos o aprendre a manejar-ho tu."),
            ('chip', 'medida', 'Vols alguna cosa feta a mida',
             'Una pàgina web, una botiga o una aplicació pensada per a la teua manera de treballar.'),
            ('flecha', 'medida', 'Intel·ligència artificial per al teu negoci',
             "Un assistent que respon amb els teus propis documents, o automatitzar el que ara fas a mà."),
        ]
    lis = []
    for ic, ancla, titulo, texto in items:
        lis.append('      <li><a href="servicios.html#%s">%s<strong>%s</strong>'
                   '<span>%s</span></a></li>'
                   % (ancla, icono(ic, 22), e(titulo), e(texto)))
    return ('<section class="seccion" id="problemas">' + chr(10) +
            '  <div class="env">' + chr(10) +
            '    <div class="seccion__cab"><h2>%s</h2></div>' % e(tit) + chr(10) +
            '    <ul class="necesitas">' + chr(10) + chr(10).join(lis) + chr(10) +
            '    </ul>' + chr(10) +
            '    <p class="problemas__pie">%s <a href="servicios.html">%s %s</a></p>'
            % (e(pie), e(ver), icono('flecha', 17)) + chr(10) +
            '  </div>' + chr(10) + '</section>')


def seccion_resumen_servicios(lang):
    raiz = IDIOMAS[lang]['raiz']
    iconos = {'casa': 'casa', 'negocio': 'tienda', 'medida': 'chip'}
    etiquetas = {
        'casa': ('Para tu casa' if lang == 'es' else 'Per a casa teua'),
        'negocio': ('Bares, tiendas y talleres' if lang == 'es' else 'Bars, botigues i tallers'),
        'medida': ('A medida' if lang == 'es' else 'A mida'),
    }
    tarjetas = []
    for b in SERVICIOS['bloques']:
        n = len(b['servicios'])
        ver = ('Ver los %d servicios' % n) if lang == 'es' else ('Vore els %d servicis' % n)
        titulos = [t(s['titulo'], lang) for s in b['servicios'][:5]]
        lis = ''.join('<li>%s</li>' % e(x) for x in titulos)
        resto = len(b['servicios']) - 5
        mas = ''
        if resto > 0:
            mas = '<li class="mas">%s</li>' % e(
                ('y %d cosas más' % resto) if lang == 'es' else ('i %d coses més' % resto))
        tarjetas.append('''    <article class="tarjeta">
      <p class="tarjeta__ic">%s</p>
      <h3>%s</h3>
      <p class="tarjeta__et">%s</p>
      <ul>%s%s</ul>
      <a class="tarjeta__enlace" href="servicios.html#%s">%s %s</a>
    </article>''' % (icono(iconos[b['id']], 26), e(t(b['titulo'], lang)),
                     e(etiquetas[b['id']]), lis, mas, b['id'], e(ver),
                     icono('flecha', 16)))

    tit = 'Qué hago' if lang == 'es' else 'Què faig'
    entr = ('Desde lo más sencillo hasta programar algo que todavía no existe.'
            if lang == 'es' else
            'Des del més senzill fins a programar alguna cosa que encara no existix.')
    return '''<section class="seccion seccion--alt" id="que-hago">
  <div class="env">
    <div class="seccion__cab">
      <h2>%s</h2>
      <p>%s</p>
    </div>
    <div class="tarjetas">
%s
    </div>
  </div>
</section>''' % (e(tit), e(entr), '\n'.join(tarjetas))


def seccion_tira(lang):
    items = ([
        ('escudo', 'No te pido nunca las claves del banco ni códigos por teléfono.'),
        ('euro', 'Te digo el precio antes de empezar. Sin sorpresas al final.'),
        ('reloj', 'Contesto el teléfono yo mismo. No hay centralita ni esperas.'),
    ] if lang == 'es' else [
        ('escudo', 'No et demane mai les claus del banc ni codis per telèfon.'),
        ('euro', 'Et dic el preu abans de començar. Sense sorpreses al final.'),
        ('reloj', "El telèfon l'agafe jo mateix. No hi ha centraleta ni esperes."),
    ])
    lis = '\n'.join('      <li>%s<span>%s</span></li>' % (icono(ic, 21), e(txt))
                    for ic, txt in items)
    return '<div class="tira">\n  <div class="env">\n    <ul>\n%s\n    </ul>\n  </div>\n</div>' % lis


def seccion_zona_corta(lang):
    """El pueblo es el nicho. El resto, avisando con antelación."""
    otros = PRECIOS['zona']['ampliada'][:8]
    pueblo = NEGOCIO['poblacion_va'] if lang == 'va' else NEGOCIO['poblacion']
    raiz = IDIOMAS[lang]['raiz']
    if lang == 'es':
        tit = 'Dónde voy'
        principal = 'Trabajo en %s' % pueblo
        sub_p = 'Aquí vivo. Vengo el mismo día si puedo, y el desplazamiento no se cobra.'
        tit_otros = 'A los pueblos de alrededor, avisando con antelación'
        sub_o = ('También me desplazo, pero hay que avisar con tiempo para cuadrarlo con '
                 'las visitas del día.')
        ver = 'Ver todos los pueblos'
    else:
        tit = 'On vaig'
        principal = 'Treballe a %s' % pueblo
        sub_p = 'Visc ací. Si puc, vinc el mateix dia, i el desplaçament no te\'l cobre.'
        tit_otros = 'Als pobles del voltant, avisant amb temps'
        sub_o = ("També hi vaig, però m'has d'avisar amb temps per a quadrar-ho amb les "
                 'altres visites del dia.')
        ver = 'Vore tots els pobles'
    chips = ''.join('<li><span>%s</span></li>' % e(x.split(' (')[0]) for x in otros)
    return '''<section class="seccion" id="zona">
  <div class="env">
    <div class="seccion__cab"><h2>%s</h2></div>
    <div class="zona">
      <div class="zona__caja zona__caja--base">
        <p class="zona__ic">%s</p>
        <h3>%s</h3>
        <p class="sub">%s</p>
      </div>
      <div class="zona__caja">
        <h3>%s</h3>
        <p class="sub">%s</p>
        <ul class="pueblos">%s</ul>
        <p class="sub"><a href="contacto.html#zona-completa">%s %s</a></p>
      </div>
    </div>
  </div>
</section>''' % (e(tit), icono('lugar', 30), e(principal), e(sub_p),
                 e(tit_otros), e(sub_o), chips, e(ver), icono('flecha', 16))


def normalizar_jsonld(datos):
    """Los datos estructurados tienen que apuntar SIEMPRE al dominio de
    NEGOCIO['url']. Si no, el aviso legal dice un dominio y Google lee otro."""
    base = NEGOCIO['url'].rstrip('/') + '/'
    copia = json.loads(json.dumps(datos))

    def arreglar(obj):
        if isinstance(obj, dict):
            # Solo se sustituyen las direcciones antiguas de GitHub Pages. Una regla
            # generica rompia rutas como https://dominio.es/img/... con dominio propio.
            return {k: (re.sub(r'https://nsorlop\.github\.io/[^/#]*/', base, v)
                        if isinstance(v, str) and k in ('@id', 'url', 'image', 'logo')
                        else arreglar(v))
                    for k, v in obj.items()}
        if isinstance(obj, list):
            return [arreglar(x) for x in obj]
        return obj

    copia = arreglar(copia)
    copia['url'] = NEGOCIO['url']
    # Que apunten a ficheros que existen de verdad, no a nombres inventados
    copia['image'] = base + 'img/portada.png'
    copia['logo'] = base + 'favicon.svg'
    return copia


def pagina_inicio(lang):
    meta = SEO['meta'][lang]
    jsonld = normalizar_jsonld(SEO['jsonld'])
    secciones = [
        seccion_hero(lang),
        seccion_tira(lang),
        seccion_problemas(lang),
        seccion_resumen_servicios(lang),
        seccion_zona_corta(lang),
        '<section class="seccion seccion--alt"><div class="env">%s</div></section>'
        % bloque_cta(lang, MARCA['cta_bloques'][0]),
    ]
    return envoltorio(lang, 'index.html', meta['title'], meta['description'], secciones,
                      jsonld=jsonld,
                      og={'titulo': meta['og_title'], 'desc': meta['og_description']})


# ---------------------------------------------------------------------------
# PÁGINA: QUÉ HAGO
# ---------------------------------------------------------------------------
def _servicio_bloque(s, lang):
    return '''  <div class="bloque-serv">
    <h3>%s</h3>
    <p>%s</p>
  </div>''' % (e(t(s['titulo'], lang)), e(t(s['desc'], lang)))


def pagina_servicios(lang):
    etiquetas = {
        'casa': ('Para tu casa' if lang == 'es' else 'Per a casa teua'),
        'negocio': ('Bares, tiendas y talleres' if lang == 'es' else 'Bars, botigues i tallers'),
        'medida': ('A medida' if lang == 'es' else 'A mida'),
    }
    partes = []
    for b in SERVICIOS['bloques']:
        oscuro = ' banda-fosca' if b['id'] == 'medida' else ''
        partes.append('''<section class="seccion%s" id="%s">
  <div class="env">
    <div class="nivel__cab">
      <h2>%s</h2>
      <span class="nivel__para">%s</span>
      <p class="nivel__entrada">%s</p>
    </div>
    <div class="rejilla-serv">
%s
    </div>
  </div>
</section>''' % (oscuro, b['id'], e(t(b['titulo'], lang)), e(etiquetas[b['id']]),
                 e(t(b['entradilla'], lang)),
                 '\n'.join(_servicio_bloque(s, lang) for s in b['servicios'])))

    nh = SERVICIOS['no_hago']
    partes.append('''<section class="seccion">
  <div class="env">
    <div class="no-hago">
      <h2>%s</h2>
      <ul>%s</ul>
    </div>
    %s
  </div>
</section>''' % (e(t(nh['titulo'], lang)),
                 ''.join('<li>%s</li>' % e(t(i, lang)) for i in nh['items']),
                 bloque_cta(lang, MARCA['cta_bloques'][1])))

    tit = 'Qué hago' if lang == 'es' else 'Què faig'
    entr = ('Todo lo que puedo hacerte, de lo más sencillo a lo más complicado. '
            'Si no sabes en qué grupo entra lo tuyo, llama y te lo digo yo.'
            if lang == 'es' else
            'Tot el que puc fer-te, des del més senzill fins al més complicat. '
            "Si no saps en quin grup entra el teu cas, crida'm i t'ho dic jo.")
    cab = '''<section class="seccion seccion--intro">
  <div class="env">
%s
  </div>
</section>''' % cabecera_pagina(lang, t(SEO['h1'], lang)[:0] or tit, tit, entr)

    desc = ('Ordenadores, móviles, wifi, impresoras, copias de seguridad, páginas web, '
            'aplicaciones a medida y automatizaciones. Servicio a domicilio en %s.'
            % NEGOCIO['poblacion'] if lang == 'es' else
            'Ordinadors, mòbils, wifi, impressores, còpies de seguretat, pàgines web, '
            'aplicacions a mida i automatitzacions. Servici a domicili a %s.'
            % NEGOCIO['poblacion_va'])
    titulo = ('Qué hago · %s' % NEGOCIO['marca'] if lang == 'es'
              else 'Què faig · %s' % NEGOCIO['marca_va'])
    return envoltorio(lang, 'servicios.html', titulo, desc, [cab] + partes)


# ---------------------------------------------------------------------------
# PÁGINA: PRECIOS
# ---------------------------------------------------------------------------
def pagina_precios(lang):
    cab = ['Qué es' if lang == 'es' else 'Què és',
           'Qué incluye' if lang == 'es' else 'Què inclou',
           'Precio' if lang == 'es' else 'Preu']
    filas = '\n'.join(
        '      <tr><th scope="row">%s</th><td class="incluye">%s</td><td class="precio" data-et="%s">%s</td></tr>'
        % (e(t(f['concepto'], lang)), e(t(f['incluye'], lang)),
           e('Precio' if lang == 'es' else 'Preu'), e(t(f['precio'], lang)))
        for f in PRECIOS['tarifas'])

    tiempos = '\n'.join(
        '      <tr><th scope="row">%s</th><td class="precio" data-et="%s">%s</td></tr>'
        % (e(t(x['tarea'], lang)),
           e('Cuánto suele llevar' if lang == 'es' else 'Quant sol portar'),
           e(t(x['tiempo'], lang)))
        for x in PRECIOS['ejemplos_tiempo'])

    cf = CONFIANZA['como_funciona']
    pasos = '\n'.join('    <li><h3>%s</h3><p>%s</p></li>' %
                      (e(t(p['titulo'], lang)), e(t(p['desc'], lang))) for p in cf['pasos'])
    com = CONFIANZA['compromisos']
    comps = '\n'.join('    <li>%s<strong>%s</strong><span>%s</span></li>' %
                      (icono('check', 21), e(t(c['titulo'], lang)), e(t(c['desc'], lang)))
                      for c in com['items'])

    secciones = ['''<section class="seccion seccion--intro">
  <div class="env">
%s
    <div class="tabla-envoltorio">
      <table class="tarifas">
        <thead><tr><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th></tr></thead>
        <tbody>
%s
        </tbody>
      </table>
    </div>
    <div class="notas-precio">%s</div>
  </div>
</section>''' % (cabecera_pagina(lang, t(PRECIOS['titulo_precios'], lang),
                                 t(PRECIOS['titulo_precios'], lang),
                                 t(PRECIOS['aviso'], lang)),
                 e(cab[0]), e(cab[1]), e(cab[2]), filas,
                 lista_ul(PRECIOS['notas'], lang)),

                 '''<section class="seccion seccion--alt">
  <div class="env">
    <div class="seccion__cab">
      <h2>%s</h2>
      <p>%s</p>
    </div>
    <div class="tabla-envoltorio">
      <table class="tarifas">
        <thead><tr><th scope="col">%s</th><th scope="col">%s</th></tr></thead>
        <tbody>
%s
        </tbody>
      </table>
    </div>
  </div>
</section>''' % (e(t(PRECIOS['titulo_tiempo'], lang)), e(t(PRECIOS['aviso_tiempo'], lang)),
                 e('Qué' if lang == 'es' else 'Què'),
                 e('Cuánto suele llevar' if lang == 'es' else 'Quant sol portar'), tiempos),

                 '''<section class="seccion">
  <div class="env">
    <div class="seccion__cab"><h2>%s</h2></div>
    <p class="lead">%s</p>
  </div>
</section>''' % (e(t(PRECIOS['titulo_desarrollo'], lang)), e(t(PRECIOS['desarrollo'], lang))),

                 '''<section class="seccion seccion--alt">
  <div class="env">
    <div class="seccion__cab"><h2>%s</h2></div>
    <ol class="pasos">
%s
    </ol>
  </div>
</section>''' % (e(t(cf['titulo'], lang)), pasos),

                 '''<section class="seccion">
  <div class="env">
    <div class="seccion__cab"><h2>%s</h2></div>
    <ul class="compromisos">
%s
    </ul>
    %s
  </div>
</section>''' % (e(t(com['titulo'], lang)), comps, bloque_cta(lang, MARCA['cta_bloques'][0]))]

    titulo = ('Precios · %s' % NEGOCIO['marca'] if lang == 'es'
              else 'Preus · %s' % NEGOCIO['marca_va'])
    desc = ('Precios orientativos del servicio informático a domicilio: visita, hora de '
            'trabajo, puesta a punto, disco SSD y clases. Presupuesto cerrado antes de empezar.'
            if lang == 'es' else
            'Preus orientatius del servici informàtic a domicili: visita, hora de faena, '
            'posada a punt, disc SSD i classes. Pressupost tancat abans de començar.')
    return envoltorio(lang, 'precios.html', titulo, desc, secciones)


# ---------------------------------------------------------------------------
# PÁGINA: QUIÉN SOY
# ---------------------------------------------------------------------------
def pagina_sobre_mi(lang):
    cred = '\n'.join(
        '      <li><span class="et">%s</span><span class="val">%s</span></li>' %
        (e(t(c['etiqueta'], lang)), e(t(c['detalle'], lang)))
        for c in SOBRE['credenciales'])
    proy = '\n'.join(
        '''    <article class="proyecto">
      <h3>%s</h3>
      <p>%s</p>
      <p class="para-ti">%s</p>
    </article>''' % (e(p['nombre']), e(t(p['que'], lang)), e(t(p['para_ti'], lang)))
        for p in SOBRE['proyectos'])
    tit_p = 'Cosas que he construido' if lang == 'es' else 'Coses que he fet'
    ver = ('Puedes ver el código de estos proyectos en mi GitHub y en mi portfolio:'
           if lang == 'es' else
           'Pots vore el codi d\'estos projectes en el meu GitHub i en el meu portfolio:')

    secciones = ['''<section class="seccion seccion--intro">
  <div class="env">
%s
    <div class="sobre">
      <div class="sobre__bio">
%s
      </div>
      <ul class="credenciales">
%s
      </ul>
    </div>
  </div>
</section>''' % (cabecera_pagina(lang, t(SOBRE['titulo'], lang), t(SOBRE['titulo'], lang)),
                 parrafos(SOBRE['bio'], lang), cred),

                 '''<section class="seccion seccion--alt">
  <div class="env">
    <div class="seccion__cab">
      <h2>%s</h2>
      <p>%s</p>
    </div>
    <div class="proyectos">
%s
    </div>
    <p class="notas-precio">%s <a href="%s" target="_blank" rel="noopener">github.com/nsorlop</a> &middot; <a href="%s" target="_blank" rel="noopener">nsorlop.github.io</a></p>
  </div>
</section>''' % (e(tit_p),
                 e('Proyectos míos, funcionando. Cuento para qué le puede servir a un '
                   'negocio de aquí cada uno de ellos.' if lang == 'es' else
                   'Projectes meus que ja funcionen. De cada un, et conte per a què li pot '
                   "servir a un negoci d'ací."),
                 proy, e(ver), NEGOCIO['github'], NEGOCIO['portfolio']),

                 '<section class="seccion"><div class="env">%s</div></section>'
                 % bloque_cta(lang, MARCA['cta_bloques'][0])]

    titulo = ('Quién soy · %s' % NEGOCIO['marca'] if lang == 'es'
              else 'Qui soc · %s' % NEGOCIO['marca_va'])
    desc = ('Néstor Soriano, de La Font de la Figuera. Graduado en Ingeniería Informática '
            'por la UPV, con experiencia en el departamento de sistemas de una empresa.'
            if lang == 'es' else
            'Néstor Soriano, de la Font de la Figuera. Graduat en Enginyeria Informàtica '
            'per la UPV, amb experiència en el departament de sistemes d\'una empresa.')
    return envoltorio(lang, 'sobre-mi.html', titulo, desc, secciones)


# ---------------------------------------------------------------------------
# PÁGINA: PREGUNTAS
# ---------------------------------------------------------------------------
def bloque_identidad(lang):
    """Va justo detrás del aviso de estafas. Sin esto, el aviso asusta y no da
    salida: quien vive solo se queda con el miedo puesto y no llama."""
    if lang == 'es':
        tit = 'Así sabrás que el que llama a tu puerta soy yo'
        intro = ('El aviso de arriba sirve para protegerte, no para que te dé miedo abrir la '
                 'puerta. Esto es lo que hago siempre, y si algo no cuadra, no abras.')
        items = [
            'Te llamo antes de salir y te digo a qué hora llego.',
            'Voy solo y me presento con mi nombre y mi apellido: Néstor Soriano.',
            'Si quieres, pídeme el DNI en la puerta. No me molesta, es lo normal.',
            'Si viene alguien diciendo que va de mi parte y yo no te he avisado antes por '
            'teléfono, no le abras y llámame al 644 21 91 18.',
            'Nunca te pido dinero por adelantado, ni las claves del banco, ni códigos del móvil.',
            'Puedes tener a alguien de tu familia contigo mientras trabajo. Me parece bien y '
            'no me estorba.',
        ]
    else:
        tit = 'Així sabràs que qui et toca a la porta soc jo'
        intro = ("L'avís de dalt és per a protegir-te, no perquè et faça por obrir la "
                 'porta. Açò és el que faig sempre. Si alguna cosa no quadra, no obris.')
        items = [
            "Et cride abans d'eixir de casa i et dic a quina hora aplegue.",
            'Vaig a soles i em presente amb el meu nom i el meu cognom: Néstor Soriano.',
            "Si vols, demana'm el DNI a la porta. No em molesta, és normal.",
            "Si ve algú dient que va de part meua i jo no t'he avisat abans per telèfon, "
            "no li obris i crida'm al 644 21 91 18.",
            'Mai et demane diners per avançat, ni les claus del banc, ni codis del mòbil.',
            'Pots tindre algú de la teua família amb tu mentres faig faena. Em pareix bé i no '
            'em fa nosa.',
        ]
    lis = chr(10).join('        <li>%s%s</li>' % (icono('check', 19), e(x)) for x in items)
    return ('<section class="seccion" id="quien-soy-yo">' + chr(10) +
            '  <div class="env">' + chr(10) +
            '    <div class="identidad">' + chr(10) +
            '      <div class="identidad__cab">' + chr(10) +
            '        %s' % icono('escudo', 30) + chr(10) +
            '        <h2>%s</h2>' % e(tit) + chr(10) +
            '      </div>' + chr(10) +
            '      <p>%s</p>' % e(intro) + chr(10) +
            '      <ul>' + chr(10) + lis + chr(10) + '      </ul>' + chr(10) +
            '    </div>' + chr(10) + '  </div>' + chr(10) + '</section>')


def pagina_preguntas(lang):
    faq = CONFIANZA['faq']
    items = '\n'.join('''    <details id="p%d">
      <summary>%s</summary>
      <div class="resp"><p>%s</p></div>
    </details>''' % (i, e(t(f['p'], lang)), e(t(f['r'], lang)))
                      for i, f in enumerate(faq['items'], 1))

    est = CONFIANZA['estafas']
    entradilla = ('Las dudas que me plantean más a menudo. Si te queda alguna, '
                  'llámame y te la contesto.' if lang == 'es' else
                  "Les preguntes que més em fan. Si et queda algun dubte, "
                  "crida'm i t'ho aclarisc.")
    pista = ('Toca una pregunta y se abre la respuesta.' if lang == 'es'
             else "Toca una pregunta i s'obri la resposta.")
    secciones = ['''<section class="seccion seccion--intro">
  <div class="env">
%s
    <p class="faq__pista">%s</p>
    <div class="faq">
%s
    </div>
  </div>
</section>''' % (cabecera_pagina(lang, t(faq['titulo'], lang), t(faq['titulo'], lang),
                                 entradilla), e(pista),
                 items),

                 '''<section class="seccion seccion--alt" id="estafas">
  <div class="env">
    <div class="estafa">
      <div class="estafa__cab">
        %s
        <h2>%s</h2>
      </div>
      %s
      <div class="estafa__senales">
        <h3>%s</h3>
        %s
      </div>
      <p class="estafa__cierre">%s</p>
    </div>
  </div>
</section>''' % (icono('aviso', 32), e(t(est['titulo'], lang)),
                 parrafos(est['intro'], lang),
                 e(t(est['senales']['titulo'], lang)),
                 lista_ul(est['senales']['items'], lang),
                 e(t(est['cierre'], lang))),
                 bloque_identidad(lang)]

    titulo = ('Preguntas frecuentes · %s' % NEGOCIO['marca'] if lang == 'es'
              else 'Preguntes freqüents · %s' % NEGOCIO['marca_va'])
    desc = ('Cuánto cuesta, cuándo voy, a qué pueblos me desplazo, si hago factura y qué '
            'pasa con tus fotos y tus datos. Y cómo reconocer las estafas por teléfono.'
            if lang == 'es' else
            "Quant costa, quan puc anar, a quins pobles vaig, si faig factura i què "
            'passa amb les teues fotos i les teues dades. I com reconéixer les estafes per telèfon.')
    faq_ld = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'inLanguage': IDIOMAS[lang]['lang'],
        'mainEntity': [{
            '@type': 'Question',
            'name': t(f['p'], lang),
            'acceptedAnswer': {'@type': 'Answer', 'text': t(f['r'], lang)},
        } for f in faq['items']],
    }
    return envoltorio(lang, 'preguntas.html', titulo, desc, secciones, jsonld=faq_ld)


# ---------------------------------------------------------------------------
# PÁGINA: CONTACTO
# ---------------------------------------------------------------------------
def pagina_contacto(lang):
    mc = MARCA['microcopy'][lang]
    raiz = IDIOMAS[lang]['raiz']
    plantilla = ('Hola Néstor, soy {nombre} de {pueblo}. Mi teléfono es {telefono}. {problema}'
                 if lang == 'es' else
                 'Hola Néstor, soc {nombre} de {pueblo}. El meu telèfon és {telefono}. {problema}')
    asunto = 'Consulta desde la web' if lang == 'es' else 'Consulta des de la web'

    vias = '''      <a class="via" href="tel:%(tel_link)s">
        <span class="via__ic via__ic--tel">%(ic_tel)s</span>
        <span class="via__et">%(et_tel)s</span>
        <span class="via__val">%(tel)s</span>
      </a>
      <a class="via" href="%(wa)s" target="_blank" rel="noopener">
        <span class="via__ic via__ic--wa">%(ic_wa)s</span>
        <span class="via__et">WhatsApp</span>
        <span class="via__val">%(tel)s</span>
      </a>
      <a class="via" href="mailto:%(correo)s">
        <span class="via__ic via__ic--mail">%(ic_mail)s</span>
        <span class="via__et">%(et_correo)s</span>
        <span class="via__val">%(correo)s</span>
      </a>
      <div class="horario">
        <h3>%(ic_reloj)s %(et_hor)s</h3>
        %(horario)s
      </div>''' % {
        'tel_link': NEGOCIO['tel_link'], 'ic_tel': icono('tel', 22),
        'et_tel': e(mc['etiqueta_telefono']), 'tel': e(NEGOCIO['tel_humano']),
        'wa': wa_url(lang), 'ic_wa': icono('wa', 21),
        'correo': e(NEGOCIO['correo']), 'ic_mail': icono('mail', 22),
        'et_correo': e('Correo electrónico' if lang == 'es' else 'Correu electrònic'),
        'ic_reloj': icono('reloj', 17), 'et_hor': e(mc['etiqueta_horario']),
        'horario': parrafos(HORARIO[lang], lang),
    }

    campos_form = dict((k, e(v)) for k, v in (CAPA1_VA if lang == 'va' else CAPA1_ES).items())
    formulario = '''      <form class="formulario" id="formulario" data-plantilla="%(plantilla)s" data-asunto="%(asunto)s">
        <h2>%(f_tit)s</h2>
        <p class="ayuda">%(f_ayuda)s</p>
        <div class="campo">
          <label for="f-nombre">%(l_nombre)s</label>
          <input type="text" id="f-nombre" name="nombre" autocomplete="name" required>
        </div>
        <div class="campo">
          <label for="f-pueblo">%(l_pueblo)s</label>
          <input type="text" id="f-pueblo" name="pueblo" autocomplete="address-level2">
        </div>
        <div class="campo">
          <label for="f-telefono">%(l_tel)s <span class="pista">%(pista_tel)s</span></label>
          <input type="tel" id="f-telefono" name="telefono" autocomplete="tel" inputmode="tel" required>
        </div>
        <div class="campo">
          <label for="f-problema">%(l_prob)s <span class="pista">%(pista_prob)s</span></label>
          <textarea id="f-problema" name="problema" rows="4" placeholder="%(ph)s" required></textarea>
        </div>
        <p class="form__nota" id="form-error" hidden role="alert"><strong>%(error)s</strong></p>
        <div class="form__botones sin-js-ocultar">
          <button type="button" class="btn btn--wa" id="enviar-whatsapp">%(ic_wa)s %(b_wa)s</button>
          <button type="button" class="btn btn--mail" id="enviar-correo">%(ic_mail)s %(b_mail)s</button>
        </div>
        <p class="form__nota solo-sin-js"><strong>%(sin_js)s</strong></p>
        <p class="form__nota">%(nota)s</p>
        <div class="capa1">
          <p class="capa1__tit">%(c_tit)s</p>
          <dl>
            <div><dt>%(c1)s</dt><dd>%(v1)s</dd></div>
            <div><dt>%(c2)s</dt><dd>%(v2)s</dd></div>
            <div><dt>%(c3)s</dt><dd>%(v3)s</dd></div>
            <div><dt>%(c4)s</dt><dd>%(v4)s</dd></div>
            <div><dt>%(c5)s</dt><dd>%(v5)s</dd></div>
          </dl>
          <p><a href="legal.html#privacidad">%(ver_priv)s</a></p>
        </div>
      </form>''' % dict({
        'plantilla': e(plantilla), 'asunto': e(asunto),
        'f_tit': e(mc['form_titulo']),
        'f_ayuda': e('Rellena lo que sepas. Con el nombre, el teléfono y qué te pasa me sobra.'
                     if lang == 'es' else
                     'Ompli el que sàpies. Amb el nom, el telèfon i què et passa, ja en tinc prou.'),
        'l_nombre': e(mc['form_nombre']), 'l_pueblo': e(mc['form_pueblo']),
        'l_tel': e(mc['form_telefono']),
        'pista_tel': e('para poder devolverte la llamada' if lang == 'es'
                       else 'per a poder tornar-te a cridar'),
        'l_prob': e(mc['form_problema']),
        'pista_prob': e('cuéntalo como sepas' if lang == 'es' else 'conta-ho com sàpies'),
        'ph': e(mc['form_placeholder_problema']),
        'error': e('Rellena tu nombre, tu teléfono y qué te pasa antes de enviar.'
                   if lang == 'es' else
                   'Ompli el teu nom, el teu telèfon i què et passa abans d\'enviar-ho.'),
        'ic_wa': icono('wa', 21), 'b_wa': e(mc['form_enviar_whatsapp']),
        'ic_mail': icono('mail', 21), 'b_mail': e(mc['form_enviar_email']),
        'sin_js': e('Si no te funcionan los botones, llama al %s o escribe a %s.'
                    % (NEGOCIO['tel_humano'], NEGOCIO['correo']) if lang == 'es' else
                    "Si no et funcionen els botons, crida'm al %s o escriu-me a %s."
                    % (NEGOCIO['tel_humano'], NEGOCIO['correo'])),
        'nota': e('Este formulario no envía nada por su cuenta: abre tu WhatsApp o tu '
                  'programa de correo con el mensaje ya escrito, y tú decides si lo mandas.'
                  if lang == 'es' else
                  "Este formulari no envia res a soles: t'obri el WhatsApp o el "
                  "programa de correu amb el missatge ja escrit, i tu decidixes si l'envies."),
        'raiz': raiz,
    }, **campos_form)

    z = PRECIOS['zona']

    def pueblos(lista):
        return ''.join('<li><span>%s</span></li>' % e(p) for p in lista)

    zona = '''<section class="seccion seccion--alt" id="zona-completa">
  <div class="env">
    <div class="seccion__cab"><h2>%s</h2></div>
    <div class="zona">
      <div class="zona__caja">
        <h3>%s</h3>
        <p class="sub">%s</p>
        <ul class="pueblos">%s</ul>
      </div>
      <div class="zona__caja">
        <h3>%s</h3>
        <p class="sub">%s</p>
        <ul class="pueblos">%s</ul>
      </div>
    </div>
    <p class="notas-precio">%s</p>
  </div>
</section>''' % (e(t(PRECIOS['titulo_zona'], lang)),
                 e('Mi pueblo' if lang == 'es' else 'El meu poble'),
                 e('Aquí vivo y aquí trabajo. Sin coste de desplazamiento.' if lang == 'es'
                   else "Visc i treballe ací. El desplaçament no te'l cobre."),
                 pueblos(z['principal']),
                 e('Otros pueblos, avisando con antelación' if lang == 'es'
                   else 'Altres pobles, avisant amb temps'),
                 e('También voy, pero hay que avisar con tiempo. El desplazamiento lo '
                   'hablamos por teléfono antes de ir.' if lang == 'es'
                   else "També hi vaig, però m'has d'avisar amb temps. El desplaçament el "
                   "parlem per telèfon abans d'anar."),
                 pueblos(z['ampliada']),
                 e(t(PRECIOS['zona_nota'], lang)))

    tit = 'Contacto' if lang == 'es' else 'Contacte'
    entr = ('Llama, escribe o manda un correo, lo que te resulte más cómodo. '
            'Preguntar no cuesta nada y no te compromete a nada.'
            if lang == 'es' else
            "Crida'm, escriu-me o envia'm un correu, com et vaja millor. "
            'Preguntar no costa res i no et compromet a res.')

    secciones = ['''<section class="seccion seccion--intro">
  <div class="env">
%s
    <div class="contacto">
      <div class="vias">
%s
      </div>
%s
    </div>
  </div>
</section>''' % (cabecera_pagina(lang, tit, tit, entr), vias, formulario), zona]

    titulo = ('Contacto · %s' % NEGOCIO['marca'] if lang == 'es'
              else 'Contacte · %s' % NEGOCIO['marca_va'])
    desc = ('Llama al %s o escribe por WhatsApp. Servicio informático a domicilio en %s. '
            'A los pueblos de alrededor, avisando con antelación.'
            % (NEGOCIO['tel_humano'], NEGOCIO['poblacion']) if lang == 'es' else
            "Crida'm al %s o escriu-me per WhatsApp. Servici informàtic a domicili a %s. "
            'Als pobles del voltant, avisant amb temps.'
            % (NEGOCIO['tel_humano'], NEGOCIO['poblacion_va']))
    return envoltorio(lang, 'contacto.html', titulo, desc, secciones)


# ---------------------------------------------------------------------------
# PÁGINA: LEGAL
# ---------------------------------------------------------------------------
def doc_aviso(lang):
    secs = []
    for s in AVISO['secciones']:
        cuerpo = '\n'.join('<p>%s</p>' % marcar_huecos(p) for p in t(s['parrafos'], lang, []))
        secs.append('<h3>%s</h3>\n%s' % (e(t(s['titulo'], lang)), cuerpo))
    return '<section class="doc" id="aviso-legal">\n  <h2>%s</h2>\n  <p class="fecha">%s</p>\n%s\n</section>' % (
        e(t(AVISO['titulo'], lang)),
        e(('Última actualización: ' if lang == 'es' else 'Última actualització: ') + fecha_larga(lang)),
        '\n'.join(secs))


def doc_secciones(datos, ancla, lang):
    """Documento legal con un resumen en lenguaje llano en cada apartado."""
    et = 'En pocas palabras' if lang == 'es' else 'En poques paraules'
    secs = []
    for sec in datos['secciones']:
        trozos = []
        llano = t(sec.get('resumen_llano'), lang, '')
        if llano:
            trozos.append('<p class="llano" data-et="%s">%s</p>' % (e(et), e(llano)))
        for par in t(sec.get('parrafos'), lang, []):
            trozos.append('<p>%s</p>' % marcar_huecos(par))
        li = t(sec.get('lista'), lang, [])
        if li:
            trozos.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % marcar_huecos(x) for x in li))
        secs.append('<h3>%s</h3>' % e(t(sec['titulo'], lang)))
        secs.extend(trozos)
    fecha = ('Última actualización: ' if lang == 'es' else 'Última actualització: ') + fecha_larga(lang)
    partes = ['<section class="doc" id="%s">' % ancla,
              '  <h2>%s</h2>' % e(t(datos['titulo'], lang)),
              '  <p class="fecha">%s</p>' % e(fecha),
              parrafos(datos.get('intro'), lang)]
    partes.extend(secs)
    partes.append('</section>')
    return '\n'.join(x for x in partes if x)


def doc_privacidad(lang):
    return doc_secciones(PRIVACIDAD, 'privacidad', lang)


def doc_condiciones(lang):
    if not CONDICIONES:
        return ''
    return doc_secciones(CONDICIONES, 'condiciones', lang)


def doc_cookies(lang):
    cab = t(COOKIES['tabla']['cabeceras'], lang, [])
    filas = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % e(c) for c in t(f, lang, []))
                    for f in COOKIES['tabla']['filas'])
    tabla = ('<div class="tabla-envoltorio"><table class="tarifas"><thead><tr>%s</tr></thead>'
             '<tbody>%s</tbody></table></div>'
             % (''.join('<th scope="col">%s</th>' % e(c) for c in cab), filas))
    secs = '\n'.join('<h3>%s</h3>\n%s' % (e(t(s['titulo'], lang)), parrafos(s.get('parrafos'), lang))
                     for s in COOKIES['secciones'])
    return '<section class="doc" id="cookies">\n  <h2>%s</h2>\n  <p class="fecha">%s</p>\n%s\n%s\n%s\n</section>' % (
        e(t(COOKIES['titulo'], lang)),
        e(('Última actualización: ' if lang == 'es' else 'Última actualització: ') + fecha_larga(lang)),
        parrafos(COOKIES.get('intro'), lang), tabla, secs)


def pagina_legal(lang):
    mc = MARCA['microcopy'][lang]
    tit = ('Aviso legal, condiciones y privacidad' if lang == 'es'
           else 'Avís legal, condicions i privacitat')
    l_cond = 'Condiciones del servicio' if lang == 'es' else 'Condicions del servici'
    enlaces = [('#aviso-legal', mc['enlace_aviso_legal'])]
    if CONDICIONES:
        enlaces.append(('#condiciones', l_cond))
    enlaces += [('#privacidad', mc['enlace_privacidad']), ('#cookies', mc['enlace_cookies'])]
    nav = ('<nav class="legal__nav" aria-label="%s">\n%s\n</nav>'
           % (e(tit), '\n'.join('  <a href="%s">%s</a>' % (h, e(x)) for h, x in enlaces)))

    cuerpo = '\n\n'.join([
        cabecera_html(lang, mc, 'legal.html'),
        '<main id="contenido" class="legal"><div class="env">',
        '<h1>%s</h1>' % e(tit),
        nav,
        doc_aviso(lang), doc_condiciones(lang), doc_privacidad(lang), doc_cookies(lang),
        '</div></main>',
        pie_html(lang, mc),
        franja_movil(lang),
    ])
    desc = ('Aviso legal, política de privacidad y política de cookies de %s.'
            % NEGOCIO['marca'] if lang == 'es' else
            'Avís legal, política de privacitat i política de cookies d\'%s.'
            % NEGOCIO['marca_va'])
    return documento(lang, 'legal.html',
                     tit + ' · ' + (NEGOCIO['marca'] if lang == 'es' else NEGOCIO['marca_va']),
                     desc, cuerpo)


# ---------------------------------------------------------------------------
# Ficheros sueltos
# ---------------------------------------------------------------------------
def escribir(ruta, contenido):
    destino = os.path.join(RAIZ, ruta)
    carpeta = os.path.dirname(destino)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(destino, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(contenido)
    print('  %-22s %7d bytes' % (ruta, len(contenido.encode('utf-8'))))


def extras():
    base = NEGOCIO['url'].rstrip('/')
    escribir('robots.txt', 'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % base)

    rutas = []
    for archivo, _ in PAGINAS:
        r = '' if archivo == 'index.html' else archivo
        rutas.append(r)
        rutas.append('va/' + r)
    rutas += ['legal.html', 'va/legal.html']
    urls = '\n'.join('''  <url>
    <loc>%s/%s</loc>
    <lastmod>%s</lastmod>
    <changefreq>monthly</changefreq>
  </url>''' % (base, r, HOY.isoformat()) for r in rutas)
    escribir('sitemap.xml',
             '<?xml version="1.0" encoding="UTF-8"?>\n'
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
             + urls + '\n</urlset>\n')

    escribir('favicon.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="13" fill="#16483a"/>
  <path d="M11 30 32 13l21 17" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="19.5" y="32" width="25" height="17" rx="2.5" fill="none" stroke="#fff" stroke-width="4"/>
  <path d="M32 49v4M27 54h10" stroke="#fff" stroke-width="4" stroke-linecap="round"/>
</svg>
''')


# ---------------------------------------------------------------------------
SERVICIOS = PRIVACIDAD = COOKIES = AVISO = CONFIANZA = SOBRE = PRECIOS = SEO = MARCA = None
CONDICIONES = None


def main():
    global SERVICIOS, PRIVACIDAD, COOKIES, AVISO, CONFIANZA, SOBRE, PRECIOS, SEO, MARCA
    global CONDICIONES
    SERVICIOS = cargar('servicios')
    AVISO = cargar('legal_aviso')
    PRIVACIDAD = cargar('legal_privacidad')
    COOKIES = cargar('legal_cookies')
    CONDICIONES = cargar('legal_condiciones', obligatorio=False)
    CONFIANZA = cargar('confianza')
    SOBRE = cargar('sobre_mi')
    PRECIOS = cargar('precios_zona')
    SEO = cargar('seo')
    MARCA = cargar('marca')

    generadores = {
        'index.html': pagina_inicio,
        'servicios.html': pagina_servicios,
        'precios.html': pagina_precios,
        'sobre-mi.html': pagina_sobre_mi,
        'preguntas.html': pagina_preguntas,
        'contacto.html': pagina_contacto,
        'legal.html': pagina_legal,
    }

    print('Generando la web...')
    for archivo, gen in generadores.items():
        escribir(archivo, gen('es'))
        escribir('va/' + archivo, gen('va'))
    extras()
    print('Listo.')


if __name__ == '__main__':
    main()
