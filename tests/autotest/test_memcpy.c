#include <sanitizer/dfsan_interface.h>
#include <stdio.h>
#include <assert.h>


int main(void) {
   
  char arr[3] = {2, 5, 7};
  char arr2[4];
  
  float init = 1.0;
  dfsan_label i_label = dfsan_create_label("i", init);
  dfsan_set_label(i_label, &arr[1], 1);

  dfsan_label j_label = dfsan_create_label("j", init);
  dfsan_set_label(j_label, &arr2[1], 1);



  memcpy(&arr2[1], arr, 3);

  dfsan_label l1 = dfsan_get_label(arr2[2]);
  assert(l1 != 0);

  dfsan_label l2 = dfsan_get_label(arr2[1]);
  assert(l2 == 0);

  const struct dfsan_label_info* l1i = dfsan_get_label_info(l1);

  printf("%u: %f, %f\n", l1, l1i->neg_dydx, l1i->pos_dydx);
   
  return 0;
}
