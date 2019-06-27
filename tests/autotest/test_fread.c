#include <sanitizer/dfsan_interface.h>
#include <stdio.h>
#include <assert.h>


int main(void) {
   
  char buf[16];
  
  float init = 1.0;
  dfsan_label i_label = dfsan_create_label("i", init);
  dfsan_set_label(i_label, &buf[1], 1);

  FILE* f = fopen("test_fread.c", "r");

  size_t nread = fread(buf, 1, 16, f);

  dfsan_label l1 = dfsan_get_label(buf[1]);
  assert(l1 == 0);

  fclose(f);

  return 0;
}
