#!/bin/bash
set -e

MYPWD=`pwd`

. ../common.inc
. ../make.inc

export PATH_BUILD_PREFIX=${MYPWD}/llvm_build
export PATH_BUILD_SUFFIX=${GR_BUILD_TYPE}
export PATH_BUILD=${PATH_BUILD_PREFIX}/${PATH_BUILD_SUFFIX}
export PATH_INSTALL=${PATH_BUILD}/install
export BIN_SUFFIX="_${GR_BUILD_TYPE}"

export LD_PRELOAD="/usr//lib/x86_64-linux-gnu/libz.so"
source  ../build.sh


# ---------------------
# Package specific settings
# ---------------------
#BIN_FILE=lib/libz.so.1.2.11
BIN_FILE="minigzip64"

# ---------------------
# Verification
# ---------------------
printf "\nVerfication:\t${BIN_FILE} with dfsan? `verify_dfsan ${PATH_BUILD}/${BIN_FILE}`\n"

cd ${MYPWD}

# ---------------------
# Post compilation
# ---------------------
if [ "" != "${BIN_SUFFIX}" ]; then
    cp ${PATH_BUILD}/${BIN_FILE} ${PATH_BIN_DIR_DFSAN_GRAD_COMPARE}/zlib/bin/minigzip${BIN_SUFFIX}
fi
