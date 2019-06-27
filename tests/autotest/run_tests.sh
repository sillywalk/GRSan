#!/bin/bash

PASS=1;
SUMMARY="\nSUMMARY:";

echo "start tests" > test.log;

#if  "$PASS" -ne "0" && make clean &>>test.log; then
printf "Running make clean\n" | tee -a test.log
make clean &>>test.log;
if [ $? -ne 0 ];  then
  echo "\nmake clean failed $?\n" | tee -a test.log;
  SUMMARY="$SUMMARY\nmake clean FAIL";
  PASS=0;
else
  SUMMARY="$SUMMARY\nmake clean PASS";
fi

printf "Running make\n" | tee -a test.log
make &>>test.log;
if [  $? -ne 0 ];  then
  printf "\nmake failed with status $?\n" | tee -a test.log;
  SUMMARY="$SUMMARY\nmake FAIL";
  PASS=0;
else
  SUMMARY="$SUMMARY\nmake PASS";
fi

for f in test*.exe; do
  printf "Running $f\n" | tee -a test.log
  if [ $f == "test_sampling.exe" ]; then
    DFSAN_OPTIONS="and_nsamples=4" ./$f &>>test.log;
  else
    ./$f &>>test.log;
  fi
  #printf "$f status: $?" | tee -a test.log
  if [ $? -ne 0 ]; then
    SUMMARY="$SUMMARY\n$f FAIL";
    PASS=0;
  else
    SUMMARY="$SUMMARY\n$f PASS";
  fi
done

printf "$SUMMARY\n" | tee -a test.log

if [ $PASS -eq 1 ]; then
  printf "\nALL TESTS PASS\n" | tee -a test.log;
else
  printf "\nTEST FAILURE\n" | tee -a test.log;
fi


