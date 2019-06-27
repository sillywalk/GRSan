afl:
	rm -rf afl_*
	mkdir -p afl_in afl_out
	cp apt-binary.gz afl_in
	afl-fuzz -i afl_in -o afl_out/ -- ./zlib/bin/minigzip_fuzz @@
	echo "the mutated filesw are in afl_out/queue"
runcomparison:
	rm -f branches.csv final_labels.txt input
	python3 comp_exp.py jpeg/bin/jpeg.sh jpeg/inputs/small1by1
genbranch:
	rm -f branches.csv final_labels.txt input
	python3 eval_gradient.py taint jpeg/bin/jpeg.sh jpeg/inputs/small1by1
	python3 eval_gradient.py grad jpeg/bin/jpeg.sh jpeg/inputs/small1by1
