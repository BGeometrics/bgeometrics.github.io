#!/bin/bash                                                                                                      

DIR_PROYECT=$HOME/bgeometrics.github.io
DIR=$DIR_PROYECT/es
DIR_TEMP=/tmp/web

echo 
echo "#### "$(basename "$0")" ####"
echo
echo $(date)

cd $DIR_PROYECT/tools


# Sobreescribo los gráficos que ya están traducidos
echo "cp $DIR_PROYECT/tools/es/graphics/* $DIR/graphics/" 
cp $DIR_PROYECT/tools/es/graphics/* $DIR/graphics/ 

echo $(date)
echo
