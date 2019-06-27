# Set the LLVM version that is to be installed.
: ${LLVM_VERSION=7.0}

# The install directory for LLVM binaries
LLVMPREFIX="`pwd`/`uname -m`_taint/llvm-${LLVM_VERSION}/bin"

# Source and object directories
SRC_DIR_LLVM="`pwd`/../llvm-7.0.0.src"
OBJ_DIR_LLVM="`pwd`/../llvm-7.0.0.build/`uname -m`_taint/llvm-objects"

# Binutils tar ball file name
BINUTILS_NAME="binutils-2.27.90"

# Binutils path
BINUTILS_PATH="`pwd`/`uname -m`/binutils"

# Build Type
LLVM_BUILD_TYPE=RelWithDebInfo

# Configure Ninja Build
USE_NINJA=1

# Control to switch ON/OFF tasks in configure script
INSTALL_BINUTILS=0
