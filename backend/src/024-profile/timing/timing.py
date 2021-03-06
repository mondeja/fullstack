#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =================================================

# Decorador para cronometrar funciones

def fn_timer(miliseconds=False):
    from time import time
    from functools import wraps
    from decimal import Decimal
    def wrap_args(func): # Envoltura para insertar el
        @wraps(func)    # argumento miliseconds en el decorador
        def function_timer(*args, **kwargs):
            start_time = time()
            result = func(*args, **kwargs)
            end_time = time()
            elapsed_time = Decimal(end_time-start_time)
            unit_time = "seconds"
            if miliseconds:
                elapsed_time *= 1000
                unit_time = "miliseconds"
            print( "Total time running %s: %f %s" %
                   (func.__name__, elapsed_time,
                    unit_time) )
            return result
        return function_timer
    return wrap_args

# ================================================

# Función lenta
@fn_timer(miliseconds=True)
#@profile  # Para activar, leer la opción 5
def slow_function():
    for _ in range(50000):
        _ += 1

# Función para demostrar el uso de timeit con la consola IPython
def slow_function_2():
    for _ in range(50000):
        _ += 1

# -----------------------------------------------

# Existen varias formas de cronometrar:

if __name__ == "__main__":
    # ============================================================================

    # Opción 1 -> Decorador
    slow_function()

    # ============================================================================

    # Opción 2 -> Módulo timeit
    from timeit import timeit

    tiempo_que_tarda = timeit("[ _ for _ in range(50000) ]", # Ejecución a realizar
                              setup="pass", # Imports e inicializaciones
                              number=5) # Número de repeticiones (devuelve la media)
    print("Tiempo total:", Decimal(tiempo_que_tarda))

    """
    Con IPython, el cronometrado con timeit es más fácil.
    Podemos abrir la consola IPython, importar el módulo donde
    se encuentran nuestras funciones y ejecutar
    %timeit funcion()

    -----------------------------------------------------------------------
    Python 3.5.3 (default, Jan 19 2017, 14:11:04)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 6.2.1 -- An enhanced Interactive Python. Type '?' for help.

    In [1]: import timing

    In [2]: %timeit timing.slow_function_2()
    2.03 ms ± 2.47 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    -----------------------------------------------------------------------

    Más información:
    http://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-timeit
    """

    """
    Podemos llamarlo también como un script
    python3 -m timeit -n <numero_de_repeticiones> -r <media_de_tiempo_por_test> -s <"setup"> <"ejecución">
    """

    # =========================================================================

    # Opción 3 -> El comando time de Unix
    """
    time -p python3 measure.py

    Salida:
        real 0.08
        user 0.03
        sys 0.02

    - real indica el tiempo total ejecutando el script
    - user indica la cantidad de tiempo que la CPU gasta ejecutando el script
    - sys indica indica la cantidad de tiempo gastado en funciones a nivel de núcleo
    """

    """
    IPython también tiene una implementación de time con %time:

    -------------------------------------------------------------------
    Python 3.5.3 (default, Jan 19 2017, 14:11:04)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 6.2.1 -- An enhanced Interactive Python. Type '?' for help.

    In [1]: import timing

    In [2]: %time timing.slow_function_2()
    CPU times: user 8 ms, sys: 0 ns, total: 8 ms
    Wall time: 8.84 ms
    -------------------------------------------------------------------

    Más información:
    http://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-time
    """

    # =========================================================================

    # Opción 4 -> Módulo cProfile
    """
    python3 -m cProfile -s cumulative measure.py

    Este comando te indicará cuánto tiempo toma el script en cada función,
    así como el número de llamadas y otra información, de una forma más detallada

    # -------------------------------------------------------

    También podemos guardar los resultados en un archivo y luego cargarlos
    desde Python:

    python3 -m cProfile -o profile.stats timing.py

    import pstats
    p = pstats.Stats("profile.stats")
    p.sort_stats("cumulative")        #  <pstats.Stats instance at 0x177dcf8>
    p.print_stats()
    """

    # =========================================================================

    # Opción 5 -> Módulo line_profiler
    """
    Este módulo es útil si necesitas comprobar cuánto tiempo
    gasta la CPU en cada línea de código. Primero hay que instalarlo:

    pip3 install line_profiler

    Para usarlo hay que indicar las funciones que queremos medir
    con un decorador:  @profile

    Luego debemos llamar al script con el siguiente comando:

    kernprof -l -v measure.py

    La salida es la siguiente:
        Timer unit: 1e-06 s

        Total time: 0.074153 s
        File: measure.py
        Function: slow_function at line 28

        Line #      Hits         Time  Per Hit   % Time  Line Contents
        ==============================================================
            28                                           @fn_timer
            29                                           @profile
            30                                           def slow_function():
            31     50001        36101      0.7     48.7      for _ in range(50000):
            32     50000        38052      0.8     51.3          _ += 1
    """
    # =========================================================================


"""
Fuentes:
http://www.marinamele.com/7-tips-to-time-python-scripts-and-control-memory-and-cpu-usage
High Performance Python - Micha Gorelick & Ian Ozsvald
"""
