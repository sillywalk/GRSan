#include <sanitizer/dfsan_interface.h>
#include <stdio.h>
#include <assert.h>

char dfsan_file_buff[4096*4096];
int main(void) {

  FILE *infile;  // TODO: try to raise to global scope
   
  char * filename = "sample.txt";
  if ((infile = fopen(filename, "rb")) == NULL) {
    fprintf(stderr, "can't open %s\n", filename);
    return 1;
  }
  int rc = setvbuf(infile, dfsan_file_buff, _IOFBF, sizeof(dfsan_file_buff));
  printf("%d\n", rc);
  int mark_ind = 2;
  float init_deriv = 1.0;
  dfsan_label i_label = dfsan_create_label("file_labeled", init_deriv);
  dfsan_set_label(i_label, &dfsan_file_buff[mark_ind], sizeof(char));
  int var = -1;
  int file_byte = -1;

  for (int i = 0; i < 15; i++) {
      file_byte = getc(infile);
//      fread(&file_byte, 1, 1, infile);
      printf("%c\n", file_byte);
        dfsan_label i_label = dfsan_get_label(file_byte);
        const struct dfsan_label_info* i_info = dfsan_get_label_info(i_label);
        printf("i label %d: %f %s\n",i_label, i_info->neg_dydx, i_info->desc);
      if (i == mark_ind) {
      }
      file_byte = dfsan_file_buff[i];
        i_label = dfsan_get_label(file_byte);
        i_info = dfsan_get_label_info(i_label);
        printf("i label %d: %f %s\n",i_label, i_info->neg_dydx, i_info->desc);
  }
  printf("%s\n", dfsan_file_buff);
//  fclose(infile); I don't think this is needed. 
   
  return 0;
}
