#include <stdlib.h>

#include "chars.h"

const int CHARS_LENGTH = 322;

Chars* chars_init() {
    Chars* chars = malloc(sizeof(Chars));
    chars->length = CHARS_LENGTH;
    chars->chars = malloc(CHARS_LENGTH * sizeof(unsigned int));

    int p = 0;
    for (unsigned int i = 48; i < 127; i++) {
        chars->chars[p++] = i;
    }
    for (unsigned int i = 910; i < 930; i++) {
        chars->chars[p++] = i;
    }
    for (unsigned int i = 931; i < 1024; i++) {
        chars->chars[p++] = i;
    }
    for (unsigned int i = 1024; i < 1154; i++) {
        chars->chars[p++] = i;
    }
    // for (unsigned int i = 12353; i < 12439; i++) {
    //     chars->chars[p++] = i;
    // }
    return chars;
}

void chars_destroy(Chars* chars) {
    free(chars->chars);
    chars->chars = NULL;
    free(chars);
    chars = NULL;
}
