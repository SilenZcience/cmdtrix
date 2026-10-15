CC=gcc
CFLAGS=-Wall -Werror -g -std=c99
OBJECTS=chars.o cascade.o delay.o arraylist.o main.o
BIN=cmdtrix

all: ${BIN}

arraylist.o: arraylist.h arraylist.c cascade.h color.h
chars.o: chars.c chars.h
cascade.o: cascade.c cascade.h color.h message.h
delay.o: delay.c delay.h
main.o: main.c chars.h arraylist.h cascade.h delay.h color.h message.h

${BIN}: ${OBJECTS}
	${CC} ${CFLAGS} -o ${BIN} ${OBJECTS} -lm

clean:
	rm -f ${BIN}
	rm -f ${OBJECTS}

.PHONY: clean all
