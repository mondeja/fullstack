#!/bin/bash

# Cuantos archivos hay de cada lenguaje de backend
PY=$(bash scripts/stats/file_types.sh backend/src py)
IPYNB=$(bash scripts/stats/file_types.sh backend/src ipynb)
JS=$(bash scripts/stats/file_types.sh backend/src js)
RB=$(bash scripts/stats/file_types.sh backend/src rb)
CPP=$(bash scripts/stats/file_types.sh backend/src cpp)
C=$(bash scripts/stats/file_types.sh backend/src c)
SH=$(bash scripts/stats/file_types.sh backend/src sh)
TEX=$(bash scripts/stats/file_types.sh backend/src tex)
CY=$(bash scripts/stats/file_types.sh backend/src pyx)
GO=$(bash scripts/stats/file_types.sh backend/src go)
PHP=$(bash scripts/stats/file_types.sh backend/src php)
JAVA=$(bash scripts/stats/file_types.sh backend/src java)

# Lo sacamos en JSON
printf '{"py":%d,"ipynb":%d,"js":%s,"rb":%s,"cpp":%s,"c":%s,"sh":%s,"tex":%s,"cy":%s,"go":%s,"php":%s,"java":%s}' \
  "$PY" "$IPYNB" "$JS" "$RB" "$CPP" "$C" "$SH" "$TEX" "$CY" "$GO" "$PHP" "$JAVA"
