#include <stdbool.h>
#include <stdlib.h>
#include <wchar.h>

#include "cascade.h"

#define MAX(i, j) (((i) > (j)) ? (i) : (j))
#define MIN(i, j) (((i) < (j)) ? (i) : (j))

const int MAX_SPEED_TICKS = 5;
const int MINIMUM_LINE_LENGTH = 10;


Cascade* cascade_init(int col, int row_amount) {
    Cascade* cascade = malloc(sizeof(Cascade));
    cascade_reset(cascade, col, row_amount);

    return cascade;
}

void cascade_reset(Cascade* cascade, int col, int row_amount) {
    cascade->finished = false;
    cascade->currentTick = 0;
    cascade->yPositionSet = 1;
    cascade->yPositionErased = 1;
    cascade->lastChar = ' ';
    cascade->col = col;
    cascade->speedTicks = rand() % MAX_SPEED_TICKS + 1;
    int randrow = rand() & row_amount;
    cascade->linelength = MAX(MINIMUM_LINE_LENGTH, randrow);
    randrow = rand() % (2 * row_amount);
    cascade->maxYPosition = MIN(row_amount, randrow);
}

void cascade_destroy(Cascade* cascade) {
    free(cascade);
    cascade = NULL;
}

void cascade_update(Cascade* cascade, int rows, wchar_t wchar, void (*f)(wchar_t, int, int, int)) {
    cascade->currentTick = cascade->currentTick % cascade->speedTicks + 1;

    if (cascade->currentTick == cascade->speedTicks) {
        if (cascade->yPositionSet <= cascade->maxYPosition) {
            f(cascade->lastChar, cascade->col, cascade->yPositionSet-1, 32);
            cascade->lastChar = wchar;
            f(cascade->lastChar, cascade->col, cascade->yPositionSet, 37);
        }
        else if (cascade->yPositionSet-1 == cascade->maxYPosition && cascade->maxYPosition >= rows) {
            f(cascade->lastChar, cascade->col, cascade->yPositionSet-1, 32);
        }
        if (cascade->yPositionSet > cascade->linelength) {
            f(' ', cascade->col, cascade->yPositionErased, 30);
            cascade->yPositionErased++;
        }
        cascade->finished = (cascade->yPositionErased > cascade->maxYPosition);
        cascade->yPositionSet++;
    }
    else if (cascade->yPositionSet <= cascade->maxYPosition) {
        cascade->lastChar = wchar;
        f(cascade->lastChar, cascade->col, cascade->yPositionSet-1, 37);
    }
}
