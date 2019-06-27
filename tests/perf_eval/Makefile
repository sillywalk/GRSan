ROOT=../

#BIN_DIR_LLVM=../../llvm-7.0.0.build/`uname -m`/llvm-7.0/bin/bin

include ${ROOT}common.inc

CFLAGS=-O0 -g3
CXXFLAGS=-O0 -g3
SANITIZER_FLAGS=-fsanitize=dataflow
SANITIZER_ADDL_FLAGS=

SRCS=$(wildcard *.c)

GRAD_EXES=$(SRCS:.c=.grad.exe)
TAINT_EXES=$(SRCS:.c=.taint.exe)
BASE_EXES=$(SRCS:.c=.base.exe)
BITCODES=$(SRCS:.c=.dfsan.bc)
LLS=$(SRCS:.c=.plain.ll)
CC=$(LLVM_BINPATH_PLAIN)/clang
BASE_CC=$(LLVM_BINPATH_PLAIN)/clang
GRAD_CC=$(LLVM_BINPATH_GRSAN)/clang

#all: $(LLS) $(BITCODES) $(EXES)
all: $(GRAD_EXES) $(BASE_EXES) $(TAINT_EXES)

%.grad.exe: %.c
	GRTRACK=1 $(GRAD_CC) $(CXXFLAGS) $< -o $@ $(SANITIZER_FLAGS) $(SANITIZER_ADDL_FLAGS) $(LLVM_LDFLAGS_GRSAN)

%.taint.exe: %.c
	GRTRACK=1 $(BASE_CC) $(CXXFLAGS) $< -o $@ $(SANITIZER_FLAGS) $(SANITIZER_ADDL_FLAGS) $(LLVM_LDFLAGS)

%.base.exe: %.c
	$(BASE_CC) $(CXXFLAGS) $< -o $@ 

%.plain.ll:	%.c
	$(CC) $(CFLAGS) -emit-llvm -S $< -o $@

%.plain.ll:	%.cpp
	$(CXX) $(CXXFLAGS) -emit-llvm -S $< -o $@

%.dfsan.bc:	%.c
	$(CC) $(CFLAGS) -c -emit-llvm $< -o $@ $(SANITIZER_FLAGS) $(SANITIZER_ADDL_FLAGS) 
	$(DIS) $@

%.dfsan.bc:	%.cpp
	$(CXX) $(CXXFLAGS) -c -emit-llvm $< -o $@ $(SANITIZER_FLAGS) $(SANITIZER_ADDL_FLAGS)
	$(DIS) $@

test:
	./run_tests.sh

clean:
	rm *.exe *.bc *.ll 2>/dev/null || true

