#!/bin/bash

rm run.log data.csv
rm input.txt input.txt.gz
cp input.txt.gz.bak input.txt.gz
../build/minigzip -d -m 75  -o data.csv  input.txt.gz 2>&1 | tee run.log;
#../build/minigzip -d -m 75 -change 75 6 -change 11 0 -o data.csv  input.txt.gz 2>&1 | tee run.log;
#../build/minigzip -d -m 11 -change 3 12 -change 11 255  -o data.csv  input.txt.gz 2>&1 | tee run.log;

