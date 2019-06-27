#!/bin/bash

# Note: If you are running this script for the first time here, 
# you probably must first run the configure.sh in order to setup
# your LLVM build environment and then proceed to run this script

: ${NUM_JOBS=16}
: ${SETTINGS_INC_FILE="`pwd`/configure.inc"}
: ${USE_NINJA=0}

if [ ! -f ${SETTINGS_INC_FILE} ]; then
    echo "Settings file not found: ${SETTINGS_INC_FILE}"
    exit 2
fi
. ${SETTINGS_INC_FILE}

set -e

if [ ${USE_NINJA} -eq 0 ]; then
  make -j ${NUM_JOBS} -C ${OBJ_DIR_LLVM}
  make install -C ${OBJ_DIR_LLVM}
else
  cmake --build ${OBJ_DIR_LLVM} --target install 2>&1 | tee build.log
fi
