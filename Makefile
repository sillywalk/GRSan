


.PHONY: tests
tests:
	make -C tests

test:
	make -C tests/autotest test

clean:
	make -C tests/autotest clean

setuptaint:
	cd ./llvm-7.0.0.build/ && ./baseline_dfsan_setup.sh
	cd ./llvm-7.0.0.build/ && SETTINGS_INC_FILE=configure.taint.inc ./configure.sh && SETTINGS_INC_FILE=configure.taint.inc ./make.sh

setupgrad:
	cd ./llvm-7.0.0.build/ &&  ./configure.sh && ./make.sh

# ONLY USE AFTER 'setuptaint' make rule
cleantaint:
	# be careful with command
	git checkout llvm-7.0.0.src/projects
	git checkout llvm-7.0.0.src/lib

grad:
	cd ./llvm-7.0.0.build/ && ./make.sh

taint:
	cd ./llvm-7.0.0.build/ && ./baseline_dfsan_setup.sh
	cd ./llvm-7.0.0.build/ && SETTINGS_INC_FILE=configure.taint.inc ./make.sh


distclean:
	rm -rf ./llvm-7.0.0.build/x86_64


distcleantaint:
	rm -rf ./llvm-7.0.0.build/x86_64_taint
