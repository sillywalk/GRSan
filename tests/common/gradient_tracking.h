#ifndef GRADIENT_TRACKING_H
#define GRADIENT_TRACKING_H
#include <limits.h>

#define MARK_IND_INIT() mark_ind = -1;

#ifdef GRTRACK
#include <sanitizer/dfsan_interface.h>

//#include <sanitizer/dfsan_interface.h>
#include <stdio.h>

FILE * data_file;

long mark_ind; // the index of the byte to mark as the independent variable
size_t n_inputs; // UNUSED
/* two parallel lists that keep track of which byte and by how much it should changed by */
int change_ind[32];/* which byte to change */
int change[32];/* how much to change the byte by */
size_t n_changes; // keeps track of position in change and change_ind


//void init_datafile(char* name);

#define INIT_DATAFILE(name) data_file = fopen(name, "a"); \
  fprintf(data_file, "name,print_ind,deriv_byte,label,value,ndx,pdx,\n"); \

//void close_datafile();

#define CLOSE_DATAFILE()  fclose(data_file);

void print_grad_byte(char* name, unsigned char byte, size_t print_ind);
void print_grad_long(char* name, unsigned long val, size_t print_ind);
void print_grad_int(char* name, unsigned int val, size_t print_ind);

void print_grad_sint(char* name, int val, size_t print_ind);
void print_grad_sbyte(char* name, char val, size_t print_ind);

void print_grad_byte_arr(char* name, unsigned char* bytes, size_t len);

//#define LOG_GRAD(name, val, print_ind, format) \
  //dfsan_label l = dfsan_get_label(val); \
  //const struct dfsan_label_info* li; \
  //if (l) { \
    //li = dfsan_get_label_info(l); \
    //printf("%s, %zu, %zu, %u, " format ", %f, %f\n", name, print_ind, mark_ind, l, val, li->neg_dydx, li->pos_dydx); \
    //if (data_file) { \
      //fprintf(data_file, "%s, %zu, %zu, %u, " format ", %f, %f\n", name, print_ind, mark_ind, l, val, li->neg_dydx, li->pos_dydx); \
    //} \
  //} else { \
    //printf("%s, %zu, %zu, %u, " format ", 0.0, 0.0 \n", name, print_ind, mark_ind, l, val); \
    //if (data_file) { \
      //fprintf(data_file, "%s, %zu, %zu, %u, " format ", 0.0, 0.0 \n", name, print_ind, mark_ind, l, val); \
    //} \
  //} \

#define MARK_GRAD(grad_name, grad_addr, grad_size) \
{ \
  float initial = 1.0; \
  dfsan_label i_label = dfsan_create_label(grad_name, initial); \
  dfsan_set_label(i_label, grad_addr,  grad_size); \
} \




#else

void init_datafile(char* name) {}
void close_datafile() {}
void print_grad_byte(char* name, unsigned char byte, unsigned long print_ind) {}
void print_grad_long(char* name, unsigned long val, unsigned long print_ind) {}
void print_grad_int(char* name, unsigned int val, unsigned long print_ind) {}

void print_grad_sint(char* name, int val, unsigned long print_ind) {}
void print_grad_sbyte(char* name, char val, unsigned long print_ind) {}

void print_grad_byte_arr(char* name, unsigned char* bytes, unsigned long len) {}


#endif

//#else	[> not (defined(DFSAN) || defined (GRSAN)) <]

//#define init_datafile(N)
//#define close_datafile()	
//#define mark_grad(N, A, S)	
//#define print_grad_byte(N, B, I)
//#define print_grad_long(N, V, I)
//#define print_grad_int(N, V, I)	
//#define print_grad_sint(N, V, I)
//#define print_grad_sbyte(N, V, I)	
//#define print_grad_byte_arr(N, B, L)

//#endif

#endif

