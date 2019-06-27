#!/bin/bash

rm run.log data.csv
for i in {0..91}
do
  rm input.txt input.txt.gz
  cp input.txt.gz.bak input.txt.gz
  echo $i;
  ../build/minigzip -d -m $i -o data.csv  input.txt.gz 2>&1 | tee run.log;
done

