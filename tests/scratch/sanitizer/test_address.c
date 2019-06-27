#include <stdlib.h>
#include <limits.h>
#include <stdio.h>


int main(int argc, char** argv) {

  char arr[40];

  /*malloc(ULONG_MAX);*/
  size_t GB = 1000000000;
  size_t alloc = atoi(argv[1]);
  
  printf("mallocing %lu gb\n", alloc);

  alloc = alloc*GB;
  malloc(alloc);

  /*arr[42] = 1;*/

  return 0;
}
