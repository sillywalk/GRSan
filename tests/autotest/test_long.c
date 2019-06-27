#include <sanitizer/dfsan_interface.h>
#include <stdio.h>
#include <assert.h>

int main(void) {
   
  long i, j, k, r, v, x, y, mult3, loop, assign_twice; 
  i = 1;
  j = 4;
  k = 4;
  r = 5;
  float init_deriv = 1.0;
  dfsan_label i_label = dfsan_create_label("i", init_deriv);
  dfsan_set_label(i_label, &i, sizeof(i));
  //test
  // test2
  if (i > 0) { 
    k = j + i;
    r = i - k;
    x = i * k;
    v = k / i;
    y = i * 2;
    mult3 = i * i * i;

    for (int a=0; a<3; a++) {
      loop = i * a;
    }

    assign_twice = i*3;
    assign_twice = i*4;
  }

  /*dfsan_label i_label = dfsan_get_label(i);*/
  dfsan_label k_label = dfsan_get_label(k);
  dfsan_label r_label = dfsan_get_label(r);
  dfsan_label x_label = dfsan_get_label(x);
  dfsan_label v_label = dfsan_get_label(v);
  dfsan_label y_label = dfsan_get_label(y);
  dfsan_label mult3_label = dfsan_get_label(mult3);
  dfsan_label loop_label = dfsan_get_label(loop);
  dfsan_label assign_twice_label = dfsan_get_label(assign_twice);
  const struct dfsan_label_info* i_info = dfsan_get_label_info(i_label);
  const struct dfsan_label_info* k_info = dfsan_get_label_info(k_label);
  const struct dfsan_label_info* r_info = dfsan_get_label_info(r_label);
  const struct dfsan_label_info* x_info = dfsan_get_label_info(x_label);
  const struct dfsan_label_info* v_info = dfsan_get_label_info(v_label);
  const struct dfsan_label_info* y_info = dfsan_get_label_info(y_label);
  const struct dfsan_label_info* mult3_info = dfsan_get_label_info(mult3_label);
  const struct dfsan_label_info* loop_info = dfsan_get_label_info(loop_label);
  const struct dfsan_label_info* assign_twice_info = dfsan_get_label_info(assign_twice_label);

  printf("i label %d: %f\n",i_label, i_info->neg_dydx);
  printf("k label %d: %f\n",k_label, k_info->neg_dydx);
  printf("r label %d: %f\n",r_label, r_info->neg_dydx);
  printf("x label %d: %f\n",x_label, x_info->neg_dydx);
  printf("v label %d: %f\n",v_label, v_info->neg_dydx);
  printf("mult3 label %d: %f\n",mult3_label, mult3_info->neg_dydx);

  assert(i_info->neg_dydx == 1.0);
  assert(i_info->pos_dydx == 1.0);
  assert(k_info->neg_dydx == 1.0);
  assert(k_info->pos_dydx == 1.0);
  assert(r_info->neg_dydx == 0.0);
  assert(r_info->pos_dydx == 0.0);
  assert(x_info->neg_dydx == 6.0);
  assert(x_info->pos_dydx == 6.0);
  assert(v_info->neg_dydx == -4.0);
  assert(v_info->pos_dydx == -4.0);
  assert(y_info->neg_dydx == 2.0);
  assert(y_info->pos_dydx == 2.0);
  assert(mult3_info->neg_dydx == 3.0);
  assert(mult3_info->pos_dydx == 3.0);
  assert(loop_info->neg_dydx == 2.0);
  assert(loop_info->pos_dydx == 2.0);
  assert(assign_twice_info->neg_dydx == 4.0);
  assert(assign_twice_info->pos_dydx == 4.0);
   
  return 0;
}