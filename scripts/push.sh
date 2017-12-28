#!/bin/bash

# ====================================================================
echo "Preparados para hacer push a la rama principal"

                    #     PUSH BACK     #


# Obtenemos el último mensaje del último commit de la rama staging
LAST_COMMIT_MESSAGE=$(git log --oneline -n 1 master | cut -d" " -f 2-)
echo "LAST_COMMIT_MESSAGE: $LAST_COMMIT_MESSAGE"
echo

# Configuramos el entorno de TravisCI para hacer commit
git config --global user.email "travis@travis-ci.org"
git config --global user.name "travis-ci"

# Cambiamos a la rama principal
git add -A .
git commit -m "$LAST_COMMIT_MESSAGE [ci skip]"

# Subimos el proyecto a la rama principal
git push origin HEAD:master


# ====================================================================

exit 0
