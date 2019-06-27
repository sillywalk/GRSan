#include <sanitizer/dfsan_interface.h>
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>



int main(void) {

  size_t i = 10;

  float init_deriv = 1.0;
  dfsan_label i_label = dfsan_create_label("i", init_deriv);
  dfsan_set_label(i_label, &i, sizeof(i));

  char *str = (char*) malloc(i);
  char strbuf[40];
  char strbuf2[40];

  strncpy(str, "asdf", 4);
  strncpy(strbuf, str, i);


  memcpy(strbuf2, str, i);
  printf("memcpy res: %s\n", strbuf2);

  char *str2 = (char*) calloc(i, i);


  if (i > 0) {
    printf("branch\n");
    printf("%s\n", str);
  }

  /*char str1 = "testing 123";*/
  /*i = i * 4;*/
  /*char str2[40];*/
  /*char str3[40];*/

  /*strncpy ( str2, str1, i);*/

  return 0;
}
