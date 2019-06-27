#include <stdio.h>
#include <limits.h>
#include <stdlib.h>

#ifdef GRTRACK
#include <dfsan_interface.h>
#endif


int main(int argc, char** argv) {

  /*malloc(ULONG_MAX);*/

  int mark_ind = atoi(argv[1]);
  char* fname = argv[2];
  FILE *file;
  file = fopen(fname, "r");
  unsigned char buf[32];

  size_t f_ind = ftell(file);
  size_t nread = fread(buf, 1, sizeof buf, file);

#ifdef GRTRACK
  float initial = 1.0;
  /*printf("labeling buf %zu\n", mark_ind);*/
  dfsan_label i_label = dfsan_create_label("decompress", initial);
  dfsan_set_label(i_label, &in[mark_ind - f_ind], sizeof(in[mark_ind - f_ind]));
#endif

  unsigned long m1 = buf[2], m2 = buf[3], m3 = buf[4], m4 = buf[5];
  unsigned long malloc_sz = (m1<<56) + m4;

  /*[>size_t malloc_sz = ((((size_t)buf[2])<<24) + (((size_t)buf[3])<<16) + (((size_t)buf[4])<<8) + (((size_t)buf[5])));<]*/
  /*[>size_t t = ((unsigned long)255)<<24;<]*/
  /*size_t t = ULONG_MAX;*/
  /*printf("malloc_sz = %lu, %lu, %lu\n", malloc_sz, t, m1);*/
  printf("malloc_sz = %lu, %u\n", malloc_sz, m1);
  char *x = (char*)malloc(malloc_sz);
  free(x);

  fclose(file);

  return 0;

}
