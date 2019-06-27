ROOT=../../conf

BIN_DIR_LLVM=../../llvm-7.0.0.build/`uname -m`/llvm-7.0/bin/bin

include ${ROOT}/common.inc

CFLAGS=-O0 -g3
CXXFLAGS=-O0 -g3
SANITIZER_FLAGS=-fsanitize=dataflow
SANITIZER_ADDL_FLAGS=

SRCS=$(wildcard *.c)

EXES=$(SRCS:.c=.exe)
BITCODES=$(SRCS:.c=.dfsan.bc)
LLS=$(SRCS:.c=.plain.ll)

all: $(LLS) $(BITCODES) $(EXES)

%.exe: %.c
	$(CC) $(CFLAGS) $< -o $@ $(SANITIZER_FLAGS) $(SANITIZER_ADDL_FLAGS)

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

clean:
	rm *.log *.txt *.exe *.bc *.ll 2>/dev/null || true

ann:
	python ../instruction_parser.py scratch.dfsan.ll hello.txt
