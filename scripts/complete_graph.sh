#!/bin/bash

INFILE="../data/simplicialcomplex/hill/107-tulare-test.dat"

VERTICES=$(awk '{print NR,$0}' $INFILE | grep -e ' 0$' | cut -d' ' -f1)

for VERTEX in $VERTICES
do
  for VERTEX2 in $VERTICES
  do
    if [ $VERTEX -lt $VERTEX2 ]
    then
      echo 1 $VERTEX $VERTEX2 >> junk.edges
    fi
  done
done

sort junk.edges > junk.edgessort
sort $INFILE > junk.sc
comm -23 junk.edgessort junk.sc > junk.newedge
cat $INFILE junk.newedge > simplextemp
rm -f junk.*

EDGES=$(awk '{print NR,$0}' simplextemp | grep -e '^[0-9]* 1 ' |cut -d' ' -f1)
for EDGE in $EDGES
do
  for EDGE2 in $EDGES
  do
    for EDGE3 in $EDGES
    do
      if [ $EDGE -lt $EDGE2 ] && [ $EDGE2 -lt $EDGE3 ]
      then
        echo 2 $EDGE $EDGE2 $EDGE3 >> junk.triangles
      fi
    done
  done
done

echo "sorting"
sort junk.triangles > junk.trianglesort
sort simplextemp > junk.sc
echo "comparing"
comm -23 junk.trianglesort junk.sc > junk.newtriangle
echo "here"
cat simplextemp junk.newtriangle > test
rm -f junk.* simplextemp
