from concurrent.futures import as_completed, ThreadPoolExecutor
import time

from backend.rae.bs4.obtener_definiciones import obtener_definiciones


def poblar_bd_definiciones():
    """
    Recorre todas las palabras del listado, obtiene la definición de cada una
    en dle.rae.es/{palabra} y lo guarda en la base de datos.
    """
    start_time = time.perf_counter()

    definiciones = {}
    with open('backend/rae/listado_palabras.txt', 'r') as listado_palabras:
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = [
                executor.submit(obtener_definiciones, palabra)
                for palabra in listado_palabras
                if (not palabra.endswith('-') and not palabra.startswith('-') and not ' ' in palabra)
            ]
            for future in as_completed(futures):
                definiciones.update(future.result())

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    return definiciones, elapsed_time
