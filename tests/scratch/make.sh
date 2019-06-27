rm hello.txt annotated-hello.txt;
make clean && make 2>&1 | tee build.log && ./scratch.exe 2>&1 | tee out.log 
