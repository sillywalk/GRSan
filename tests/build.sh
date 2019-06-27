#!/bin/bash
set -e


FLAGS_DFSAN="-fsanitize=dataflow"
FLAGS_L_INC="-L${PATH_ZLIB}/${PATH_BUILD_SUFFIX}"
LLVM_BINPATH="/usr/local/bin"

if [ "${GR_BUILD_TYPE}" == "dfsan" ]; then
    LLVM_BINPATH=$LLVM_BINPATH_PLAIN

    LLVM_CC="${LLVM_BINPATH}/clang"
    LLVM_CFLAGS="${LLVM_CFLAGS} ${FLAGS_DFSAN} -DDFSAN -DGRTRACK"
    LLVM_CXXFLAGS="${FLAGS_DFSAN} -DDFSAN -DGRTRACK"
    LLVM_LDFLAGS="${LLVM_LDFLAGS} ${FLAGS_DFSAN} ${FLAGS_L_INC}"
    BIN_SUFFIX="_taint"


elif [ "${GR_BUILD_TYPE}" == "grsan" ]; then
    LLVM_BINPATH=$LLVM_BINPATH_GRSAN

    LLVM_CC="${LLVM_BINPATH}/clang"
    LLVM_CFLAGS="${LLVM_CFLAGS} ${FLAGS_DFSAN} -DGRSAN -DGRTRACK "
    LLVM_CXXFLAGS="${LLVM_CXXFLAGS} ${FLAGS_DFSAN} -DGRSAN -DGRTRACK  "

    #LLVM_LDFLAGS="${LLVM_LDFLAGS_GRSAN} ${FLAGS_DFSAN} -flto -Wl ${FLAGS_L_INC}"
    LLVM_LDFLAGS="${LLVM_LDFLAGS_GRSAN} ${FLAGS_DFSAN} -flto -Wl ${FLAGS_L_INC}"
    BIN_SUFFIX="_grad"

elif [ "${GR_BUILD_TYPE}" == "manual" ]; then
    LLVM_BINPATH=$LLVM_BINPATH_GRSAN

    LLVM_CC="${LLVM_BINPATH}/clang"
    LLVM_CFLAGS="${LLVM_CFLAGS} ${FLAGS_DFSAN} -DGRSAN -DGRTRACK -DMANUAL"
    LLVM_CXXFLAGS="${LLVM_CXXFLAGS} ${FLAGS_DFSAN} -DGRSAN -DGRTRACK -DMANUAL"

    LLVM_LDFLAGS="${LLVM_LDFLAGS_GRSAN} ${FLAGS_DFSAN} ${FLAGS_L_INC}"


elif [ "${GR_BUILD_TYPE}" == "fuzz" ]; then
    PATH_BUILD_SUFFIX=fuzz
    LLVM_CC=afl-gcc
    BIN_SUFFIX="_fuzz"

elif [ "${GR_BUILD_TYPE}" == "fast" ]; then
    LLVM_BINPATH=$LLVM_BINPATH_PLAIN

    LLVM_CC="${LLVM_BINPATH}/clang"
    LLVM_CFLAGS="-O2 -g"
    LLVM_CXXFLAGS="-O2 -g"
    LLVM_LDFLAGS="-flto -Wl ${FLAGS_L_INC}"

elif [ "${GR_BUILD_TYPE}" == "base" ]; then
    LLVM_BINPATH=$LLVM_BINPATH_PLAIN

    LLVM_CC="${LLVM_BINPATH}/clang"
    LLVM_CFLAGS="-O0 -g"
    LLVM_CXXFLAGS="-O0 -g"
    LLVM_LDFLAGS="-flto -Wl ${FLAGS_L_INC}"



elif [ "${GR_BUILD_TYPE}" == "bug" ]; then
    LLVM_CC="${LLVM_BINPATH}/clang"
    LLVM_CFLAGS="-O0 -g -fsanitize=address,undefined -fno-omit-frame-pointer"
    LLVM_CXXFLAGS="-O0 -g -fsanitize=address,undefined -fno-omit-frame-pointer"
    LLVM_LDFLAGS="${LLVM_LDFLAGS} -fsanitize=address,undefined  ${FLAGS_L_INC}"

else
    LLVM_LDFLAGS="${LLVM_LDFLAGS} ${FLAGS_L_INC}"

fi

PATH_BUILD=${PATH_BUILD_PREFIX}/${PATH_BUILD_SUFFIX}
PATH_INSTALL=${PATH_BUILD}/install


# ---------------------
# Package specific settings
# ---------------------
#BIN_FILE=lib/libz.so.1.2.11
#BIN_FILE="minigzip64"


[ -e ${PATH_BUILD} ] && [ -d ${PATH_BUILD} ] || mkdir -p ${PATH_BUILD}
cd ${PATH_BUILD}




# ---------------------
# Configure
# ---------------------
[ -e "Makefile" ] || \
  CC="${LLVM_CC}" \
  CXX="${LLVM_CXX}" \
  NM="${LLVM_BINPATH}/llvm-nm" \
  AR="${LLVM_BINPATH}/llvm-ar" \
  OBJDUMP="${LLVM_BINPATH}/llvm-objdump" \
  RANLIB="${LLVM_BINPATH}/llvm-ranlib" \
  CFLAGS="${LLVM_CFLAGS}" \
  LDFLAGS="${LLVM_LDFLAGS}" \
  ../../src/configure --prefix="${PATH_INSTALL}"

# ---------------------
# Run make and install
# ---------------------
if [[ ! -z "${BRANCH_MAP}" ]]; then
  make 2>build.log
  make install || true
else
    make -j16
     make install || true
fi

if [[ ! -z "${BRANCH_MAP}" ]] && type branch_map >/dev/null 2>&1; then
  echo "generating branch map...";
  branch_map build.log;
  MAPPATH=`readlink -f branch_map.csv`;
  echo "generated branch map: $MAPPATH"
fi

