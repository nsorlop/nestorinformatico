#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comprobaciones de la web generada: enlaces, anclas, recursos y detalles
de accesibilidad. Se ejecuta desde la raíz del proyecto:

    python _revision/comprobar.py
"""
import glob
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)


def ids_de(html):
    return set(re.findall(r'\sid="([^"]+)"', html))


def main():
    paginas = sorted(glob.glob('*.html') + glob.glob('va/*.html'))
    paginas = [p.replace(os.sep, '/') for p in paginas]
    problemas = []
    avisos = []

    cache = {}
    for pag in paginas:
        cache[pag] = open(pag, encoding='utf-8').read()

    for pag in paginas:
        base = os.path.dirname(pag)
        html = cache[pag]
        propios = ids_de(html)

        for href in re.findall(r'href="([^"]+)"', html):
            if href.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                continue
            if href.startswith('#'):
                if href != '#' and href[1:] not in propios:
                    problemas.append('%s: ancla propia #%s no existe' % (pag, href[1:]))
                continue
            ruta, _, ancla = href.partition('#')
            destino = os.path.normpath(os.path.join(base, ruta)).replace(os.sep, '/')
            if not os.path.exists(destino):
                problemas.append('%s: enlace roto %s' % (pag, href))
                continue
            if ancla and destino.endswith('.html'):
                otro = cache.get(destino) or open(destino, encoding='utf-8').read()
                if ancla not in ids_de(otro):
                    problemas.append('%s: %s no tiene el ancla #%s' % (pag, destino, ancla))

        for rec in re.findall(r'(?:src|href)="((?:\.\./)?(?:css|js|fonts|img)/[^"]+)"', html):
            destino = os.path.normpath(os.path.join(base, rec)).replace(os.sep, '/')
            if not os.path.exists(destino):
                problemas.append('%s: falta el recurso %s' % (pag, rec))

        # Que el valenciano no salte al castellano por un enlace mal puesto.
        # El unico enlace que puede cruzar de idioma es el selector, que lleva hreflang.
        for enlace in re.findall(r'<a\b[^>]*>', html):
            m = re.search(r'href="([^"]+)"', enlace)
            if not m:
                continue
            href = m.group(1)
            if href.startswith(('http', 'mailto:', 'tel:', '#')):
                continue
            cruza = href.startswith('../') if base == 'va' else href.startswith('va/')
            if cruza and 'hreflang' not in enlace:
                problemas.append('%s: el enlace %s cambia de idioma sin querer' % (pag, href))

        # Accesibilidad y buenas prácticas
        if 'user-scalable=no' in html or 'maximum-scale' in html:
            problemas.append('%s: el viewport impide hacer zoom' % pag)
        if html.count('<h1') != 1:
            avisos.append('%s: tiene %d etiquetas h1 (deberia haber una)' % (pag, html.count('<h1')))
        for img in re.findall(r'<img\b[^>]*>', html):
            if 'alt=' not in img:
                problemas.append('%s: imagen sin alt -> %s' % (pag, img[:60]))
        if 'lang=' not in html[:400]:
            problemas.append('%s: falta el idioma en la etiqueta html' % pag)
        # Nada de peticiones a servidores ajenos
        for url in re.findall(r'(?:src|href)="(https?://[^"]+)"', html):
            if not url.startswith(('https://nestorinformatico.es', 'https://github.com', 'https://nsorlop.github.io',
                                   'https://wa.me', 'https://schema.org')):
                problemas.append('%s: recurso externo %s' % (pag, url))

    total = sum(os.path.getsize(p) for p in paginas) / len(paginas)
    peso_css = sum(os.path.getsize(f) for f in glob.glob('css/*.css'))
    peso_js = sum(os.path.getsize(f) for f in glob.glob('js/*.js'))
    peso_fuentes = sum(os.path.getsize(f) for f in glob.glob('fonts/*.woff2'))

    print('Paginas revisadas: %d' % len(paginas))
    print('Peso medio de pagina: %.0f KB' % (total / 1024))
    print('CSS %.0f KB · JS %.0f KB · fuentes %.0f KB' %
          (peso_css / 1024, peso_js / 1024, peso_fuentes / 1024))
    print('Primera carga aproximada (portada + css + js + 2 fuentes): %.0f KB' %
          ((os.path.getsize('index.html') + peso_css + peso_js +
            os.path.getsize('fonts/atkinson-hyperlegible-400-latin.woff2') +
            os.path.getsize('fonts/bitter-700-latin.woff2')) / 1024))
    print()
    if problemas:
        print('PROBLEMAS (%d):' % len(problemas))
        for p in sorted(set(problemas)):
            print('  - %s' % p)
    else:
        print('Sin problemas.')
    if avisos:
        print()
        print('Avisos (%d):' % len(avisos))
        for a in sorted(set(avisos)):
            print('  - %s' % a)
    return 1 if problemas else 0


if __name__ == '__main__':
    raise SystemExit(main())
