#!/bin/bash

# mupdf

set -e 

MYPWD=`pwd`

. ../common.inc
. ../make.inc

: ${GR_BUILD_TYPE=dfsan}

PATH_BUILD_PREFIX=${MYPWD}/llvm_build
PATH_BUILD_SUFFIX=plain
FLAGS_DFSAN="-fsanitize=dataflow"
BIN_SUFFIX=

if [ "${GR_BUILD_TYPE}" == "dfsan" ]; then
    PATH_BUILD_SUFFIX=dfsan
    LLVM_BINPATH=${LLVM_BINPATH_PLAIN}
    LLVM_CC=${LLVM_BINPATH_PLAIN}/clang
    LLVM_CXX=${LLVM_BINPATH_PLAIN}/clang++
    LLVM_CFLAGS="${LLVM_CFLAGS} ${FLAGS_DFSAN} -DGRTRACK"
    LLVM_CXXFLAGS="${LLVM_CXXFLAGS} ${FLAGS_DFSAN} -DGRTRACK"
    LLVM_LDFLAGS="${LLVM_LDFLAGS} ${FLAGS_DFSAN} ${FLAGS_L_INC}"
    BIN_SUFFIX="_taint"

elif [ "${GR_BUILD_TYPE}" == "fuzz" ]; then
    PATH_BUILD_SUFFIX=fuzz
    LLVM_CC=afl-gcc
    LLVM_CXX=afl-g++
    BIN_SUFFIX="_fuzz"
    #FLAGS_L_INC="-L${PATH_ZLIB}/${PATH_BUILD_SUFFIX}"
#    LLVM_LDFLAGS="${LLVM_LDFLAGS} ${FLAGS_L_INC}"

elif [ "${GR_BUILD_TYPE}" == "grsan" ]; then
    PATH_BUILD_SUFFIX=grsan
    LLVM_BINPATH=${LLVM_BINPATH_GRSAN}
    LLVM_CC=${LLVM_BINPATH_GRSAN}/clang
    LLVM_CXX=${LLVM_BINPATH_GRSAN}/clang++
    LLVM_CFLAGS="${LLVM_CFLAGS} ${FLAGS_DFSAN} -DGRSAN -DGRTRACK"
    LLVM_CXXFLAGS="${LLVM_CXXFLAGS} ${FLAGS_DFSAN} -DGRSAN -DGRTRACK"
    #FLAGS_L_INC="-L${PATH_ZLIB}/${PATH_BUILD_SUFFIX}"
    LLVM_LDFLAGS="${LLVM_LDFLAGS_GRSAN} ${FLAGS_DFSAN} ${FLAGS_L_INC}"
    BIN_SUFFIX="_grad"


elif [ "${GR_BUILD_TYPE}" == "base" ]; then
    LLVM_BINPATH=${LLVM_BINPATH_PLAIN}

    LLVM_CC="${LLVM_BINPATH}/clang"
    LLVM_CXX="${LLVM_BINPATH}/clang++"
    LLVM_CFLAGS="-O0 -g"
    LLVM_CXXFLAGS="-O0 -g"
    LLVM_LDFLAGS="-flto -Wl ${FLAGS_L_INC}"

    BIN_SUFFIX="_base"


elif [ "${GR_BUILD_TYPE}" == "fuzz" ]; then
    LLVM_BINPATH=$LLVM_BINPATH_PLAIN
    PATH_BUILD_SUFFIX=fuzz
    LLVM_CC=${LLVM_CC_FUZZ}
    LLVM_CXX=${LLVM_CXX_FUZZ}
    LLVM_CFLAGS="${LLVM_CFLAGS} -Wl,-R${PATH_BUILD_SUFFIX}"
    BIN_SUFFIX="_fuzz"



elif [ "${GR_BUILD_TYPE}" == "fast" ]; then
    LLVM_BINPATH=$LLVM_BINPATH_PLAIN
    PATH_BUILD_SUFFIX=fast
    LLVM_CC=clang
    LLVM_CXX=clang++
    LLVM_CFLAGS="-O3 -g"
    LLVM_CXXFLAGS="-O3 -g"
    BIN_SUFFIX="_fast"

