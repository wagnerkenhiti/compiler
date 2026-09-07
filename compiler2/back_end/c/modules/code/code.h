#ifndef __CODE_H__
#define __CODE_H__

typedef struct arguments{
    int argument;
    struct arguments* nextArgument;
} arguments;

typedef struct line_code{
    char* mnemonic;
    arguments* argument;
} line_code;


int count_lines(char* text);
void fill_array(line_code array[], char* code);

#endif
