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

cd $DIR_PROYECT/tools
python3 web-generation-pages-dark.py
python3 web-generation-pages-all-es.py
python3 web-generation-pages-all.py

cp -r $DIR_PROYECT/graphics/* $DIR_ES/graphics
cp -r $DIR_PROYECT/reports/* $DIR_ES/reports

# Sobreescribo los gráficos que ya están traducidos
cp $DIR_PROYECT/tools/es/graphics/* $DIR_ES/graphics/

python3 web-generation-translate-graphics.py

if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/activate" ]; then
        deactivate
fi

cd $DIR_PROYECT/tools
cp -r $DIR_TEMP/* $DIR_PROYECT

cd $DIR_PROYECT

git pull
git add *
git commit -a -m"daily"
git push

echo $(date)
echo
