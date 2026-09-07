#include <stdio.h>
#include "modules/code/code.h"
#include "modules/file/file.h"
int main(){

    char* code = open_content_file("../object_code.txt");

    // printf("%s",code);

    int lines = count_lines(code);


    line_code struct_code[lines];


    fill_array(struct_code, code);
    int i = 0;
    while(i != lines-1){




        i++;
    }

    printf("Programa finalizado!");

    return 0;
}
