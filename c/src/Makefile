CC=gcc
CFLAGS=-Wall -Werror -g
OBJECTS=chars.o cascade.o delay.o arraylist.o main.o
BIN=cmdtrix

all: ${BIN}

arraylist.o: arraylist.h arraylist.c cascade.h
chars.o: chars.c chars.h
cascade.o: cascade.c cascade.h
delay.o: delay.c delay.h

${BIN}: ${OBJECTS}
	${CC} ${CFLAGS} -o ${BIN} ${OBJECTS}

clean:
	rm -f ${BIN}
	rm -f ${OBJECTS}

.PHONY: clean all
