#ifndef __CODE_H__
#define __CODE_H__


typedef struct line_code{
    char* mnemonic;
    float argument;
} line_code;


int count_lines(char* text);
void fill_array(line_code array[], char* code);

#endif
