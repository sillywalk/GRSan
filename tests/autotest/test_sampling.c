#include <sanitizer/dfsan_interface.h>
#include <stdio.h>
#include <assert.h>



int main(void) {
   
  int x, y;
  x = 4;

  float init_deriv = 1.0;
  dfsan_label i_label = dfsan_create_label("i", init_deriv);
  dfsan_set_label(i_label, &x, sizeof(x));

  y = x & 4;
  

  /*dfsan_label i_label = dfsan_get_label(i);*/
  dfsan_label y_label = dfsan_get_label(y);
  const struct dfsan_label_info* yi = dfsan_get_label_info(y_label);

  printf("i label %d: %f, %f\n",y_label, yi->neg_dydx, yi->pos_dydx);

  assert(yi->neg_dydx == 4.0);
  assert(yi->pos_dydx == -1.0);
   
  return 0;
}
