#!/bin/bash

Datafile='../full-list'
runtimefile='../runtimes/ls_phat_times'
for COUNTY in $(cat $Datafile); do
  echo $COUNTY >> $runtimefile
  echo "hillary" >> $runtimefile
  { time ./../phat/simple_example $COUNTY hillary rips ; } 2>> $runtimefile
done

for COUNTY in $(cat $Datafile); do
  echo $COUNTY >> $runtimefile
  echo "trump" >> $runtimefile
  { time ./../phat/simple_example $COUNTY trump rips ; } 2>> $runtimefile
done

