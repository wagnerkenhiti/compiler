#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "modules/code/code.h"
#include "modules/file/file.h"
int main(){

    char* code = open_content_file("../object_code.txt");
    int lines = count_lines(code);

    line_code C_array[lines];

    fill_array(C_array, code);

    int register_i = 0;
    while(register_i <= lines-1){
        int register_s;
        float D_array[lines*2];
        if (strcmp(C_array[register_i].mnemonic, "CRCT") == 0){
            register_s++;
            D_array[register_s] = C_array[register_i].argument;
        }
        else if(strcmp(C_array[register_i].mnemonic, "CRVL") == 0){
            register_s++;
            D_array[register_s] = D_array[(int)C_array[register_i].argument];
        }
        else if(strcmp(C_array[register_i].mnemonic, "SOMA") == 0){
            if(register_s>=1){
                D_array[register_s-1] = D_array[register_s-1] + D_array[register_s];
                register_s--;
            }
            else {
                printf("ERROR: %s \nNot enough elements.\n",C_array[register_i].mnemonic);
                register_i = lines*2;
                break;
            }
        }
        else if(strcmp(C_array[register_i].mnemonic, "SUBT") == 0){
            if(register_s>=1){
                D_array[register_s-1] = D_array[register_s-1] - D_array[register_s];
                register_s--;
            }
            else {
                printf("ERROR: %s \nNot enough elements.\n",C_array[register_i].mnemonic);
                register_i = lines*2;
                break;
            }
        }
        else if(strcmp(C_array[register_i].mnemonic, "MULT") == 0){
            if(register_s>=1){
                D_array[register_s-1] = D_array[register_s-1] * D_array[register_s];
                register_s--;
            }
            else {
                printf("ERROR: %s \nNot enough elements.\n",C_array[register_i].mnemonic);
                register_i = lines*2;
                break;
            }
        }
        else if(strcmp(C_array[register_i].mnemonic, "DIVI") == 0){
            if(register_s>=1){
                D_array[register_s-1] = D_array[register_s-1] / D_array[register_s];
                register_s--;
            }
            else {
                printf("ERROR: %s \nNot enough elements.\n",C_array[register_i].mnemonic);
                register_i = lines*2;
                break;
            }
        }
        else if(strcmp(C_array[register_i].mnemonic, "INVE") == 0){
            D_array[register_s] =(-1)*D_array[register_s];
        }
        else if(strcmp(C_array[register_i].mnemonic, "CONJ") == 0){
            if(register_s>=1){
                if((D_array[register_s-1] == (float)0 || D_array[register_s-1] == (float)1) && (D_array[register_s] == (float)0 || D_array[register_s] == (float)1)){
                    D_array[register_s-1] = (D_array[register_s-1] == 1 && D_array[register_s] == 1) ? 1 : 0;
                    register_s--;
                }
                else {
                    printf("ERROR: %s \nWrongly typed elements.\n",C_array[register_i].mnemonic);
                    break;
                }
            }
            else {
                printf("ERROR: %s \nNot enough elements.\n",C_array[register_i].mnemonic);
                register_i = lines*2;
                break;
            }
        }
        else if(strcmp(C_array[register_i].mnemonic, "DISJ") == 0){
            if(register_s>=1){
                if((D_array[register_s-1] == (float)0 || D_array[register_s-1] == (float)1) && (D_array[register_s] == (float)0 || D_array[register_s] == (float)1)){
                    D_array[register_s-1] = (D_array[register_s-1] == 1 || D_array[register_s] == 1) ? 1 : 0;
                    register_s--;
                }
                else {
                    printf("ERROR: %s \nWrongly typed elements.\n",C_array[register_i].mnemonic);
                    break;
                }
            }
            else {
                printf("ERROR: %s \nNot enough elements.\n",C_array[register_i].mnemonic);
                register_i = lines*2;
                break;
            }
        }
        else if(strcmp(C_array[register_i].mnemonic, "NEGA") == 0){
            if(D_array[register_s] == (float)0 || D_array[register_s] == (float)1){
                D_array[register_s] = (D_array[register_s] == 1) ? 0 : 1;
            }
            else {
                printf("ERROR: %s \nNot enough elements.\n",C_array[register_i].mnemonic);
                register_i = lines*2;
                break;
            }
        }
        else if(strcmp(C_array[register_i].mnemonic, "CPME") == 0){
            if(register_s>=1){
               D_array[register_s-1] = (D_array[register_s-1] < D_array[register_s]) ? 1 : 0;
               register_s--;
            }
            else {
                printf("ERROR: %s \nNot enough elements.\n",C_array[register_i].mnemonic);
                register_i = lines*2;
                break;
            }
        }
        else if(strcmp(C_array[register_i].mnemonic, "CPMA") == 0){
            if(register_s>=1){
               D_array[register_s-1] = (D_array[register_s-1] > D_array[register_s]) ? 1 : 0;
               register_s--;
            }
            else {
                printf("ERROR: %s \nNot enough elements.\n",C_array[register_i].mnemonic);
                register_i = lines*2;
                break;
            }
        }
        else if(strcmp(C_array[register_i].mnemonic, "CPIG") == 0){
            if(register_s>=1){
               D_array[register_s-1] = (D_array[register_s-1] == D_array[register_s]) ? 1 : 0;
               register_s--;
            }
            else {
                printf("ERROR: %s \nNot enough elements.\n",C_array[register_i].mnemonic);
                register_i = lines*2;
                break;
            }
        }
        else if(strcmp(C_array[register_i].mnemonic, "CPES") == 0){
            if(register_s>=1){
               D_array[register_s-1] = (D_array[register_s-1] != D_array[register_s]) ? 1 : 0;
               register_s--;
            }
            else {
                printf("ERROR: %s \nNot enough elements.\n",C_array[register_i].mnemonic);
                register_i = lines*2;
                break;
            }
        }
        else if(strcmp(C_array[register_i].mnemonic, "CPMI") == 0){
            if(register_s>=1){
               D_array[register_s-1] = (D_array[register_s-1] <= D_array[register_s]) ? 1 : 0;
               register_s--;
            }
            else {
                printf("ERROR: %s \nNot enough elements.\n",C_array[register_i].mnemonic);
                register_i = lines*2;
                break;
            }
        }
        else if(strcmp(C_array[register_i].mnemonic, "CMAI") == 0){
            if(register_s>=1){
                D_array[register_s-1] = (D_array[register_s-1] >= D_array[register_s]) ? 1 : 0;

                register_s--;
            }
            else {
                printf("ERROR: %s \nNot enough elements.\n",C_array[register_i].mnemonic);
                register_i = lines*2;
                break;
            }
        }
        else if(strcmp(C_array[register_i].mnemonic, "ARMZ") == 0){
            if (register_s < (int)C_array[register_i].argument){
                printf("ERROR: %s \nNot enough elements.\n",C_array[register_i].mnemonic);
                register_i = lines*2;
                break;
            }
            D_array[(int)C_array[register_i].argument] = D_array[register_s];
            register_s--;
        }
        else if(strcmp(C_array[register_i].mnemonic, "DSVI") == 0){
            if (lines < (int)C_array[register_i].argument){
                printf("ERROR: %s \nNot enough elements.\n",C_array[register_i].mnemonic);
                register_i = lines*2;
                break;
            }
            register_i = (int)C_array[register_i].argument;
        }
        else if(strcmp(C_array[register_i].mnemonic, "DSVF") == 0){
            if (lines < (int)C_array[register_i].argument){
                printf("ERROR: %s \nNot enough elements.\n",C_array[register_i].mnemonic);
                register_i = lines*2;
                break;
            }
            if(D_array[register_s]==0) register_i = (int)C_array[register_i].argument;
            register_s--;
        }
        else if(strcmp(C_array[register_i].mnemonic, "LEIT") == 0){
            float input;
            printf("Input value: ");
            scanf(" %f",&input);
            register_s++;
            D_array[register_s] = input;
        }
        else if(strcmp(C_array[register_i].mnemonic, "IMPR") == 0){
            printf("Printed value: %f\n",D_array[register_s]);
            register_s--;
        }
        else if(strcmp(C_array[register_i].mnemonic, "ALME") == 0){
            register_s = register_s + (int)C_array[register_i].argument;

        }
        else if(strcmp(C_array[register_i].mnemonic, "INPP") == 0){
            register_s = -1;
            printf("Starting...\n");
        }
        else if(strcmp(C_array[register_i].mnemonic, "PARA")){
            printf("\nFinished!");
        }
        register_i++;
    }


    if(register_i == lines*2) printf("Fix the object code!\n");


    for(int i =0;i<lines;i++){
        free(C_array[i].mnemonic);
    }

    return 0;
}
