from copy import copy
import re

from backend.rae.constants import (
    CLASES_QUE_PERTENECEN_A_LA_DEFINICION,
    ESPECIALIDADES,
    NO_USADAS,
    REGIONES,
)

EXPRESIONES_REGULARES = [
    (r'\([^()]*\)', ''),  # Eliminar parte entre paréntesis
    (' +', ' '),  # Eliminar espacios de más
    (r'\.\s*\.', '.'),  # Eliminar puntos adicionales que podrían haber quedado al eliminar otras partes de la definición
    (r'\s+\.', '.',),  # Eliminar espacios antes de un punto
]


def obtener_definiciones_palabra(soup):
    return soup.find_all('p', {'class': ['j', 'j1', 'j2']})


def obtener_palabra_acepcion(elemento_padre):
    header = elemento_padre.find('header')
    superindice = header.find('sup')

    if superindice:
        superindice.decompose()

    return header.text


def obtener_especialidades(c_abbrs):
    for abbr in c_abbrs:
        title = abbr.get('title')
        for especialidad in ESPECIALIDADES:
            if especialidad in title:
                return title


def obtener_regiones(c_abbrs):
    for abbr in c_abbrs:
        title = abbr.get('title')
        for region in REGIONES:
            if region in title:
                return title


def es_recursiva(definicion_html):
    definicion_html_str = str(definicion_html)
    comienzo_parentesis = definicion_html_str.find('(‖')
    fin_parentesis = definicion_html_str.find(')')
    u_span = definicion_html.find_all('span', {'class': 'u'})

    if u_span:
        posicion_u_span = definicion_html_str.find('span class="u"')
        if posicion_u_span < comienzo_parentesis or posicion_u_span > fin_parentesis:
            return True
    return False


def obtener_metadata(definicion_html):
    metadata_anterior = []
    metadata_posterior = []
    elemento = definicion_html
    guardar_metadata_posterior = False

    while elemento:
        elemento = elemento.find_next()
        id_elemento = elemento.get('id')
        if id_elemento and id_elemento != definicion_html.get('id'):  # Si tiene id y no coinciden, es otro párrafo
            break
        elif not guardar_metadata_posterior and elemento.get('data-id'):
            guardar_metadata_posterior = True
            
        clases = elemento.get('class')
        if (
            clases
            and clases[0] in ['d', 'g']
            and elemento.text not in CLASES_QUE_PERTENECEN_A_LA_DEFINICION
            and elemento.parent.get('class') != ['c']
        ):
            metadata = elemento.text
            if not guardar_metadata_posterior:
                metadata_anterior.append(metadata)
            else:
                metadata_posterior.append(metadata)

    return {
        'anterior': '|'.join(metadata_anterior),
        'posterior': '|'.join(metadata_posterior),
    }


def obtener_id_acepcion(definicion_html, elemento_padre):
    id_palabra = elemento_padre.get('id')
    id_acepcion = definicion_html.get('id')

    return f'{id_palabra}#{id_acepcion}'


def obtener_ids_sinonimos(definicion_html, elemento_padre):
    a_html = definicion_html.find('a', {'class': 'a'})
    if not a_html:
        return {}


    id_azul = a_html.get('href')
    if 'id=' not in id_azul:  # Si no tiene 'id=', es un azul parcial: a la misma palabra
        id_palabra = elemento_padre.get('id')
        id_azul = f'{id_palabra}{id_azul}'

    id_azul = id_azul.replace('/?id=', '')
    ids_otros_sinonimos = a_html.get('data-r')

    return {
        'azul': id_azul,
        'otros_sinonimos': ids_otros_sinonimos,
    }


def obtener_palabra_rae(soup):
    titulo = soup.title.string
    palabra = titulo[:titulo.find('|')-1]

    return palabra


def obtener_acepcion(definicion_html):
    # Crear una copia del elemento
    copia_definicion_html = copy(definicion_html)
    spans_a_remover = copia_definicion_html.find_all('span', {'class': ['n_acep', 'h']})
    abbrs_a_remover = copia_definicion_html.find_all('abbr', {'class': ['c', 'g']})
    elementos_a_remover = spans_a_remover + abbrs_a_remover
    # No todos los abbrs con class="d" no deben ser eliminados de la definición
    d_abbrs = copia_definicion_html.find_all('abbr', {'class': ['d']})

    for elemento in elementos_a_remover:
        elemento.decompose()
    
    for d_abbr in d_abbrs:
        if d_abbr.text not in CLASES_QUE_PERTENECEN_A_LA_DEFINICION:
            d_abbr.decompose()

    definicion = copia_definicion_html.text

    for regex in EXPRESIONES_REGULARES:
        definicion = re.sub(regex[0], regex[1], definicion)
    # Eliminar texto después del último punto
    definicion = _eliminar_texto_despues_del_ultimo_punto(definicion)
    return definicion.strip()


def _eliminar_texto_despues_del_ultimo_punto(definicion):
    ultimo_punto = definicion.rfind('.')
    return definicion[:ultimo_punto+1]


def tiene_otra_grafia(elemento_padre):
    try:
        n1 = elemento_padre.find('p', {'class': 'n1'})
        if (
            n1
            and n1.find('abbr', {'title': 'También'})
        ):
            av = n1.find('a', {'class': 'av'})
            if av and _es_monopalabra(av.text.replace(',', '').replace('.', '')):
                return True
        return False
    except Exception as exc:
        import pdb;pdb.set_trace()
        pass


def obtener_otra_grafia(elemento_padre, palabra_original, definicion_original):
    definicion = definicion_original.copy()
    elemento = elemento_padre.find('p', {'class': 'n1'})
    palabra_otra_grafia = elemento.find('a', {'class': 'av'}).text.replace(',', '').replace('.', '')

    palabra_original_dividida = palabra_original.split(',')
    palabra_original_dividida[0] = palabra_otra_grafia
    
    definicion['palabra_acepcion'] = ','.join(palabra_original_dividida)

    abbrs = elemento.find_all('abbr')
    for abbr in abbrs:
        if abbr.text in NO_USADAS:
            metadata_anterior = definicion["metadata_anterior"]
            definicion['metadata_anterior'] = f'{metadata_anterior}|{abbr.text}'
    
    return definicion


def _es_monopalabra(definicion):
    palabras = definicion.split()
    
    return len(palabras) == 1


def obtener_definiciones_de_frases(soup):
    elementos = soup.find_all('p', {'class': ['k5', 'k6', 'm']})
    
    if not elementos:
        return {}, None
    
    elemento_padre = elementos[0].parent
    frases_y_definiciones = {}
    try:
        for elemento in elementos:
            if elemento.get('class')[0] in ['k5', 'k6']:
                subfrases = _obtener_subfrases_de_frase(elemento)
                for subfrase in subfrases:
                    frases_y_definiciones[subfrase] = []
            elif elemento.get('class')[0] == 'm':
                for subfrase in subfrases:
                    frases_y_definiciones[subfrase].append(elemento)
    except Exception as exc:
        import pdb;pdb.set_trace()
        pass

    return frases_y_definiciones, elemento_padre


def _obtener_subfrases_de_frase(elemento):
    return re.split(r", u |, o ", elemento.text)
