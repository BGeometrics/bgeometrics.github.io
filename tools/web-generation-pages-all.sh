#!/bin/bash                                                                                                      

DIR_PROYECT=$HOME/bgeometrics.github.io
DIR_ES=$DIR_PROYECT/es
DIR_TEMP=/tmp/web

echo 
echo "#### "$(basename "$0")" ####"
echo
echo $(date)

cd $DIR_PROYECT/tools
./web-generation-pages-all-es.py
./web-generation-pages-all.py

#cd $DIR_TEMP/es
#find . -type f -wholename "$DIR_TEMP/*.html" -exec sed -i 's/flag-united-kingdom/flag-spain/g' {} +

cp -r $DIR_PROYECT/graphics/* $DIR_ES/graphics
cp -r $DIR_PROYECT/reports/* $DIR_ES/reports

# Sobreescribo los gráficos que ya están traducidos
cp $DIR_PROYECT/tools/es/graphics/* $DIR_ES/graphics/

./web-generation-translate-graphics.py

cd $DIR_PROYECT/tools
cp -r $DIR_TEMP/* $DIR_PROYECT

cd $DIR_PROYECT

git pull
git add *
git commit -a -m"daily"
git push

echo $(date)
echo
