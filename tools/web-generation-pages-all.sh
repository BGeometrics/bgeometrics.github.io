#!/bin/bash                                                                                                      

DIR=$HOME/bgeometrics.github.io
DIR_TEMP=/tmp/web

echo 
echo "#### "$(basename "$0")" ####"
echo
echo $(date)

cd $DIR/tools
./web-generation-pages-all-es.py
./web-generation-pages-all.py

cd $DIR_TEMP/es
find . -type f -wholename "$DIR_TEMP/*.html" -exec sed -i 's/flag-united-kingdom/flag-spain/g' {} +

cd $DIR/tools

cp -r $DIR_TEMP/* $DIR

cd $DIR

git pull
git add *
git commit -a -m"daily"
git push

echo $(date)
echo
