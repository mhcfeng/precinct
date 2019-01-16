#!/bin/bash
#USAGE: ./process_neighbors.sh COUNTY
INDIR="../data/adjacency/"
NUMPRECINCTS=$(cat $INDIR$1".csv" | wc -l | sed 's/ //g')
tail -"$((NUMPRECINCTS-1))" $INDIR$1".csv" | sed -e :a -e 's/"\([^",]*\),\([^"]*\)"/"\1 \2"/; ta' | sed 's/"//g' | sort -n -t',' -k3 > $INDIR$1"-sorted.csv"
awk 'BEGIN{FS=","} {if ($3<0) print $0}' $INDIR$1"-sorted.csv" > junk.trump
awk 'BEGIN{FS=","} {if ($3>0) print $0}' $INDIR$1"-sorted.csv" | tail -r > junk.hill
cut -d',' -f1 junk.trump | awk '{print NR,$0}' > $INDIR"trump/"$1"-key"
cut -d',' -f1 junk.hill | awk '{print NR,$0}' > $INDIR"hill/"$1"-key"
cat $INDIR"trump/"$1"-key" | sed 's/\([^ ]*\) \([^ ]*\)/s%\2\\([ ,]\\)%\1\\1%g/' > sed.script
sed -f sed.script junk.trump | sed -E 's/( ?)[0-9]+-[a-zA-Z0-9_.-]*( ?)/\1\2/g' | sed -E 's/ +/ /g'| sed 's/ ,/,/g' | sed 's/, /,/g'> $INDIR"trump/"$1".csv"
rm -f sed.script
cat $INDIR"hill/"$1"-key" | sed 's/\([^ ]*\) \([^ ]*\)/s%\2\\([ ,]\\)%\1\\1%g/' > sed.script
sed -f sed.script junk.hill | sed -E 's/( ?)[0-9]+-[a-zA-Z0-9_.-]*( ?)/\1\2/g' | sed -E 's/ +/ /g' | sed 's/ ,/,/g' | sed 's/, /,/g'> $INDIR"hill/"$1".csv"
rm -f sed.script, junk.*
