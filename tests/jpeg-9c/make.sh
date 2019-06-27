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


source  ../build.sh



BIN_FILE=bin/djpeg
# ---------------------
# Verification
# ---------------------
printf "\nVerfication:\t${BIN_FILE} with dfsan? `verify_dfsan ${PATH_INSTALL}/${BIN_FILE}`\n"

# ---------------------
# Post compilation
# ---------------------
if [ "" != "${BIN_SUFFIX}" ]; then
    echo "cp ${PATH_INSTALL}/${BIN_FILE} ${PATH_BIN_DIR_DFSAN_GRAD_COMPARE}/jpeg/bin/djpeg${BIN_SUFFIX}"
    cp ${PATH_INSTALL}/${BIN_FILE} ${PATH_BIN_DIR_DFSAN_GRAD_COMPARE}/jpeg/bin/djpeg${BIN_SUFFIX}
fi


cd ${MYPWD}
