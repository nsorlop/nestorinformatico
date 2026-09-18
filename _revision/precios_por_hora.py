#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Los precios pasan a ser por tiempo, no paquetes cerrados.

Néstor: "el precio depende del rato". Queda la hora de trabajo, ejemplos de
cuánto suele llevar cada cosa, y para desarrollo un presupuesto por escrito.

    python _revision/precios_por_hora.py
"""
import io
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)

P = '_contenido/precios_zona.json'
d = json.load(io.open(P, encoding='utf-8'))

d['aviso'] = {
    'es': 'Cobro por el rato que estoy, no por paquetes cerrados. Lo que cuesta depende de '
          'lo que lleve arreglarlo, así que antes de ir hablamos por teléfono, te digo lo '
          'que creo que tardaré y, si veo que se alarga, te aviso antes de seguir.',
    'va': "Cobre pel rato que estic, no per paquets tancats. El que costa depén del que "
          "porte arreglar-ho, així que abans d'anar ho parlem per telèfon, et dic el que "
          "crec que tardaré i, si veig que s'allarga, t'avise abans de continuar.",
}

d['tarifas'] = [
    {'concepto': {'es': 'Llamar y preguntar', 'va': 'Cridar i preguntar'},
     'incluye': {'es': 'Me cuentas qué te pasa y te digo si tiene arreglo, cuánto puede '
                       'llevar y cuándo puedo ir.',
                 'va': "Em contes què et passa i et dic si té arreglo, quant pot portar i "
                       "quan puc anar."},
     'precio': {'es': 'Gratis', 'va': 'Gratis'}},
    {'concepto': {'es': 'La primera hora en tu casa', 'va': 'La primera hora a ta casa'},
     'incluye': {'es': 'El viaje, mirar qué le pasa y dejártelo arreglado si da tiempo en '
                       'ese rato.',
                 'va': "El viatge, mirar què li passa i deixar-t'ho arreglat si dona temps "
                       "en eixe rato."},
     'precio': {'es': '35 €, con el IVA dentro', 'va': "35 €, amb l'IVA dins"}},
    {'concepto': {'es': 'Cada media hora de más', 'va': 'Cada mitja hora de més'},
     'incluye': {'es': 'Si hace falta más rato, va por medias horas, no por horas enteras.',
                 'va': "Si fa falta més rato, va per mitges hores, no per hores senceres."},
     'precio': {'es': '15 €, con el IVA dentro', 'va': "15 €, amb l'IVA dins"}},
]

d['titulo_tiempo'] = {'es': 'Cuánto suele llevar cada cosa',
                      'va': 'Quant sol portar cada cosa'}
d['aviso_tiempo'] = {
    'es': 'Esto es lo que tardo normalmente. No es una promesa: un ordenador puede dar más '
          'guerra de la esperada, y entonces te lo digo antes de seguir.',
    'va': "Açò és el que tarde normalment. No és una promesa: un ordinador pot donar més "
          "guerra de l'esperada, i llavors t'ho dic abans de continuar.",
}
d['ejemplos_tiempo'] = [
    {'tarea': {'es': 'Poner a punto un ordenador que va lento',
               'va': 'Posar a punt un ordinador que va lent'},
     'tiempo': {'es': 'Entre hora y media y dos horas', 'va': 'Entre hora i mitja i dos hores'}},
    {'tarea': {'es': 'Quitar virus y publicidad que sale sola',
               'va': "Llevar virus i publicitat que ix a soles"},
     'tiempo': {'es': 'Entre una y dos horas', 'va': 'Entre una i dos hores'}},
    {'tarea': {'es': 'Cambiar el disco por uno SSD y pasar todas tus cosas',
               'va': 'Canviar el disc per un SSD i passar totes les teues coses'},
     'tiempo': {'es': 'Sobre dos horas, más lo que cueste el disco',
                'va': 'Sobre dos hores, més el que coste el disc'}},
    {'tarea': {'es': 'Dejar listo un ordenador o un móvil nuevo',
               'va': 'Deixar llest un ordinador o un mòbil nou'},
     'tiempo': {'es': 'Sobre hora y media, según lo que haya que pasar',
                'va': "Sobre hora i mitja, segons el que hi haja que passar"}},
    {'tarea': {'es': 'Montar la copia de seguridad de tus fotos y probarla delante de ti',
               'va': 'Muntar la còpia de seguretat de les teues fotos i provar-la davant de tu'},
     'tiempo': {'es': 'Sobre una hora, más el disco donde se guarda',
                'va': 'Sobre una hora, més el disc on es guarda'}},
    {'tarea': {'es': 'Hacer que el wifi llegue a toda la casa',
               'va': "Fer que el wifi aplegue a tota la casa"},
     'tiempo': {'es': 'Sobre una hora, más el aparato si hace falta poner uno',
                'va': "Sobre una hora, més l'aparell si fa falta posar-ne un"}},
    {'tarea': {'es': 'Instalar la impresora y dejarla funcionando desde el móvil',
               'va': 'Instal·lar la impressora i deixar-la funcionant des del mòbil'},
     'tiempo': {'es': 'Sobre una hora', 'va': 'Sobre una hora'}},
    {'tarea': {'es': 'Una clase en tu casa para aprender a manejarlo',
               'va': 'Una classe a ta casa per a aprendre a manejar-ho'},
     'tiempo': {'es': 'La hora que tú quieras', 'va': 'L\'hora que tu vullgues'}},
]

d['titulo_desarrollo'] = {'es': 'Páginas web, aplicaciones e inteligencia artificial',
                          'va': "Pàgines web, aplicacions i intel·ligència artificial"}
d['desarrollo'] = {
    'es': 'Esto no va por horas sueltas, porque no se sabe el rato hasta ver qué necesitas. '
          'Lo hablamos con calma, te digo cuántas horas creo que lleva y te paso un '
          'presupuesto por escrito antes de empezar. Así sabes el total desde el principio. '
          'Lo mismo para el mantenimiento de un negocio: según lo que haya que revisar, te '
          'digo un precio al mes y no hay sorpresas.',
    'va': "Açò no va per hores soltes, perquè no se sap el rato fins que es veu què "
          "necessites. Ho parlem amb calma, et dic quantes hores crec que porta i et passe "
          "un pressupost per escrit abans de començar. Així saps el total des del principi. "
          "El mateix per al manteniment d'un negoci: segons el que hi haja que revisar, et "
          "dic un preu al mes i no hi ha sorpreses.",
}

d['notas'] = {
    'es': [
        'En La Font de la Figuera el viaje va dentro del precio. A los pueblos de alrededor '
        'también voy, avisando con antelación, y te digo antes de salir si hay algún '
        'suplemento y cuánto es.',
        'Las piezas y el material (discos, memoria, routers, cables) van aparte. No compro '
        'nada sin consultarlo contigo antes y te digo el precio.',
        'No pido nada por adelantado. Se paga cuando el trabajo está hecho, en efectivo, por '
        'Bizum o por transferencia.',
        'Si al mirarlo resulta que no tiene arreglo, te cobro solo el rato que he estado y te '
        'digo qué te conviene hacer.',
        'Factura siempre, la pidas o no.',
    ],
    'va': [
        "A la Font de la Figuera el viatge va dins del preu. Als pobles del voltant també hi "
        "vaig, avisant amb antelació, i t'ho dic abans d'eixir si hi ha algun suplement i "
        "quant és.",
        "Les peces i el material (discs, memòria, routers, cables) van a banda. No compre res "
        "sense consultar-ho amb tu abans i et dic el preu.",
        "No demane res per avançat. Es paga quan la faena està feta, en efectiu, per Bizum o "
        "per transferència.",
        "Si en mirar-ho resulta que no té arreglo, et cobre només el rato que he estat i et "
        "dic què et convé fer.",
        "Factura sempre, la demanes o no.",
    ],
}

json.dump(d, io.open(P, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
json.load(io.open(P, encoding='utf-8'))

# La pregunta del precio en el FAQ tiene que decir lo mismo
C = '_contenido/confianza.json'
c = json.load(io.open(C, encoding='utf-8'))
for f in c['faq']['items']:
    if f['p']['es'].startswith('¿Cuánto cuesta'):
        f['r']['es'] = ('Llamar y preguntar es gratis. Si hace falta que vaya, cobro por el rato '
                        'que estoy: la primera hora en tu casa son 35 €, con el IVA y el viaje '
                        'dentro, y a partir de ahí 15 € cada media hora. Antes de ir te digo lo '
                        'que creo que tardaré, y si se alarga te aviso antes de seguir. Se paga al '
                        'terminar, en efectivo, por Bizum o por transferencia.')
        f['r']['va'] = ("Cridar i preguntar és gratis. Si fa falta que vaja, cobre pel rato que "
                        "estic: la primera hora a ta casa són 35 €, amb l'IVA i el viatge dins, i a "
                        "partir d'ahí 15 € cada mitja hora. Abans d'anar et dic el que crec que "
                        "tardaré, i si s'allarga t'avise abans de continuar. Es paga en acabar, en "
                        "efectiu, per Bizum o per transferència.")
        print('FAQ del precio actualizada')
json.dump(c, io.open(C, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
json.load(io.open(C, encoding='utf-8'))
print('tarifas:', len(d['tarifas']), '| ejemplos de tiempo:', len(d['ejemplos_tiempo']))
