all:	base dfsan grsan fuzz

base:
	GR_BUILD_TYPE="base" ./make.sh

dfsan:
	GR_BUILD_TYPE="dfsan" ./make.sh

grsan:
	GR_BUILD_TYPE="grsan" ./make.sh

fuzz:
	GR_BUILD_TYPE="fuzz" ./make.sh

fast:
	GR_BUILD_TYPE="fast" ./make.sh

bug:
	GR_BUILD_TYPE="bug" ./make.sh

distclean:
	rm -rf llvm_build
