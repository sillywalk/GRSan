
# Working with build scripts for target applications
Every application folder follows the following structure:

```
    src		- contains the package contents

    Makefile    - offers options:
		  make plain : builds the app in llvm_build/plain without DFSAN
                  make dfsan : builds the app in llvm_build/dfsan with DFSAN (using normal LLVM build)
                  make grsan : builds the app in llvm_build/grsan with DFSAN (using modified LLVM build)
                               also defines macro GRSAN

    make.sh     - has package specific build settings modifications. Also follows a standard structure within.
```

## Preparation
Copy the `tests/conf/common.inc` over to the `tests` directory and modify the variables according to your local environment.

## Building the applications

To build, run either of the following as required
```
$ make plain
$ make dfsan
$ make grsan
```
To build all:
```
$ make all
```

# Editing application source code
We can surround our changes with `#ifdef GRSAN` while make DFSAN specific flow tracking changes
to the target application source code.

# Earlier notes

## libxml
    @abhi
    - `./configure; make`
    - `make distclean` to clean everyting
    - make check inside /example; then ./gjobs gjobs.xml or something similar
    - `./configure CC=clang CFLAGS=-fsanitize=dataflow LDFLAGS=-fsanitize=dataflow`

## jpeg-9c
```
./configure CC=clang CFLAGS="-fsanitize=dataflow -fPIC"
make
cat rdjpgcom.c # this is where the label is marked
```


# Notes on command line options
`-m <byte>` - denotes which byte to mark as the independent variable
`-change <byte> <delta>` - change <byte> by <delta>
`-o <filename>` - create a datafile named <filename>
To test if command line works, try using the above options and inserting the below statement afterwards
```
fprintf(stderr, "%zd is mark_ind; n_changes is %zd\n", mark_ind, n_changes);
```
