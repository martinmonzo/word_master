"""
TODO: 
- dar (dejar el etc.), espumante (elminar Apl.), dubnio (dejar numero atomico y eliminar simbolo quimico), tioneo (dejar U.)
- guardar acepcion adentro de la monopalabra
- leer palabras de txt en un for
"""

from bs4 import BeautifulSoup
import requests

from backend.rae.constants import (
    COLOQUIAL,
    DESUSADO,
    ESPECIALIDADES,
    POCO_USADO,
    REGIONES,
)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def populate_definitions():
    response = requests.get('https://dle.rae.es/tres', headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    
    palabra = _obtener_palabra(soup)

    definiciones_html = _obtener_definiciones_completas(soup)
    definiciones = []
    for definicion_html in definiciones_html:
        definicion = _armar_definicion(definicion_html)
        definiciones.append(definicion)
    
    return definiciones


def _obtener_definiciones_completas(soup):
    parrafos = soup.find_all('p', {'class': ['j', 'j1', 'j2']})
    return parrafos


def _armar_definicion(definicion_html):
    definicion_dict = {
        'coloquial': _es_coloquial(definicion_html),
        'region': _obtener_region(definicion_html),
        'especialidad': _obtener_especialidades(definicion_html),
        'uso': _obtener_uso(definicion_html),
        'recursiva': _es_recursiva(definicion_html),
        'categoria_gramatical': _obtener_categoria_gramatical(definicion_html),
        'respuesta': '', # TODO: Depende si es m., f., pl., prnl., etc.
        'acepcion': None, # TODO: Ver si hay alguna etiqueta que no deba ser borrada, por ej: U. ...
        'data_id_sinonimo': None,
    }

    acepcion = _obtener_acepcion(definicion_html)
    definicion_dict['acepcion'] = acepcion
    if _es_monopalabra(acepcion):
        definicion_dict['data_id_sinonimo'] = _obtener_data_id_sinonimo(definicion_html)

    return definicion_dict


def _obtener_palabra(soup):
    titulo = soup.title.string
    palabra = titulo[:titulo.find('|')-1]

    return palabra


def _get_meanings(soup, palabra):
    _p = soup.find_all('p', {'class': ['j', 'j1', 'j2']})
    n_acep = soup.find_all('span', {'class': 'n_acep'})


def _obtener_region(definicion_html):
    c_abbrs = definicion_html.find_all('abbr', {'class': 'c'})

    for abbr in c_abbrs:
        title = abbr.get('title')
        for region in REGIONES:
            if region in title:
                return title


def _obtener_especialidades(definicion_html):
    c_abbrs = definicion_html.find_all('abbr', {'class': 'c'})

    for abbr in c_abbrs:
        title = abbr.get('title')
        for especialidad in ESPECIALIDADES:
            if especialidad in title:
                return title


def _es_coloquial(definicion_html):
    d_abbrs = definicion_html.find_all('abbr', {'class': 'd'})

    for abbr in d_abbrs:
        title = abbr.get('title')
        if title == COLOQUIAL:
            return True
    
    return False


def _es_recursiva(definicion_html):
    definicion_html_str = str(definicion_html)
    comienzo_parentesis = definicion_html_str.find('(‖')
    fin_parentesis = definicion_html_str.find(')')
    u_span = definicion_html.find_all('span', {'class': 'u'})

    if u_span:
        posicion_u_span = definicion_html_str.find('span class="u"')
        if posicion_u_span < comienzo_parentesis or posicion_u_span > fin_parentesis:
            return True

    return False


def _obtener_acepcion(definicion_html):
    spans = definicion_html.find_all('span', {'class': ['n_acep', 'h']})
    abbrs = definicion_html.find_all('abbr', {'class': ['c', 'd', 'g']})

    for elemento in spans+abbrs:
        elemento.decompose()

    definicion = definicion_html.text.strip()
    return _eliminar_parentesis_sinonimo(definicion)


def _obtener_uso(definicion_html):
    d_abbrs = definicion_html.find_all('abbr', {'class': 'd'})

    for abbr in d_abbrs:
        title = abbr.get('title')
        if title == DESUSADO:
            return DESUSADO
        elif title == POCO_USADO:
            return POCO_USADO


def _obtener_categoria_gramatical(definicion_html):
    abbr = definicion_html.find('abbr', {'class': ['d', 'g']})
    title = abbr.get('title')

    return title


def _eliminar_parentesis_sinonimo(definicion):
    if '(‖' in definicion:
        parte_entre_parentesis = definicion[definicion.find('(‖')-1:definicion.find(')')+1]
        definicion = definicion.replace(parte_entre_parentesis, "")

    return definicion


def _es_monopalabra(definicion):
    palabras = definicion.split()
    if len(palabras) == 1:
        return True
    return False


def _obtener_data_id_sinonimo(definicion_html):
    return definicion_html.find('a', {'class': 'a'}).get('href')
