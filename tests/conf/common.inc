# -------------------------------------------
# Local environment specific variables
# -------------------------------------------
PATH_TESTS_ROOT=/local/ksbhat/repo/gradtest/tests
LLVM_BUILD_DIR=/local/ksbhat/repo/rebuild/gradtest/llvm-7.0.0.build
LLVM_BINPATH_PLAIN=${LLVM_BUILD_DIR}/x86_64_taint/llvm-7.0/bin/bin
LLVM_BINPATH_GRSAN=${LLVM_BUILD_DIR}/x86_64/llvm-7.0/bin/bin

# --------------------------------------------
# Variables that mostly do not require changes
# --------------------------------------------
LLVM_CC=${LLVM_BINPATH_PLAIN}/clang
LLVM_CXX=${LLVM_BINPATH_PLAIN}/clang++
LLVM_CC_GRSAN=${LLVM_BINPATH_GRSAN}/clang
LLVM_CXX_GRSAN=${LLVM_BINPATH_GRSAN}/clang++
LLVM_CFLAGS="-O0 -g"
LLVM_CXXFLAGS="-O0 -g"
LLVM_LDFLAGS="-L${LLVM_BINPATH_PLAIN}/../lib -L${LLVM_BINPATH_PLAIN}/../clang/7.0.0/lib/linux/"
LLVM_LDFLAGS_GRSAN="-L${LLVM_BINPATH_GRSAN}/../lib -L${LLVM_BINPATH_GRSAN}/../clang/7.0.0/lib/linux/"
