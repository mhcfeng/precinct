#!/bin/bash

Datafile='../curr-batch'

for COUNTY in $(cat $Datafile); do
  ./workflow.sh hill $COUNTY vr
  ./workflow.sh trump $COUNTY vr
  ./workflow.sh hill $COUNTY adjacency
  ./workflow.sh trump $COUNTY adjacency
done
