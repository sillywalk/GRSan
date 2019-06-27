#include <sanitizer/dfsan_interface.h>
#include <stdio.h>
#include <assert.h>


int double_int(int a) {
    return 2 *a;
}

int double_ptrint(int * a) {
    return *a * 2;
}
int quadruple_int_with_variable(int a) {
    int two = 2;
    return two *two *a;
}

int main(void) {

  int i = 2;
  float init_deriv = 1.0;
  dfsan_label i_label = dfsan_create_label("i", init_deriv);
  dfsan_set_label(i_label, &i, sizeof(i));

  int res = double_int(i);
  dfsan_label res_label = dfsan_get_label(res);
  const struct dfsan_label_info* res_info = dfsan_get_label_info(res_label);
  printf("res, %d -- res label %d: %f %s\n", res, res_label, res_info->neg_dydx, res_info->desc);
  assert(res_info->neg_dydx == 2.0);

  res = double_int(2);
  res_label = dfsan_get_label(res);
  res_info = dfsan_get_label_info(res_label);
  printf("res, %d -- res label %d: %f %s\n", res, res_label, res_info->neg_dydx, res_info->desc);
  assert(res_info->neg_dydx == 0.0);

  res = double_ptrint(&i);
  res_label = dfsan_get_label(res);
  res_info = dfsan_get_label_info(res_label);
  printf("res, %d -- res label %d: %f %s\n", res, res_label, res_info->neg_dydx, res_info->desc);
  assert(res_info->neg_dydx == 2.0);

  res = quadruple_int_with_variable(i);
  res_label = dfsan_get_label(res);
  res_info = dfsan_get_label_info(res_label);
  printf("res, %d -- res label %d: %f %s\n", res, res_label, res_info->neg_dydx, res_info->desc);
  assert(res_info->neg_dydx == 4.0);

  res = double_int(res);
  res_label = dfsan_get_label(res);
  res_info = dfsan_get_label_info(res_label);
  printf("res, %d -- res label %d: %f %s\n", res, res_label, res_info->neg_dydx, res_info->desc);
  assert(res_info->neg_dydx == 8.0);
  
  return 0;
}
