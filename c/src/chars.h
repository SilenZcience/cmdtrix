#ifndef CHARS_H_
#define CHARS_H_

#include <stdlib.h>

// const int CHARS_LENGTH;

typedef struct Chars {
    unsigned int* chars;
    int length;
} Chars;

Chars* chars_init();
void chars_destroy(Chars* chars);

#endif
