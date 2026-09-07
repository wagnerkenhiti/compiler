all: backend

backend: code.o file.o main.o 
	gcc -o main bin/main.o bin/code.o bin/file.o 

code.o: modules/code/code.c
	gcc -o bin/code.o -c modules/code/code.c 

file.o: modules/file/file.c
	gcc -o bin/file.o -c modules/file/file.c

main.o: main.c
	gcc -o bin/main.o -c main.c

clean: 
	rm -rf bin/*.o

mrproper: clean
	rm -f backend
