# Gradtest

## Dependencies
On ubuntu 18.04: `sudo apt install make cmake build-essential bison ninja-build`

## Building LLVM grad and taint versions
1. run `make setupgrad`
2. run `make setuptaint` to build version with taint
3. run `make cleantaint` to reset source to grad version
4. run `make grad` or `make taint` to rebuild when making changes.


## Test Programs
1. To build test programs, cd to `tests` dir and copy `tests/conf/common.inc` to `tests` dir. Modify `PATH_TESTS_ROOT` and `LLVM_BUILD_DIR` to your tests and build dirs in the `common.inc` file in your `tests` dir. 
2. run `make` in the tests dir to build dfsan, grsan, and uninstrumented versions of all test programs. You can also build individual programs from their directories.

## Testing
1. Tests are located in `tests/autotest`
2. Run `make test` to run all tests, or `make` to just build them.
3. Any file starting with `test_` will be run as a test, and will show up as an error if it fails an assertion or otherwise returns nonzero. 
