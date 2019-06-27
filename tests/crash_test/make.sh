#!/bin/bash

# Libxml

set -e 

MYPWD=`pwd`

. ../common.inc
. ../make.inc

: ${GR_BUILD_TYPE=dfsan}
: ${ENABLE_GRAD=0}

PATH_BUILD_PREFIX=${MYPWD}/llvm_build
PATH_BUILD_SUFFIX=plain
FLAGS_DFSAN="-fsanitize=dataflow"
FLAGS_L_INC="-L${PATH_ZLIB}/${PATH_BUILD_SUFFIX}"
BIN_SUFFIX=

if [ "${GR_BUILD_TYPE}" == "dfsan" ]; then
    PATH_BUILD_SUFFIX=dfsan
    LLVM_CFLAGS="${LLVM_CFLAGS} ${FLAGS_DFSAN} -DDFSAN -DGRTRACK"
    LLVM_CXXFLAGS="${LLVM_CXXFLAGS} ${FLAGS_DFSAN} -DDFSAN -DGRTRACK"
    FLAGS_L_INC="-L${PATH_ZLIB}/${PATH_BUILD_SUFFIX}"
    LLVM_LDFLAGS="${LLVM_LDFLAGS} ${FLAGS_DFSAN} ${FLAGS_L_INC}"
    BIN_SUFFIX="_taint"

elif [ "${GR_BUILD_TYPE}" == "grsan" ]; then
    PATH_BUILD_SUFFIX=grsan
    LLVM_CC=${LLVM_CC_GRSAN}
    LLVM_CXX=${LLVM_CXX_GRSAN}
    LLVM_CFLAGS="${LLVM_CFLAGS} ${FLAGS_DFSAN} -fPIC -DGRSAN -DGRTRACK"
    LLVM_CXXFLAGS="${LLVM_CXXFLAGS} ${FLAGS_DFSAN} -fPIC -DGRSAN -DGRTRACK"
    FLAGS_L_INC="-L${PATH_ZLIB}/${PATH_BUILD_SUFFIX}"
    LLVM_LDFLAGS="${LLVM_LDFLAGS_GRSAN} ${FLAGS_DFSAN} ${FLAGS_L_INC}"
    BIN_SUFFIX="_grad"

elif [ "${GR_BUILD_TYPE}" == "fuzz" ]; then
    PATH_BUILD_SUFFIX=fuzz
    LLVM_CC=afl-clang
    LLVM_CXX=afl-clang++
    BIN_SUFFIX="_fuzz"

elif [ "${GR_BUILD_TYPE}" == "fast" ]; then
    PATH_BUILD_SUFFIX=fast
    LLVM_CC=clang
    LLVM_CXX=clang++
    LLVM_CFLAGS="-O3 -g"
    LLVM_CXXFLAGS="-O3 -g"
    BIN_SUFFIX="_fast"

elif [ "${GR_BUILD_TYPE}" == "bug" ]; then
    PATH_BUILD_SUFFIX=bug
    LLVM_CC=clang
    LLVM_CXX=clang++
    #LLVM_CFLAGS="-O2 -g -fsanitize=address,undefined -fno-omit-frame-pointer"
    LLVM_CFLAGS="-O0 -g -fsanitize=address -fno-omit-frame-pointer"
    #LLVM_CXXFLAGS="-O2 -g -fsanitize=address,undefined -fno-omit-frame-pointer"
    #LLVM_CXXFLAGS="-O2 -g -fsanitize=address -fno-omit-frame-pointer"
    LLVM_LDFLAGS="-fsanitize=address"
    #LLVM_LDFLAGS="${LLVM_LDFLAGS} -fsanitize=address,undefined  ${FLAGS_L_INC}"
    BIN_SUFFIX="_bug"
else
    LLVM_LDFLAGS="${LLVM_LDFLAGS} ${FLAGS_L_INC}"

fi

PATH_BUILD=${PATH_BUILD_PREFIX}/${PATH_BUILD_SUFFIX}
PATH_INSTALL=${PATH_BUILD}/install

# ---------------------
# Package specific settings
# ---------------------
BIN_FILE=crash_test


[ -e ${PATH_BUILD} ] && [ -d ${PATH_BUILD} ] || mkdir -p ${PATH_BUILD}
cd ${PATH_BUILD}


# ---------------------
# Configure 
# ---------------------
  cmake -DCMAKE_C_COMPILER=${LLVM_CC} 		\
        -DCMAKE_INSTALL_PREFIX="${PATH_INSTALL}"	\
        -DCMAKE_C_FLAGS="${LLVM_CFLAGS}" \
        -DCMAKE_EXE_LINKER_FLAGS="${LLVM_LDFLAGS}" ../../src



# ---------------------
# Run make and install
# ---------------------
make -j8
make install || true



# ---------------------
# Verification
# ---------------------
printf "\nVerfication:\t${BIN_FILE} with dfsan? `verify_dfsan ${PATH_BUILD}/${BIN_FILE}`\n"

# ---------------------
# Post compilation
# ---------------------
if [ "" != "${BIN_SUFFIX}" ]; then
    cp ${PATH_BUILD}/${BIN_FILE} ${PATH_BIN_DIR_DFSAN_GRAD_COMPARE}/crash_test/bin/crash_test${BIN_SUFFIX}
fi
cd ${MYPWD}
