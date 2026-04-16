#include <stdio.h>
#include <string.h>
#define LENTOKENS 50
#define LENID 50

typedef struct token{
    char lexeme[LENID], type[20];
} token;

void print_token_array(token tokens[], int len){
    for(int i=0;i<len;i++){
        printf("(%s,%s), ",tokens[i].lexeme,tokens[i].type);
    }
}

int main(){
    
    char *operation= "a+b \n b   +   c \n value1*value2";
    int i=0;
    int l=0;
    token tokens[LENTOKENS];
    while(i<strlen(operation)){
        if(operation[i] >= 'a' && operation[i] <= 'z' || operation[i] >= 'A' && operation[i] <= 'Z'){
            char idname[LENID];
            int k=0;
            while(i<strlen(operation) && (operation[i] >= 'a' && operation[i] <= 'z' || operation[i] >= 'A' && operation[i] <= 'Z' || operation[i] >= '0' && operation[i] <= '9')){
                idname[k++]=operation[i++];
            }
            token aux;
            strcpy(aux.lexeme, idname);
            strcpy(aux.type,"IDENTIFIER");
            tokens[l++]=aux;
        }
        else if (operation[i] == '+' || operation[i] == '-' || operation[i] == '*' || operation[i] == '/'){
            token aux;
            char operator[2];
            operator[0]=operation[i++];
            operator[1]='\0';
            strcpy(aux.lexeme,operator);
            strcpy(aux.type,"OPERATOR");
            tokens[l++]=aux;
        } 
        else i++;
    }
    print_token_array(tokens,l);

    return 0;
} 