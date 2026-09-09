#include "code.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
int count_lines(char* text){
    if (text == NULL || strlen(text) == 0) return -1;
    int i=0, lines=0;
    while (i < strlen(text)){
        if (text[i] == '\n') lines++;
        i++;
    }
    return lines;
}

void fill_array(line_code array[], char* code){
    int i =0, array_i = 0;
    int lines = count_lines(code);

    for (int k=0;k<lines;k++){
        array[k].argument=-1;
        array[k].mnemonic=NULL;
    }
        while (code[i]!='\0' && array_i < lines){
            if(code[i]=='\n') array_i++;
            if((code[i] >= 'A' && code[i] <= 'Z' || code[i] >= 'a' && code[i] <= 'z') && i < strlen(code)){
                char buffer[5];
                for(int j=0; j < 4; j++,i++){
                    buffer[j]=code[i];
                }
                buffer[4] = '\0';
                char* buffer_mal = malloc((strlen(buffer)+1)*sizeof(char));
                strcpy(buffer_mal,buffer);
                array[array_i].mnemonic = buffer_mal;
            }
            else if ((code[i] >= '0' && code[i] <= '9') || code[i] == '-' || code[i] == '.') {
                double value = 0.0;
                int sign = 1;

                if (code[i] == '-') {
                    sign = -1;
                    i++;
                }

                while (code[i] >= '0' && code[i] <= '9' && i < strlen(code)) {
                    value = value * 10.0 + (code[i] - '0');
                    i++;
                }

                if (code[i] == '.') {
                    i++;
                    double divisor = 10.0;

                    while (code[i] >= '0' && code[i] <= '9' && code[i] != '\0') {
                        value = value + (code[i] - '0') / divisor;
                        divisor *= 10.0;
                        i++;
                    }
                }

                value *= sign;

                array[array_i].argument = value;
            }
            else{
                i++;
            }


            }

}
