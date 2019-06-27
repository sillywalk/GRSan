#!/bin/bash

# Libxml

set -e 

MYPWD=`pwd`

. ../common.inc
. ../make.inc

PATH_BUILD_PREFIX=${MYPWD}/llvm_build
PATH_BUILD_SUFFIX=${GR_BUILD_TYPE}

PATH_BUILD=${PATH_BUILD_PREFIX}/${PATH_BUILD_SUFFIX}
PATH_INSTALL=${PATH_BUILD}/install

LLVM_CFLAGS="-Wl,-R${PATH_ZLIB}/${PATH_BUILD_SUFFIX} $LLVM_CFLAGS"

BIN_SUFFIX="_${GR_BUILD_TYPE}"


source ../build.sh



BIN_FILE=bin/xmllint

# ---------------------
# Post compilation
# ---------------------
if [ "" != "${BIN_SUFFIX}" ]; then
    cp ${PATH_INSTALL}/${BIN_FILE} ${PATH_BIN_DIR_DFSAN_GRAD_COMPARE}/libxml/bin/xmllint${BIN_SUFFIX}
fi

# ---------------------
# Verification
# ---------------------
printf "\nVerfication:\t${BIN_FILE} with dfsan? `verify_dfsan ${PATH_INSTALL}/${BIN_FILE}`\n"

cd ${MYPWD}
