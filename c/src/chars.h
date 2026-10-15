#ifndef CHARS_H_
#define CHARS_H_

#include <stdlib.h>
#include <wchar.h>

typedef struct Chars {
    unsigned int* chars;
    int length;
} Chars;

Chars* chars_init(const wchar_t* extra_chars, int extra_len, int use_japanese);
void chars_destroy(Chars* chars);

#endif
