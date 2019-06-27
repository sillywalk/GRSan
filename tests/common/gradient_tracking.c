

#include "gradient_tracking.h"

#ifdef GRTRACK
#include <sanitizer/dfsan_interface.h>

/* 
    This function opens a file called `name` for writing. 
    You can access the file via the 'data_file' variable. 
    When finished using the file, call the `close_datafile()` function.
*/
void init_datafile(char* name) {
  data_file = fopen (name,"a");
  /*fprintf(data_file, "var_name, var_index, mark_index, label, value, neg_deriv, pos_deriv\n");*/
}


void close_datafile() { fclose (data_file); }

/* 
    This function assigns a named (via `name`) label with derivative 1.0
    to memory [addr, addr+size].
*/
/*void mark_grad(char* name, void* addr, size_t size) {*/
    /*float initial = 1.0;*/
    /*dfsan_label i_label = dfsan_create_label(name, initial);*/
    /*dfsan_set_label(i_label, addr,  size);*/
/*}*/


#define PRINT_ONE_TEMPLATE(FunctionName, Type, PrintFormat1, PrintFormat2)      \
  void FunctionName(char *name, Type val, size_t print_ind) {            \
    dfsan_label l = dfsan_get_label(val); \
    const struct dfsan_label_info* li; \
    if (l) { \
      li = dfsan_get_label_info(l); \
      printf("%s, %zu, %zu, %u, " PrintFormat1 ", %f, %f\n", name, print_ind, mark_ind, l, val, li->neg_dydx, li->pos_dydx); \
      if (data_file) { \
        fprintf(data_file, "%s, %zu, %zu, %u, " PrintFormat2 ", %f, %f\n", name, print_ind, mark_ind, l, val, li->neg_dydx, li->pos_dydx); \
      } \
    } else { \
      printf("%s, %zu, %zu, %u, " PrintFormat1 ", 0.0, 0.0 \n", name, print_ind, mark_ind, l, val); \
      if (data_file) { \
        fprintf(data_file, "%s, %zu, %zu, %u, " PrintFormat2 ", 0.0, 0.0 \n", name, print_ind, mark_ind, l, val); \
      } \
    } \
  } \

#define PRINT_MANY_TEMPLATE(FunctionName, Type, PrintFormat1, PrintFormat2)      \
  void FunctionName(char *name, Type* vals, size_t len) {            \
    size_t cnt = 0; \
    for (size_t i=0; i<len; i++) { \
      dfsan_label l = dfsan_get_label(vals[i]); \
      const struct dfsan_label_info* li; \
      if (l) { \
        cnt++; \
        li = dfsan_get_label_info(l); \
        printf("%s, %zu, %zu, %u, " PrintFormat1 ", %f, %f\n", name, i, mark_ind, l, vals[i], li->neg_dydx, li->pos_dydx); \
        if (data_file) { \
          fprintf(data_file, "%s, %zu, %zu, %u, " PrintFormat2 ", %f, %f\n", name, i, mark_ind, l, vals[i], li->neg_dydx, li->pos_dydx); \
        } \
      } else { \
        printf("%s, %zu, %zu, %u, " PrintFormat1 ", 0.0, 0.0 \n", name, i, mark_ind, l, vals[i]); \
        if (data_file) { \
          fprintf(data_file, "%s, %zu, %zu, %u, " PrintFormat2 ", 0.0, 0.0 \n", name, i, mark_ind, l, vals[i]); \
        } \
      } \
    } \
    printf("total marked %zu\n", cnt); \
  } \

#define COUNT_MANY_TEMPLATE(FunctionName, Type)      \
  size_t FunctionName(Type* vals, size_t len) {            \
    size_t cnt = 0; \
    for (size_t i=0; i<len; i++) { \
      dfsan_label l = dfsan_get_label(vals[i]); \
      if (l) { \
        cnt++; \
      } \
    } \
    return cnt; \
  } \

/*
    These are a set of macros involving derivatives with different types.

    The COUNT_MANY_TEMPLATE generates a function that counts the number of non-zero derivatives in an array up to length `len`.
        Example: size_t grad_byte_arr_cnt(unsigned char* vals, size_t len)

    The PRINT_ONE_TEMPLATE generates a function that prints/logs the derivative associated with `val`.
        Example: void print_grad_long(char *name, unsigned long val, size_t print_ind)

        The format is name, iteration_count(if in loop), mark_index, gradient_label, value, neg_deriv, pos_deriv 
        Example: inffast.inflate_fast:117 hold, 65, 0, 0, 6750300, 0.0, 0.0

    The PRINT_MANY_TEMPLATE generates a function that prints/logs the derivative in an array of size `len`
        Example: void print_grad_byte_arr(char *name, unsigned char* vals, size_t len)

        The format is name, index, mark_index, gradient_label, value, neg_deriv, pos_deriv 
        Example: read_buf, 1, 0, 0, 101, 0.0, 0.0

*/
PRINT_ONE_TEMPLATE(print_grad_long, unsigned long, "%zu", "%zu")
PRINT_ONE_TEMPLATE(print_grad_byte, unsigned char, "%u", "%u")
PRINT_ONE_TEMPLATE(print_grad_int, unsigned int, "%u", "%u")
// s-int for signed
PRINT_ONE_TEMPLATE(print_grad_sint, int, "%d", "%d")
PRINT_ONE_TEMPLATE(print_grad_sbyte, char, "%d", "%d")
PRINT_MANY_TEMPLATE(print_grad_byte_arr, unsigned char, "%u", "%u")
COUNT_MANY_TEMPLATE(grad_byte_arr_cnt, unsigned char)

#else
/*void init_datafile(char* name) {}*/
/*void close_datafile() {}*/
/*void print_grad_byte(char* name, unsigned char byte, size_t print_ind) {}*/
/*void print_grad_long(char* name, unsigned long val, size_t print_ind) {}*/
/*void print_grad_int(char* name, unsigned int val, size_t print_ind) {}*/

/*void print_grad_sint(char* name, int val, size_t print_ind) {}*/
/*void print_grad_sbyte(char* name, char val, size_t print_ind) {}*/

/*void print_grad_byte_arr(char* name, unsigned char* bytes, size_t len) {}*/


#endif
