#ifndef __FILE_H__
#define  __FILE_H__
#include <stdio.h>
int lenght_file(FILE* pointer);
FILE* open_file(char* name);
void close_file(FILE* file);

// Get the content of a file and close it.
char* open_content_file(char* nome);


#endif
