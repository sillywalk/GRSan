#include <sanitizer/dfsan_interface.h>
#include <stdio.h>
#include <assert.h>

int main(void) {
  char *str1 = "string1";
  char str2[100];

  dfsan_label i_label;
  const struct dfsan_label_info* i_info;
  float init_deriv = 1.0;
  i_label = dfsan_create_label("file_labeled", init_deriv);
  dfsan_set_label(i_label, &str1[0], sizeof(char));

  i_label = dfsan_get_label(str1[0]);
  i_info = dfsan_get_label_info(i_label);
  printf("str1 i label %d: %f %s\n",i_label, i_info->neg_dydx, i_info->desc);

//  strcpy(str2, str1);
//  strncpy(str2, str1, 7);
  memcpy(str2, str1, 7);
  i_label = dfsan_get_label(str1[0]);
  i_info = dfsan_get_label_info(i_label);
  printf("str1 i label %d: %f %s\n",i_label, i_info->neg_dydx, i_info->desc);
  i_label = dfsan_get_label(str2[0]);
  i_info = dfsan_get_label_info(i_label);
  printf("str2 i label %d: %f %s\n",i_label, i_info->neg_dydx, i_info->desc);
  i_label = dfsan_get_label(str2[1]);
  i_info = dfsan_get_label_info(i_label);
  printf("str2 i[1] label %d: %f %s\n",i_label, i_info->neg_dydx, i_info->desc);
   
  return 0;
}
