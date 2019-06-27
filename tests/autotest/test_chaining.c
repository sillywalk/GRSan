#include <sanitizer/dfsan_interface.h>
#include <stdio.h>
#include <assert.h>

void test_int(void) {
  int i, res;
  i = 2;

  float init_deriv = 1.0;
  dfsan_label i_label = dfsan_create_label("i", init_deriv);
  dfsan_set_label(i_label, &i, sizeof(i));

  res = i * i * i;

    
  /*dfsan_label i_label = dfsan_get_label(i);*/
  dfsan_label res_label = dfsan_get_label(res);
  const struct dfsan_label_info* i_info = dfsan_get_label_info(i_label);
  const struct dfsan_label_info* res_info = dfsan_get_label_info(res_label);

  printf("i label %d: %f\n", i_label, i_info->neg_dydx);
  printf("res label %d: %f\n", res_label, res_info->neg_dydx);

  assert(i_info->neg_dydx == 1.0);
  assert(i_info->pos_dydx == 1.0);
  assert(res_info->neg_dydx == 12.0);
  assert(res_info->pos_dydx == 12.0);
 
}

void test_long(void) {
  long i, res;
  i = 2;

  float init_deriv = 1.0;
  dfsan_label i_label = dfsan_create_label("i", init_deriv);
  dfsan_set_label(i_label, &i, sizeof(i));

  res = i * i * i;

    
  /*dfsan_label i_label = dfsan_get_label(i);*/
  dfsan_label res_label = dfsan_get_label(res);
  const struct dfsan_label_info* i_info = dfsan_get_label_info(i_label);
  const struct dfsan_label_info* res_info = dfsan_get_label_info(res_label);

  printf("i label %d: %f\n", i_label, i_info->neg_dydx);
  printf("res label %d: %f\n", res_label, res_info->neg_dydx);

  assert(i_info->neg_dydx == 1.0);
  assert(i_info->pos_dydx == 1.0);
  assert(res_info->neg_dydx == 12.0);
  assert(res_info->pos_dydx == 12.0);
 
}

void test_char(void) {
  char i, res;
  i = 2;

  float init_deriv = 1.0;
  dfsan_label i_label = dfsan_create_label("i", init_deriv);
  dfsan_set_label(i_label, &i, sizeof(i));

  res = i * i * i;

    
  /*dfsan_label i_label = dfsan_get_label(i);*/
  dfsan_label res_label = dfsan_get_label(res);
  const struct dfsan_label_info* i_info = dfsan_get_label_info(i_label);
  const struct dfsan_label_info* res_info = dfsan_get_label_info(res_label);

  printf("i label %d: %f\n", i_label, i_info->neg_dydx);
  printf("res label %d: %f\n", res_label, res_info->neg_dydx);

  assert(i_info->neg_dydx == 1.0);
  assert(i_info->pos_dydx == 1.0);
  assert(res_info->neg_dydx == 12.0);
  assert(res_info->pos_dydx == 12.0);
 
}

int main(void) {

  test_int();
  test_long();
  test_char();
  
  return 0;
}
