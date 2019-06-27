PATH_ZLIB=${PATH_TESTS_ROOT}/zlib-1.2.11/llvm_build
PATH_LIBXML=${PATH_TESTS_ROOT}/libxml2-2.9.7
PATH_GLIB=${PATH_TESTS_ROOT}/harfbuzz-1.7.6/deps/glib-2.48.2/obj/install/lib
PATH_FREETYPE=${PATH_TESTS_ROOT}/harfbuzz-1.7.6/deps/freetype-2.6.4/build/install/lib
PATH_FFI=${PATH_TESTS_ROOT}/harfbuzz-1.7.6/deps/libffi-3.2.1/build/install/lib
PATH_LIBELF=${PATH_TESTS_ROOT}/libelf-0.8.13/build

PATH_BIN_DIR_DFSAN_GRAD_COMPARE=${PATH_TESTS_ROOT}/../exps/programs/

verify_dfsan()
{
    target=$1

    LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libz.so" nm ${target} | grep "dfs\\$" > /dev/null
    if [ $? -eq 0 ]; then
        echo yes
    else
        echo no
    fi
}
