#!/bin/bash                                                                                                      

DIR=$HOME/bgeometrics.github.io/es
DIR_TEMP=/tmp/web

echo 
echo "#### "$(basename "$0")" ####"
echo
echo $(date)

cd $DIR/tools

./web-generation-pages-all-es.py

cd $DIR_TEMP
find . -type f -name "$DIR_TEMP/*.html" -exec sed -i 's/<html lang="en">/<html lang="es">/g' {} +

#cp $DIR_TEMP/* $DIR

#cd $DIR

#git pull
#git add *
#git commit -a -m"daily"
#git push

#echo $(date)
#echo
