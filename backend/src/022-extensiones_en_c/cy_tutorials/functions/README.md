## Funciones en Cython
Las funciones de Python poseen las siguientes características:
- Son creadas e importadas dinámicamente en tiempo de ejecución.
- Son creadas de forma anónima con la palabra clave `lambda`.
- Pueden ser definidas dentro de otra función.
- Pueden devolverse desde otras funciones.
- Pueden ser pasadas como argumento a otras funciones.
- Puden ser llamadas con argumentos posicionales u opcionales.
- Pueden ser definidas con valores por defecto.

Las funciones de C tienen un gasto de cómputo mínimo. Poseen las siguientes características:
- Pueden ser pasadas como argumento a otras funciones (pero puede ser más incómodo que en Python).
- No pueden ser definidas dentro de otra función.
- Tienen un nombre estáticamente asignado que no es modificable.
- Toman sólo argumentos posicionales.
- No soportan valores por defecto en sus parámetros.

### Funciones ordinarias de Python
> Puedes ver [el ejemplo](https://github.com/mondeja/fullstack/tree/master/backend/src/022-extensiones_en_c/cy_tutorials/functions/funciones.py)

Las funciones ordinarias de Python pueden ser llamadas desde código Cython y tienen atributos como `__name__`, son del tipo `function`, son modificables y corren en código bytecode de Python.

### Funciones Python en Cython con `def`
> Puedes ver [los ejemplos aquí](https://github.com/mondeja/fullstack/tree/master/backend/src/022-extensiones_en_c/cy_tutorials/functions/funciones_cy.pyx)

Cython soporta funciones de Python regulares definidas con la palabra clave `def`. A nivel de declaración, sólo se diferencian de las funciones de Python usuales en que están definidas dentro de un archivo de extensión `.pyx`.

Este tipo de funciones pueden ser llamadas desde código Python usual, pero tienen menos información almacenada (no tienen un atributo `__name__`, si comprobamos su tipo vemos que son `builtin_function_or_method`), no pueden ser modificables, corren código C compilado que llama a la API de CPython... aunque conservan el miembro `__doc__`.

### Funciones C en Cython con `cdef`
> Puedes ver [el ejemplo aquí](https://github.com/mondeja/fullstack/tree/master/backend/src/022-extensiones_en_c/cy_tutorials/functions/funciones_cy.pyx).

Son funciones puras de C y se comportan como tal, por lo tanto debemos declarar el tipo de variable que retornará. Pueden ser llamadas directamente desde Cython, pero para usarlas desde Python habrá que envolverlas dentro de una función `def` de Cython.

Gracias a estas funciones podemos ganar mucho en rendimiento pero perdemos las posibilidades de tipado dinámico y el resto de ventajas que nos ofrece Python.

### Combinar funciones `def` y `cdef` con `cpdef`
Este tipo de función combina características de los dos anteriores. Con esta función no necesitamos escribir una envoltura para las funciones C si queremos usarlas desde código Python ya que son llamables directamente desde allá. Si la llamamos desde Cython llamaremos a la versión C de la función, pero al llamarla desde Python llamamos a su envoltura.

Su declaración es la misma que la versión `def`, pero en lugar de usar la palabra reservada `def` usamos `cpdef`. Su rendimiento es idéntico a una función `cdef` envuelta dentro de una función `def` de Cython.

Las funciones `cpdef` tienen una limitación, debido al hecho de que deben ser dobles: sus argumentos y tipos devueltos deben ser compatibles tanto para los tipos de C como para los de Python.

_________________________________________

### Funciones `inline` `cdef` y `cpdef`
C y C++ soportan la palabra clave opcional `inline` para sugerir al compilador que reemplace la función con su cuerpo allí donde sea llamada dentro del código. El compilador es libre de ignorarla.

Cython soporta también la palabra clave `inline` para las funciones `cdef` y `cpdef` simplemente colocando `inline` después de `cdef`/`cpdef`:

```
cdef inline long c_fact(long a):
# ...
```

Cython pasa este modificador al código generado en C. Cuando es usado correctamente puede proveer mejoras de rendimiento, especialmente para funciones pequeñas llamadas repetidamente en bucles anidados, por ejemplo.

_________________________________________

### Manejo de excepciones en funciones
Una función `def` siempre devuelve algun tipo de puntero a un objeto `PyObject` a nivel de C. Esta invariante permite a Cython propagar excepciones correctamente de las funciones `def`. Los otros tipos de funciones, `cdef` y `cpdef` pueden devolver un tipo que no es de Python, lo cual hace necesario otro tipo de indicación de excepciones.

Por ejemplo, suponiendo que tenemos la siguiente función:

```
cpdef int divide_ints(int i, int j):
    return i / j
```

Si la llamamos con un valor de `j==0`, el intérprete nos mostrará el mensaje `Exception ZeroDivisionError: 'integer division or modulo by zero' in 'division.divide_ints' ignored` y la función devolverá 0.

Para propagar correctamente la excepción, Cython provee una cláusula `except` para permitir a una función `cdef` o `cpdef` comunicarse con su llamador que una excepción de Python debe o puede ocurrir durante su ejecución. Por lo tanto, hay que reescribir la función así:

```
cpdef int divide_ints(int i, int j) except? -1:
    return i / j
```

Ahora al ejecutar la misma operación lanzará la excepción `ZeroDivisionError`. 

La cláusula `except?` permite al valor `-1` actual como un centinela indicando que una función puede ocurrir. Si la función devuelve un código de error -1, Cython comprueba si el estado global de la excepción ha sido establecido, y, si es así, propaga la excepción. No hace falta que establezcamos el valor a `-1` porque Cython lo hará por nosotros. También aclarar que el valor `-1` es arbitrario y podemos establecer otro código de error.

_________________________________________