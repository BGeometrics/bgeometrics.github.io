#!/bin/bash

# Script for copy code for Alfa Bitcoin

set +x

# Change variables to the corresponding values
HOST=192.168.1.66
DDBB="XXX"
DDBB_USER="YYY"
DIR="$HOME/proyectos/bitcoin-scripts"
DIR_JSON="$HOME/bgeometrics.github.io/files"
DIR_HTML="$HOME/bgeometrics.github.io/alfabitcoin"
DIR_TARGET="$HOME/proyectos/my_package/src/my_package"
DIR_TARGET="/tmp/code"
DIR_SCRIPTS_TARGET="$DIR_TARGET/scripts"
DIR_HTML_TARGET="$DIR_TARGET/html"
DIR_JSON_TARGET="$DIR_TARGET/json"
DIR_DDBB_TARGET="$DIR_TARGET/ddbb"
export PGPASSWORD=ZZZ


echo
echo "#### "$(basename "$0")" ####"
echo "#### Scripts for copy code Alfa Bitcoin ####"
echo $(date)
echo ""


echo "Create directory"
if [ ! -d "$DIR_TARGET" ]; then
  mkdir $DIR_TARGET
else
  rm -rf $DIR_TARGET/*
fi


echo "Copy charts"
if [ ! -d "$DIR_HTML_TARGET" ]; then
  mkdir $DIR_HTML_TARGET
fi

cp -rp $DIR_HTML/* $DIR_HTML_TARGET


echo "Copy scripts for get data"
if [ ! -d "$DIR_SCRIPTS_TARGET" ]; then
  mkdir $DIR_SCRIPTS_TARGET
fi
cd $DIR
cp bitcoin-realized-price-getdata.py $DIR_SCRIPTS_TARGET
cp bitcoin-realized-price-getdata-2.py $DIR_SCRIPTS_TARGET
cp bitcoin-research-sth-realized-price-getdata.py $DIR_SCRIPTS_TARGET
cp bitcoin-address-active-getdata.py $DIR_SCRIPTS_TARGET
cp bitcoin-stablecoin-supply-getdata.py $DIR_SCRIPTS_TARGET
cp bitcoin-supply-in-profit-getdata.py $DIR_SCRIPTS_TARGET
cp bitcoin-chainex-addr-*-getdata.py $DIR_SCRIPTS_TARGET
cp bitcoin-price-distribution.py $DIR_SCRIPTS_TARGET
cp bitcoin-chainex-hodl-waves-relative-getdata.py $DIR_SCRIPTS_TARGET
cp bitcoin-chainex-rhodl_1m-getdata.py $DIR_SCRIPTS_TARGET
cp bitcoin-thermocap-node-getdata.py $DIR_SCRIPTS_TARGET
cp bitcoin-openinterest-getdata.py $DIR_SCRIPTS_TARGET
cp bitcoin-sopr-getdata.py $DIR_SCRIPTS_TARGET
cp bitcoin-research-lth-sopr-getdata.py $DIR_SCRIPTS_TARGET
cp bitcoin-research-sth-sopr-getdata.py $DIR_SCRIPTS_TARGET
cp bitcoin-coc-vdd-getdata.py $DIR_SCRIPTS_TARGET
cp bitcoin-nvt-getdata.py $DIR_SCRIPTS_TARGET
cp bitcoin-tv-miner-getdata.py $DIR_SCRIPTS_TARGET
cp bitcoin-tv-m2-getdata.py $DIR_SCRIPTS_TARGET
cp btc-binance-funding-rate-getdata.py $DIR_SCRIPTS_TARGET


echo "Copy lib and files"
cd $DIR
cp bitcoin_utils.py $DIR_SCRIPTS_TARGET
cp config_alfabitcoin.py $DIR_SCRIPTS_TARGET
cp btc-lib-*tar.gz $DIR_SCRIPTS_TARGET
#pip install btc-lib-*tar.gz


echo "Copy scripts generate files json"
cd "$DIR" 
cp btc-file-realized-price.py $DIR_SCRIPTS_TARGET
cp btc-file-mvrv-zscore.py $DIR_SCRIPTS_TARGET
cp btc-file-sth-realized-price.py $DIR_SCRIPTS_TARGET
cp btc-file-address-active.py $DIR_SCRIPTS_TARGET
cp btc-file-stablecoin-supply.py $DIR_SCRIPTS_TARGET
cp btc-file-supply-in-profit.py $DIR_SCRIPTS_TARGET
cp btc-file-addr-distribution.py $DIR_SCRIPTS_TARGET
cp bitcoin-price-distribution.py $DIR_SCRIPTS_TARGET
cp btc-file-nupl.py $DIR_SCRIPTS_TARGET
cp btc-file-hodl-waves.py $DIR_SCRIPTS_TARGET
cp btc-file-capitalization.py $DIR_SCRIPTS_TARGET
cp btc-file-price.py $DIR_SCRIPTS_TARGET
cp btc-file-capitalization.py $DIR_SCRIPTS_TARGET
cp btc-file-open-interest-futures.py $DIR_SCRIPTS_TARGET
cp btc-file-sopr.py $DIR_SCRIPTS_TARGET
cp btc-file-nvt.py $DIR_SCRIPTS_TARGET
cp btc-file-btc-ohlc-4h.py $DIR_SCRIPTS_TARGET


echo "Copy json files"
if [ ! -d "$DIR_JSON_TARGET" ]; then
  mkdir $DIR_JSON_TARGET
fi
cd $DIR_JSON
cp addresses_active.json $DIR_JSON_TARGET 
cp funding_rate.json $DIR_JSON_TARGET
cp lth_sopr.json $DIR_JSON_TARGET
cp m2_yoy_change.json $DIR_JSON_TARGET
cp m2_weeks7_change.json $DIR_JSON_TARGET 
cp miner_sell_presure.json $DIR_JSON_TARGET 
cp miner_sell_presure_200dma.json $DIR_JSON_TARGET
cp mvrv.json $DIR_JSON_TARGET 
cp nvts_bg.json $DIR_JSON_TARGET
cp nupl.json $DIR_JSON_TARGET 
cp oi_total.json $DIR_JSON_TARGET 
cp profit_loss.json $DIR_JSON_TARGET 
cp realized_price.json $DIR_JSON_TARGET
cp sopr.json $DIR_JSON_TARGET
cp stablecoin_supply.json $DIR_JSON_TARGET
cp sth_realized_price.json $DIR_JSON_TARGET
cp sth_sopr.json $DIR_JSON_TARGET
cp terminal_price.json $DIR_JSON_TARGET
cp vdd_multiple.json $DIR_JSON_TARGET


echo "Export data"
if [ ! -d "$DIR_DDBB_TARGET" ]; then
  mkdir $DIR_DDBB_TARGET
fi

TABLES=("btc_address" "btc_address_distribution" "btc_hodl_waves_relative" "btc_lth_sth" "btc_miner" "btc_nupl" "btc_open_interest" "btc_price_usd" "btc_realized_price" "btc_stablecoin_supply" "btc_supply" "btc_sopr" "btc_sopr" "btc_nvt" "btc_miner" "btc_m2_global" "btc_funding_rate")

# Iterate over array elements
for TABLE in "${TABLES[@]}"
do
    pg_dump -U $DDBB_USER -h $HOST -d $DDBB -t $TABLE -f $DIR_DDBB_TARGET/$TABLE.dump
done

# pg_restore -U [username] -d [database] -t [table_name] [dump_file]

#cp $DIR/$(basename "$0") $DIR_HTML/tools 
