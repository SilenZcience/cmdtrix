#ifndef MESSAGE_H
#define MESSAGE_H

#include <stdbool.h>
#include <wchar.h>

typedef struct Message {
    wchar_t *text;
    int len;
    double chance;
    int color_ansi;
    int r, g, b;
    bool use_rgb;
} Message;

#define MAX_MESSAGES 32

#endif
