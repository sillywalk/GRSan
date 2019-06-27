echo "PERF EVAL:" >> results.log

echo "base"
#for p in *base.exe; do echo $p; echo $p >> results.log; for i in 1 2 3; do echo $i; { /usr/bin/time -f "%U" ./$p; } 2>>results.log ; done; echo ' '; done

export GR_MODE_PERF=1;
echo "taint"
for p in *taint.exe; do echo $p; echo $p >> results.log; for i in 1 2 3; do echo $i; { /usr/bin/time -f "%U" ./$p; } 2>>results.log ; done; echo ' '; done


echo "grad"
#for p in *grad.exe; do echo $p; echo $p >> results.log; for i in 1 2 3; do echo $i; { /usr/bin/time -f "%U" ./$p; } 2>>results.log ; done; echo ' '; done
