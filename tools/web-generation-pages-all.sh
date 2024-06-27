#!/bin/bash                                                                                                      

DIR=$HOME/bgeometrics.github.io
DIR_TEMP=/tmp/web

echo 
echo "#### "$(basename "$0")" ####"
echo
echo $(date)

cd $DIR/tools

./web-generation-pages-all.py

#cd $DIR/tools/es
#./web-generation-pages-all.py

#cd $DIR_TEMP/es
#find . -type f -name "$DIR_TEMP/*.html" -exec sed -i 's/<html lang="en">/<html lang="es">/g' {} +
#find . -type f -name "$DIR_TEMP/*.html" -exec sed -i 's/flag-united-kingdom flag m-0/flag-spain flag m-0/g' {} +

cp $DIR_TEMP/* $DIR

cd $DIR

git pull
git add *
git commit -a -m"daily"
git push

echo $(date)
echo
