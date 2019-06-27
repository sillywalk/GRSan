
#ifdef GRTRACK
#include <sanitizer/dfsan_interface.h>
#endif

#define REP10(X) X X X X X X X X X X
#define REP1000(X) REP10(REP10(X))
#define REP1000000(X) REP1000(REP1000(X))

#define NITERS 100000

int main() {
  /*unsigned long x = 1;*/
  /*for (unsigned long i=0; i<100000000; i++) {*/
    /*x = x & i;*/
  /*}*/
  float i = 100000;
  float x = 11111;
  float y = 100000;

#ifdef GRTRACK
  float init = 1.0;
  dfsan_label i_label = dfsan_create_label("i", init);
  dfsan_set_label(i_label, &i, sizeof(i));
#endif

  for (int j=0; j<NITERS; j++) {
    REP1000(REP1000(y = i / x;))
  }

  return 0;
}

