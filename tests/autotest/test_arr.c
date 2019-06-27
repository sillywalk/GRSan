#include <sanitizer/dfsan_interface.h>
#include <stdio.h>
#include <assert.h>
int main(void) {
   
  int i, j, k, r, v, x;
  int arr[3] = {2, 5, 7};
  i = 2;
  j = 3;
  k = 4;
  r = 5;
  float init = 1.0;
  dfsan_label i_label = dfsan_create_label("i", init);
  dfsan_set_label(i_label, &i, sizeof(i));

  arr[1] = i;

  /*for (j=0; j<3; j++) {*/
    /*k = j*arr[j];*/
  /*}   */
  k = j*arr[0];
  r = j*arr[1];

  dfsan_label k_label = dfsan_get_label(k);
  dfsan_label r_label = dfsan_get_label(r);
  const struct dfsan_label_info* i_info = dfsan_get_label_info(i_label);
  const struct dfsan_label_info* k_info = dfsan_get_label_info(k_label);
  const struct dfsan_label_info* r_info = dfsan_get_label_info(r_label);

  printf("i label %d: %f\n",i_label, i_info->neg_dydx);
  printf("k label %d: %f\n",k_label, k_info->neg_dydx);
  printf("r label %d: %f\n",r_label, r_info->neg_dydx);

  assert(i_info->neg_dydx == 1.0);
  assert(i_info->pos_dydx == 1.0);
  assert(k_info->neg_dydx == 0.0);
  assert(k_info->pos_dydx == 0.0);
  assert(r_info->neg_dydx == 3.0);
  assert(r_info->pos_dydx == 3.0);
   
   
  return 0;
}
