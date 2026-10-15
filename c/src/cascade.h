#ifndef CASCADE_H_
#define CASCADE_H_

#include <stdbool.h>
#include <wchar.h>

#include "color.h"

#define MAX_SPEED_TICKS 5

typedef struct Cascade {
    bool finished;
    int currentTick;
    int speedTicks;
    int speedTickCap;

    int yPositionSet;
    int yPositionErased;
    wchar_t lastChar;

    int col;
    int lineLength;
    int maxYPosition;
    int minYPosition;
    bool bottom_up;

    bool message_event;
    wchar_t* message_chars;
    int message_color_ansi;
    int message_r, message_g, message_b;
    bool message_use_rgb;
    int message_begin;
    int message_length;
    int message_index;
    int message_end;
} Cascade;

Cascade* cascade_init(int col, int rows, bool bottom_up);
void cascade_reset(Cascade* cascade, int col, int rows, bool bottom_up);
void cascade_destroy(Cascade* cascade);
void cascade_update(Cascade* cascade, int rows, wchar_t ch, void (*f)(wchar_t, int, int, Color, const char*));

#endif
