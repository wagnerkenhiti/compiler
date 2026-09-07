#include "file.h"
#include <stdlib.h>
int lenght_file(FILE* pointer){
    if (pointer!=NULL){
        fseek(pointer,0,SEEK_END);
        int length = ftell(pointer);
        rewind(pointer);
        return length;
    }
    else{
        return -1;
    }
}

FILE* open_file(char* name){
    FILE* file = fopen(name,"r");
    if (file!=NULL) return file;
    else return NULL;
}

void close_file(FILE* file){
    if (file != NULL) fclose(file);
}



char* open_content_file(char* name){
    FILE* file=open_file(name);
    if (file==NULL) return NULL;
    int lenght=lenght_file(file);

    char* text = malloc(sizeof(char)*lenght+1);

    fread(text,1,lenght,file);

    text[lenght]='\0';

    close_file(file);
    return text;
}
