#ifndef COLOR_H_
#define COLOR_H_

#include <stdbool.h>

typedef struct Color {
    int ansi;       /* foreground ANSI code (30-37), used when use_rgb is false */
    int r, g, b;    /* 24-bit color, used when use_rgb is true */
    bool use_rgb;
} Color;

#endif
