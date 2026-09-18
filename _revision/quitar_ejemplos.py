#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quita las frases de ejemplo de la web.

Néstor las rechazó: había cosas que no hace y otras que no aportaban. En su
lugar, la portada lleva cuatro categorías amplias (problema con el aparato,
algo concreto con un programa, desarrollo a medida e inteligencia artificial)
y la página de servicios se queda solo con el título y la descripción.

    python _revision/quitar_ejemplos.py
"""
import io
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)


def leer(ruta):
    with io.open(ruta, encoding='utf-8') as fh:
        return fh.read()


def escribir(ruta, texto):
    with io.open(ruta, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(texto)


# ---------------------------------------------------------------------------
# 1. Fuera el campo "ejemplos" del contenido (queda en el historial de git)
# ---------------------------------------------------------------------------
p = '_contenido/servicios.json'
d = json.loads(leer(p))
quitados = 0
for b in d['bloques']:
    for s in b['servicios']:
        if s.pop('ejemplos', None) is not None:
            quitados += 1
escribir(p, json.dumps(d, ensure_ascii=False, indent=1))
json.loads(leer(p))

# ---------------------------------------------------------------------------
# 2. build.py: nueva sección de la portada y bloques de servicio sin chips
# ---------------------------------------------------------------------------
s = leer('build.py')

ini = s.index('def _chips(s, lang):')
fin = s.index('def seccion_resumen_servicios(lang):')
nuevo = '''def seccion_problemas(lang):
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


'''
s = s[:ini] + nuevo + s[fin:]

# Los bloques de servicio se quedan sin la fila de chips
viejo_bloque = '''  </div>\'\'\' % (e(t(s['titulo'], lang)), e(t(s['desc'], lang)), _chips(s, lang))'''
nuevo_bloque = '''  </div>\'\'\' % (e(t(s['titulo'], lang)), e(t(s['desc'], lang)))'''
assert viejo_bloque in s
s = s.replace(viejo_bloque, nuevo_bloque)
s = s.replace('''    <h3>%s</h3>
    <p>%s</p>%s
  </div>''', '''    <h3>%s</h3>
    <p>%s</p>
  </div>''')

escribir('build.py', s)
import ast
ast.parse(leer('build.py'))

print('Servicios que tenían ejemplos:', quitados)
print('Quedan referencias a _chips en build.py:', leer('build.py').count('_chips'))
