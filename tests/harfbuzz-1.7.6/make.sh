#!/bin/bash

# harfbuzz

# TODO: Doesn't completely work yet. Needs to work on compiling its dependent libraries
# As of 17th Dec 2018. 
# --Koustubha

set -e 

MYPWD=`pwd`

. ../common.inc
. ../make.inc

: ${GR_BUILD_TYPE=dfsan}

PATH_BUILD_PREFIX=${MYPWD}/llvm_build
PATH_BUILD_SUFFIX=plain
FLAGS_DFSAN="-fsanitize=dataflow"
LLVM_CXXFLAGS="${LLVM_CXXFLAGS} -Wcast-align -fvisibility-inlines-hidden --std=c++0x -Bsymbolic-functions"

if [ "${GR_BUILD_TYPE}" == "dfsan" ]; then
    PATH_BUILD_SUFFIX=dfsan
    LLVM_CFLAGS="${LLVM_CFLAGS} ${FLAGS_DFSAN}"
    LLVM_CXXFLAGS="${LLVM_CXXFLAGS} ${FLAGS_DFSAN}"
    FLAGS_L_INC="-L${PATH_GLIB}/${PATH_BUILD_SUFFIX} -L${PATH_FREETYPE}/${PATH_BUILD_SUFFIX}"
    LLVM_LDFLAGS="${LLVM_LDFLAGS} ${FLAGS_DFSAN} ${FLAGS_L_INC}"

elif [ "${GR_BUILD_TYPE}" == "grsan" ]; then
    PATH_BUILD_SUFFIX=grsan
    LLVM_CC=${LLVM_CC_GRSAN}
    LLVM_CXX=${LLVM_CXX_GRSAN}
    LLVM_CFLAGS="${LLVM_CFLAGS} ${FLAGS_DFSAN} -DGRSAN"
    LLVM_CXXFLAGS="${LLVM_CXXFLAGS} ${FLAGS_DFSAN} -DGRSAN"
    FLAGS_L_INC="-L${PATH_GLIB}/${PATH_BUILD_SUFFIX} -L${PATH_FREETYPE}/${PATH_BUILD_SUFFIX}"
    LLVM_LDFLAGS="${LLVM_LDFLAGS_GRSAN} ${FLAGS_DFSAN} ${FLAGS_L_INC}"

else
    FLAGS_L_INC="-L${PATH_GLIB}/${PATH_BUILD_SUFFIX} -L${PATH_FREETYPE}/${PATH_BUILD_SUFFIX}"
    LLVM_LDFLAGS="${LLVM_LDFLAGS} ${FLAGS_L_INC}"

fi

PATH_BUILD=${PATH_BUILD_PREFIX}/${PATH_BUILD_SUFFIX}
PATH_INSTALL=${PATH_BUILD}/install

# ---------------------
# Package specific settings
# ---------------------
BIN_FILE=lib/libharfbuzz.so


[ -e ${PATH_BUILD} ] && [ -d ${PATH_BUILD} ] || mkdir -p ${PATH_BUILD}
cd ${PATH_BUILD}

# ---------------------
# Dependency checks
# ---------------------
if [ -e "${PATH_GLIB}/${PATH_BUILD_SUFFIX}/install/lib/libglib-2.0.so" ]; then
  echo "First build ${PATH_BUILD_SUFFIX} version of glib2 (ubuntu pkg version 2.48.2)" && exit 1;
fi
if [ -e "${PATH_FREETYPE}/${PATH_BUILD_SUFFIX}/install/lib/libfreetype.so" ]; then
  echo "First build ${PATH_BUILD_SUFFIX} version of freetype-2.6.4" && exit 1;
fi
if [ -e "${PATH_FFI}/${PATH_BUILD_SUFFIX}/install/lib/libffi.so" ]; then
  echo "First build ${PATH_BUILD_SUFFIX} version of libffi" && exit 1;
  # TODO: Tried with version 3.2.1. Needs recheck
fi
if [ -e "${PATH_ELF}/${PATH_BUILD_SUFFIX}/install/lib/libelf.so" ]; then
  echo "First build ${PATH_BUILD_SUFFIX} version of libelf" && exit 1;
  # TODO: Not sure which version fits here yet.
fi


# ---------------------
# Configure 
# ---------------------
  ../../src/configure CC=${LLVM_CC}				\
	CFLAGS="${LLVM_CFLAGS}" CXXFLAGS="${LLVM_CXXFLAGS}"	\
	LDFLAGS="${LLVM_LDFLAGS}"	\
	--prefix="${PATH_INSTALL}"


# ---------------------
# Run make and install
# ---------------------
make
make install || true


# ---------------------
# Verification
# ---------------------
printf "\nVerfication:\t${BIN_FILE} with dfsan? `verify_dfsan ${PATH_INSTALL}/${BIN_FILE}`\n"

cd ${MYPWD}
