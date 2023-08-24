#ifndef MATRIX_H_
#define MATRIX_H_

#include <stdbool.h>
#include <wchar.h>

typedef struct Cascade {
    bool finished;
    int currentTick;
    int yPositionSet;
    int yPositionErased;
    wchar_t lastChar;
    int col;
    int speedTicks;
    int linelength;
    int maxYPosition;
} Cascade;

Cascade* cascade_init(int col, int row_amount);
void cascade_reset(Cascade* cascade, int col, int row_amount);
void cascade_destroy(Cascade* cascade);
void cascade_update(Cascade* cascade, int rows, wchar_t s, void (*f)(wchar_t, int, int, int));

#endif
