all:
	gcc -g -o neuzz neuzz.c

fuzzer: 
	python3 run_fuzzer.py grad ./neuzz ../dfsan_grad_comparison/jpeg/bin/djpeg_fuzz ../dfsan_grad_comparison/jpeg/inputs/small1by1

comp:
	# djepg
	#rm -rf seeds* taint_info*
	#python3 comp_fuzzer.py ./neuzz ./djpeg /local/gabe1/share/neuzz10/jpeg1 /local/gabe1/share/neuzz10/jpeg10_grad/ /local/gabe1/share/neuzz10/jpeg10_taint/ 512
	###GRADTEST_FLAGS="" python3 comp_fuzzer.py ./neuzz ../dfsan_grad_comparison/jpeg/bin/djpeg_fuzz /local/dongdong/share/ /local/dongdong/gradtest/gradtest/exps/programs/readelf/inputs/afl_out/readelf_grad /local/dongdong/gradtest/gradtest/exps/programs/readelf/inputs/afl_out/readelf_taint 16
	#python3 comp_fuzzer.py ./neuzz ./djpeg /local/dongdong/share/24h/libjpeg_10 /local/dongdong/share/24h/libjpeg_grad /local/dongdong/share/24h/libjpeg_taint 16
	
	# xmlint
	#rm -rf seeds* taint_info*
	python3 comp_fuzzer.py ./neuzz ./xmllint /local/gabe1/share/neuzz10/libxml1 /local/gabe1/share/neuzz10/libxml10_grad/ /local/gabe1/share/neuzz10/libxml10_taint/ 512 /local/dongdong/gradtest/gradtest/exps/programs/libxml/bin/libxml.sh
	#python3 comp_fuzzer.py ./neuzz ./xmllint /local/dongdong/share/24h/libxml_10 /local/dongdong/share/24h/libxml_grad /local/dongdong/share/24h/libxml_taint 16
	
	# mupdf
	#rm -rf seeds* taint_info*
	#GRADTEST_FLAGS="show" python3 comp_fuzzer.py ./neuzz ./mutool /local/gabe1/share/neuzz10/mupdf1 /local/gabe1/share/neuzz10/mupdf10_grad/ /local/gabe1/share/neuzz10/mupdf10_taint/ 512
	#GRADTEST_FLAGS="show" python3 comp_fuzzer.py ./neuzz ./mutool /local/dongdong/share/24h/mupdf_10 /local/dongdong/share/24h/mupdf_grad /local/dongdong/share/24h/mupdf_taint 16
	
	# strip
	#rm -rf seeds* taint_info*
	#GRADTEST_FLAGS="-o sss" python3 comp_fuzzer.py ./neuzz ./strip-new /local/gabe1/share/neuzz10/strip1 /local/gabe1/share/neuzz10/strip10_grad/ /local/gabe1/share/neuzz10/strip10_taint/ 512
	###GRADTEST_FLAGS="-a" python3 comp_fuzzer.py ./neuzz ../../tests/binutils-2.30/llvm_build/fuzz/install/bin/readelf /local/dongdong/gradtest/gradtest/exps/programs/readelf/inputs/afl_out/readelf /local/dongdong/gradtest/gradtest/exps/programs/readelf/inputs/afl_out/readelf_grad /local/dongdong/gradtest/gradtest/exps/programs/readelf/inputs/afl_out/readelf_taint 16
	
	# objdump
	#rm -rf seeds* taint_info*
	#GRADTEST_FLAGS="-xD" python3 comp_fuzzer.py ./neuzz ./objdump /local/gabe1/share/neuzz10/objdump1 /local/gabe1/share/neuzz10/objdump10_grad/ /local/gabe1/share/neuzz10/objdump10_taint/ 512
	###GRADTEST_FLAGS="-a" python3 comp_fuzzer.py ./neuzz ../../tests/binutils-2.30/llvm_build/fuzz/install/bin/readelf /local/dongdong/gradtest/gradtest/exps/programs/readelf/inputs/afl_out/readelf /local/dongdong/gradtest/gradtest/exps/programs/readelf/inputs/afl_out/readelf_grad /local/dongdong/gradtest/gradtest/exps/programs/readelf/inputs/afl_out/readelf_taint 16

	# readel
	#rm -rf seeds* taint_info*
	#GRADTEST_FLAGS="-a" python3 comp_fuzzer.py ./neuzz ./readelf /local/gabe1/share/neuzz10/readelf1 /local/gabe1/share/neuzz10/readelf10_grad /local/gabe1/share/neuzz10/readelf10_taint 16
	#GRADTEST_FLAGS="-a" python3 comp_fuzzer.py ./neuzz ./readelf /local/dongdong/share/24h/readelf_10 /local/dongdong/gradtest/gradtest/exps/programs/readelf/inputs/afl_out/readelf_grad /local/dongdong/gradtest/gradtest/exps/programs/readelf/inputs/afl_out/readelf_taint 16
	
	# minigzip
	#rm -rf seeds* taint_info*
	#GRADTEST_FLAGS="-c -d" python3 comp_fuzzer.py ./neuzz ../../tests/zlib-1.2.11/llvm_build/fuzz/minigzip /local/gabe1/share/neuzz10/zlib10 /local/gabe1/share/neuzz10/zlib10_grad/ /local/gabe1/share/neuzz10/zlib10_taint/ 512
	###GRADTEST_FLAGS="-a" python3 comp_fuzzer.py ./neuzz ../../tests/binutils-2.30/llvm_build/fuzz/install/bin/readelf /local/dongdong/gradtest/gradtest/exps/programs/readelf/inputs/afl_out/readelf /local/dongdong/gradtest/gradtest/exps/programs/readelf/inputs/afl_out/readelf_grad /local/dongdong/gradtest/gradtest/exps/programs/readelf/inputs/afl_out/readelf_taint 16
gentaint:
	python3 generate_fuzzer_info.py grad ../dfsan_grad_comparison/jpeg/inputs/small1by1_grad/ ../dfsan_grad_comparison/jpeg/inputs/small1by1/ 512
