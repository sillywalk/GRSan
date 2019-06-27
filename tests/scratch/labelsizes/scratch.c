#include <sanitizer/dfsan_interface.h>
#include <stdio.h>

int main(void) {
  
  int8_t sx8 = 0;
  int16_t sx16 = 0;
  int32_t sx32 = 0;
  int64_t sx64 = 0;


  float init_deriv = 1.0;
  dfsan_label i_label8 = dfsan_create_label("sx8", init_deriv);
  dfsan_set_label(i_label8, &sx8, sizeof(sx8));
  dfsan_label i_label16 = dfsan_create_label("sx16", init_deriv);
  dfsan_set_label(i_label16, &sx16, sizeof(sx16));
  dfsan_label i_label32 = dfsan_create_label("sx32", init_deriv);
  dfsan_set_label(i_label32, &sx32, sizeof(sx32));
  dfsan_label i_label64 = dfsan_create_label("sx64", init_deriv);
  dfsan_set_label(i_label64, &sx64, sizeof(sx64));

  if (sx8 != 1) {
    printf("sx8\n");
  } else {
    printf("else\n");
  }



  if (sx16 != 1) {
    printf("sx16\n");
  } else {
    printf("else\n");
  }


  if (sx32 != 1) {
    printf("sx32\n");
  } else {
    printf("else\n");
  }


  if (sx64 != 1) {
    printf("sx64\n");
  } else {
    printf("else\n");
  }



  return 0;
}
 
