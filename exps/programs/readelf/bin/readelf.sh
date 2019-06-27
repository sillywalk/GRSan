#!/bin/bash

if [ ! $# -eq 3 ]; then
  echo "Usage: readelf.sh <mode> <mark byte index> <input file>  (mode is taint or gradient)";
  exit 1;
fi


SCRIPT=$(readlink -f "$0")

# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

TAINT_EXE="$SCRIPTPATH/readelf_taint"
GRADIENT_EXE="$SCRIPTPATH/readelf_grad"
BUG_EXE="$SCRIPTPATH/readelf_bug"

MODE=$1;
MARK=$2;
INFILE=$3;

if [ "$MODE" = "taint" ]; then
  echo "$TAINT_EXE -a -k $MARK $INFILE";
  eval "$TAINT_EXE -a -k $MARK $INFILE";
elif [ "$MODE" = "gradient" ]; then
  echo "$GRADIENT_EXE -a -k $MARK  $INFILE";
  eval "$GRADIENT_EXE -a -k $MARK $INFILE";
elif [ "$MODE" = "bug" ]; then
  eval "$BUG_EXE -a $INFILE";
else
  echo "invalid mode $MODE, must be taint or gradient";
  exit 1;
fi

