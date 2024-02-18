#!/bin/bash                                                                                                      

DIR=$HOME/bgeometrics.github.io
DIR_TEMP=/tmp/web

echo 
echo "#### "$(basename "$0")" ####"
echo
echo $(date)

cd $DIR/tools

./web-generation-pages-all.py

cp $DIR_TEMP/* $DIR

cd $DIR

git pull
git commit -a -m"daily"
git push

echo $(date)
echo
