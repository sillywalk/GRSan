all:	plain dfsan grsan

plain:
	GR_BUILD_TYPE="plain" ./make.sh

dfsan:
	GR_BUILD_TYPE="dfsan" ./make.sh

grsan:
	GR_BUILD_TYPE="grsan" ./make.sh

distclean:
	rm -rf llvm_build
