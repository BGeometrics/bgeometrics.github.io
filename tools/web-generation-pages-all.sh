#!/bin/bash                                                                                                      

DIR_PROYECT=$HOME/bgeometrics.github.io
DIR_ES=$DIR_PROYECT/es
DIR_TEMP=/tmp/web

DIR_DUMP=$HOME/proyectos/bitcoin-scripts
VENV_DIR="$DIR_DUMP/bitcoin-scripts-env"

echo 
echo "#### "$(basename "$0")" ####"
echo
echo $(date)

# Virtual env python
if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/activate" ]; then
        source $VENV_DIR/bin/activate
fi

# Mismo criterio que bitcoin-scripts/git-deploy.sh: si el pull falla o deja
# archivos sin fusionar, abortar. Sin esto se generaban las paginas con
# plantillas viejas y el push final se rechazaba (2026-11-24).
safe_pull() {
    if ! git pull --no-rebase --no-edit; then
        echo "$(date '+%F %T') ERROR web-generation: git pull fallo o genero conflictos ($1). Abortando sin commit/push." >&2
        git merge --abort 2>/dev/null || true
        exit 1
    fi
    if git diff --name-only --diff-filter=U | grep -q .; then
        echo "$(date '+%F %T') ERROR web-generation: quedan archivos sin fusionar tras el pull ($1). Abortando sin commit/push." >&2
        git merge --abort 2>/dev/null || true
        exit 1
    fi
}

cd $DIR_PROYECT
safe_pull "inicio"

cd $DIR_PROYECT/tools
python3 web-generation-pages-dark.py
python3 web-generation-pages-all-es.py
python3 web-generation-pages-all.py

cp -r $DIR_PROYECT/graphics/* $DIR_ES/graphics
cp -r $DIR_PROYECT/reports/* $DIR_ES/reports

# JS compartido raiz -> es. Copia NOMINAL a proposito: NO usar assets/js/* porque
# bgeometrics.js y main.js son versiones propias del sitio ES y se machacarian.
cp $DIR_PROYECT/assets/js/bg-chart-data.js      $DIR_ES/assets/js/
cp $DIR_PROYECT/assets/js/chart-upgrade-band.js $DIR_ES/assets/js/
cp $DIR_PROYECT/assets/js/bg-auth-badge.js      $DIR_ES/assets/js/

# Sobreescribo los gráficos que ya están traducidos
cp $DIR_PROYECT/tools/es/graphics/* $DIR_ES/graphics/

python3 web-generation-pages-dark-es.py
python3 web-generation-translate-graphics.py

# Set link canonical to dark pages
python3 canonical.py

if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/activate" ]; then
        deactivate
fi

# Mode dark by default
cp $DIR_TEMP/index.html $DIR_TEMP/index_light.html
cp $DIR_TEMP/index_dark.html $DIR_TEMP/index.html

cd $DIR_PROYECT/tools
cp -r $DIR_TEMP/* $DIR_PROYECT

cd $DIR_PROYECT

safe_pull "antes del push"
git add *
git commit -a -m"daily"
git push

echo $(date)
echo
