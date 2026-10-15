#include <stdlib.h>

#include "chars.h"

const int CHARS_LENGTH_JAPANESE = 55;

typedef struct CharRange {
    unsigned int start;
    unsigned int end; /* exclusive */
} CharRange;

/* exactly the same ranges as the python charList (cmdtrix/util/Chars.py) */
static const CharRange BASIC_RANGES[] = {
    {   48,  127 }, /* basic latin */
    {  910,  930 }, {  931,  994 }, {  996, 1018 }, { 1020, 1024 }, /* greek */
    { 1024, 1120 }, { 1122, 1124 }, { 1134, 1136 }, { 1152, 1154 }, /* cyrillic */
    { 8705, 8709 }, { 8710, 8731 }, { 8734, 8748 }, { 8750, 8751 }, /* math operators */
    { 8753, 8810 }, { 8812, 8853 }, { 8876, 8920 }, { 8922, 8942 },
    { 8946, 8960 },
};

#define BASIC_RANGE_COUNT ((int)(sizeof(BASIC_RANGES) / sizeof(BASIC_RANGES[0])))

static int basic_length(void) {
    int length = 0;
    for (int i = 0; i < BASIC_RANGE_COUNT; i++) {
        length += (int)(BASIC_RANGES[i].end - BASIC_RANGES[i].start);
    }
    return length;
}

Chars* chars_init(const wchar_t* extra_chars, int extra_len, int use_japanese) {
    Chars* chars = malloc(sizeof(Chars));
    int p = 0;

    if (use_japanese) {
        chars->length = CHARS_LENGTH_JAPANESE;
        chars->chars = malloc(chars->length * sizeof(unsigned int));
        for (unsigned int i = 65382; i < 65437; i++) {
            chars->chars[p++] = i;
        }
    } else if (extra_len > 0) {
        /* custom symbols replace the default char list (like python's -S) */
        chars->length = extra_len;
        chars->chars = malloc(chars->length * sizeof(unsigned int));
        for (int i = 0; i < extra_len; i++) {
            chars->chars[p++] = (unsigned int)extra_chars[i];
        }
    } else {
        chars->length = basic_length();
        chars->chars = malloc(chars->length * sizeof(unsigned int));
        for (int i = 0; i < BASIC_RANGE_COUNT; i++) {
            for (unsigned int c = BASIC_RANGES[i].start; c < BASIC_RANGES[i].end; c++) {
                chars->chars[p++] = c;
            }
        }
    }

    return chars;
}

void chars_destroy(Chars* chars) {
    free(chars->chars);
    chars->chars = NULL;
    free(chars);
}
