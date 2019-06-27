#!/bin/bash

set -e 

MYPWD=`pwd`

. ../common.inc
. ../make.inc

PATH_BUILD_PREFIX=${MYPWD}/llvm_build
PATH_BUILD_SUFFIX=${GR_BUILD_TYPE}
PATH_BUILD=${PATH_BUILD_PREFIX}/${PATH_BUILD_SUFFIX}
PATH_INSTALL=${PATH_BUILD}/install
BIN_SUFFIX="_${GR_BUILD_TYPE}"

source ../build.sh

## ---------------------
## Package specific settings
## ---------------------
BIN_FILE=bin/objdump


# ---------------------
# Verification
# ---------------------
printf "\nVerfication:\t${BIN_FILE} with dfsan? `verify_dfsan ${PATH_INSTALL}/${BIN_FILE}`\n"

# ---------------------
# Post compilation
# ---------------------
if [ "" != "${BIN_SUFFIX}" ]; then
	for b in objdump readelf strip; do
		if [ -e ${PATH_BIN_DIR_DFSAN_GRAD_COMPARE}/$b/bin/$b${BIN_SUFFIX} ]; then
			rm ${PATH_BIN_DIR_DFSAN_GRAD_COMPARE}/$b/bin/$b${BIN_SUFFIX} || true
		fi
	  cp ${PATH_INSTALL}/bin/$b ${PATH_BIN_DIR_DFSAN_GRAD_COMPARE}/$b/bin/$b${BIN_SUFFIX}
			#ln -s ${PATH_INSTALL}/bin/$b ${PATH_BIN_DIR_DFSAN_GRAD_COMPARE}/$b/bin/$b${BIN_SUFFIX}
	done
fi

cd ${MYPWD}