elif [ "${GR_BUILD_TYPE}" == "bug" ]; then
    LLVM_BINPATH=$LLVM_BINPATH_PLAIN
    PATH_BUILD_SUFFIX=bug
    LLVM_CC=${LLVM_BINPATH_PLAIN}/clang
    LLVM_CXX=${LLVM_BINPATH_PLAIN}/clang++
    LLVM_CFLAGS="-O2 -g -fsanitize=address,undefined -fno-omit-frame-pointer"
    LLVM_CXXFLAGS="-O2 -g -fsanitize=address,undefined -fno-omit-frame-pointer"
    LLVM_LDFLAGS="-fsanitize=address,undefined"
    #LLVM_LDFLAGS="${LLVM_LDFLAGS} -fsanitize=address,undefined  ${FLAGS_L_INC}"
    BIN_SUFFIX="_bug"

fi

PATH_BUILD=${PATH_BUILD_PREFIX}/${PATH_BUILD_SUFFIX}
PATH_INSTALL=${PATH_BUILD}/install

# ---------------------
# Package specific settings
# ---------------------
#BIN_FILE=libmupdf.a
BIN_FILE=mutool


[ -e ${PATH_BUILD} ] && [ -d ${PATH_BUILD} ] || mkdir -p ${PATH_BUILD}
cd ${PATH_BUILD}


# ---------------------
# Configure 
# ---------------------
export XCFLAGS="${LLVM_CFLAGS}"
export XTHIRD_FLAGS="${LLVM_CFLAGS}"
export XLDFLAGS="${LLVM_LDFLAGS}"
#export CFLAGS="${LLVM_CFLAGS}"
export CC=${LLVM_CC}
export CXX=${LLVM_CXX}
#export AR=${LLVM_AR}
export AR="${LLVM_BINPATH}/llvm-ar"
export NM="${LLVM_BINPATH}/llvm-nm"
export OBJDUMP="${LLVM_BINPATH}/llvm-objdump"
export RANLIB="${LLVM_BINPATH}/llvm-ranlib"
export LDFLAGS="${LLVM_LDFLAGS}"
export OUT=${PATH_INSTALL}
export build=debug


# ---------------------
# Run make and install
# ---------------------
echo "$XCFLAGS"
make -j 16 HAVE_X11=no HAVE_GLUT=no -C ../../src
#V=1 make -n  HAVE_X11=no HAVE_GLUT=no -C ../../src
#make -n HAVE_X11=no HAVE_GLUT=no -C ../../src

# ---------------------
# Verification
# ---------------------
printf "\nVerfication:\t${BIN_FILE} with dfs\$.* symbols? `verify_dfsan ${PATH_INSTALL}/${BIN_FILE}`\n"

if [ "" != "${BIN_SUFFIX}" ]; then
		if [ -e ${PATH_BIN_DIR_DFSAN_GRAD_COMPARE}/mupdf/bin/${BIN_FILE}${BIN_SUFFIX} ]; then
			rm ${PATH_BIN_DIR_DFSAN_GRAD_COMPARE}/mupdf/bin/${BIN_FILE}${BIN_SUFFIX} || true
		fi
    printf "\nLinking ${PATH_INSTALL}/${BIN_FILE} to ${PATH_BIN_DIR_DFSAN_GRAD_COMPARE}/mupdf/bin/${BIN_FILE}${BIN_SUFFIX}\n"
	  cp ${PATH_INSTALL}/${BIN_FILE} ${PATH_BIN_DIR_DFSAN_GRAD_COMPARE}/mupdf/bin/${BIN_FILE}${BIN_SUFFIX}
		#ln -s ${PATH_INSTALL}/${BIN_FILE} ${PATH_BIN_DIR_DFSAN_GRAD_COMPARE}/mupdf/bin/${BIN_FILE}${BIN_SUFFIX}
fi



cd ${MYPWD}
