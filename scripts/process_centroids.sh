#!/bin/bash
# Usage ./process_centroids COUNTY
INDIR="../data/extractcentroids/"
NUMPRECINCTS=$(cat $INDIR$1".csv" | wc -l | sed 's/ //g')
tail -"$((NUMPRECINCTS-1))" $INDIR$1".csv" | sed -e :a -e 's/"\([^",]*\),\([^"]*\)"/"\1 \2"/; ta' | sed 's/"//g' | sort -n -t',' -k4 > $INDIR$1"-sorted.csv"
awk 'BEGIN{FS=","} {if ($4<0) print $0}' $INDIR$1"-sorted.csv" > junk.trump
awk 'BEGIN{FS=","} {if ($4>0) print $0}' $INDIR$1"-sorted.csv" | tail -r > junk.hill
cut -d',' -f1 junk.trump | awk '{print NR,$0}' > $INDIR"trump/"$1"-key"
cut -d',' -f1 junk.hill | awk '{print NR,$0}' > $INDIR"hill/"$1"-key"
cat $INDIR"trump/"$1"-key" | sed 's/\([^ ]*\) \([^ ]*\)/s%\2[ ,]%\1,%g/' > sed.script
sed -f sed.script junk.trump > $INDIR"trump/"$1".csv"
rm -f sed.script
cat $INDIR"hill/"$1"-key" | sed 's/\([^ ]*\) \([^ ]*\)/s%\2[ ,]%\1,%g/' > sed.script
sed -f sed.script junk.hill > $INDIR"hill/"$1".csv"
rm -f sed.script, junk.*
