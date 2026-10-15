#include <stddef.h>
#include <stdbool.h>
#include <stdlib.h>
#include <wchar.h>
#include <string.h>
#include <time.h>

#include "cascade.h"

#include "message.h"
extern Message messages[MAX_MESSAGES];
extern int message_count;




#define MAX(i, j) (((i) > (j)) ? (i) : (j))
#define MIN(i, j) (((i) < (j)) ? (i) : (j))

static const int MINIMUM_LINE_LENGTH = 10;

extern double chance_for_dim;
extern double chance_for_italic;
extern Color color_main;
extern Color color_peak;

/* python's random() always yields [0.0, 1.0) */
static double random_unit(void) {
    return (double)rand() / ((double)RAND_MAX + 1.0);
}

static void build_style(char* buf, size_t size) {
    buf[0] = '\0';
    int has = 0;
    if (chance_for_dim > 0.0 && random_unit() < chance_for_dim) {
        has = 1;
        strncat(buf, "2;", size - strlen(buf) - 1);
    }
    if (chance_for_italic > 0.0 && random_unit() < chance_for_italic) {
        has = 1;
        strncat(buf, "3;", size - strlen(buf) - 1);
    }
    if (!has) {
        strncpy(buf, "0;", size);
    }
}

static int random_line_length(int rows) {
    int span = rows - MINIMUM_LINE_LENGTH + 1;
    if (span < 1) {
        /* the python version would raise on terminals this small */
        return MAX(1, rows);
    }
    int r = MINIMUM_LINE_LENGTH + rand() % span;
    if (r > rows) r = rows;
    return r;
}

/* message_color_ansi == -1 means "no explicit color" -> the main color is
   used, which keeps working while --rainbow is active
   (python: self.message_color or COLOR) */
static Color message_color(const Cascade* cascade) {
    Color color;
    if (cascade->message_use_rgb) {
        color.ansi = 0;
        color.r = cascade->message_r;
        color.g = cascade->message_g;
        color.b = cascade->message_b;
        color.use_rgb = true;
    } else if (cascade->message_color_ansi >= 0) {
        color.ansi = cascade->message_color_ansi;
        color.r = color.g = color.b = 0;
        color.use_rgb = false;
    } else {
        color = color_main;
    }
    return color;
}

Cascade* cascade_init(int col, int rows, bool bottom_up) {
    Cascade* cascade = malloc(sizeof(Cascade));
    cascade->message_chars = NULL;
    cascade->message_event = false;
    cascade_reset(cascade, col, rows, bottom_up);
    return cascade;
}

void cascade_reset(Cascade* cascade, int col, int rows, bool bottom_up) {
    cascade->finished = false;
    cascade->currentTick = 0;
    cascade->lastChar = L'\0';
    cascade->col = col;

    cascade->speedTicks = (rand() % MAX_SPEED_TICKS) + 1;
    cascade->speedTickCap = cascade->speedTicks;
    cascade->bottom_up = bottom_up;

    if (!bottom_up) {
        cascade->yPositionSet = 1;
        cascade->yPositionErased = 1;
        cascade->lineLength = random_line_length(rows);
        /* python: maxYPosition = min(rows, randrange(2 * rows)) */
        int my = rand() % (2 * rows);
        cascade->maxYPosition = MIN(rows, my);
        cascade->minYPosition = 1;
    } else {
        cascade->yPositionSet = rows;
        cascade->yPositionErased = rows;
        cascade->lineLength = random_line_length(rows);
        /* python: minYPosition = max(1, rows - randrange(2 * rows)) */
        int minY = rows - (rand() % (2 * rows));
        if (minY < 1) minY = 1;
        cascade->minYPosition = minY;
        cascade->maxYPosition = rows;
    }

    if (cascade->message_chars) {
        free(cascade->message_chars);
        cascade->message_chars = NULL;
    }
    cascade->message_event = false;
    cascade->message_color_ansi = -1;
    cascade->message_use_rgb = false;
    cascade->message_begin = 1;
    cascade->message_length = 0;
    cascade->message_index = 0;
    cascade->message_end = 0;

    for (int mi = 0; mi < message_count; mi++) {
        Message* msg = &messages[mi];
        bool has_space;
        if (!bottom_up) {
            /* python: self.maxYPosition > len(message) + 1 */
            has_space = cascade->maxYPosition > msg->len + 1;
        } else {
            /* python: available_len = rows - self.minYPosition + 1 > len(message) + 1 */
            has_space = (rows - cascade->minYPosition + 1) > msg->len + 1;
        }
        /* python evaluates the space check before the chance roll */
        if (!has_space || random_unit() >= msg->chance) {
            continue;
        }
        cascade->message_event = true;
        cascade->message_length = msg->len;
        cascade->message_chars = malloc((cascade->message_length + 1) * sizeof(wchar_t));
        if (!cascade->message_chars) {
            cascade->message_event = false;
            break;
        }
        if (bottom_up) {
            /* python pops the message chars from the back for bottom-up cascades */
            for (int k = 0; k < cascade->message_length; k++) {
                cascade->message_chars[k] = msg->text[cascade->message_length - 1 - k];
            }
        } else {
            for (int k = 0; k < cascade->message_length; k++) {
                cascade->message_chars[k] = msg->text[k];
            }
        }
        if (!bottom_up) {
            /* python: message_begin = randrange(1, maxYPosition - len(message) + 2) */
            cascade->message_begin = 1 + rand() % (cascade->maxYPosition - cascade->message_length + 1);
        } else {
            /* python: message_begin = randrange(minYPosition + len(message) - 1, rows) */
            int begin = cascade->minYPosition + cascade->message_length - 1;
            cascade->message_begin = begin + rand() % (rows - begin);
        }
        if (cascade->message_begin < 1) cascade->message_begin = 1;
        cascade->message_index = 0;
        cascade->message_color_ansi = msg->color_ansi;
        cascade->message_r = msg->r;
        cascade->message_g = msg->g;
        cascade->message_b = msg->b;
        cascade->message_use_rgb = msg->use_rgb;
        break;
    }
}

void cascade_destroy(Cascade* cascade) {
    if (cascade->message_chars) {
        free(cascade->message_chars);
        cascade->message_chars = NULL;
    }
    free(cascade);
}

void cascade_update(Cascade* cascade, int rows, wchar_t ch, void (*f)(wchar_t, int, int, Color, const char*)) {
    cascade->currentTick = (cascade->currentTick % cascade->speedTickCap) + 1;
    char style[32];

    if (!cascade->bottom_up) {
        if (cascade->currentTick == cascade->speedTicks) {
            if (cascade->yPositionSet <= cascade->maxYPosition) {
                build_style(style, sizeof(style));
                if (cascade->message_event && cascade->message_index < cascade->message_length &&
                    cascade->yPositionSet >= cascade->message_begin &&
                    cascade->yPositionSet < cascade->message_begin + cascade->message_length) {
                    cascade->lastChar = cascade->message_chars[cascade->message_index++];
                    f(cascade->lastChar, cascade->col, cascade->yPositionSet - 1, message_color(cascade), style);
                } else {
                    f(cascade->lastChar, cascade->col, cascade->yPositionSet - 1, color_main, style);
                }
                cascade->lastChar = ch;
                f(cascade->lastChar, cascade->col, cascade->yPositionSet, color_peak, "");
            } else if (cascade->yPositionSet - 1 == cascade->maxYPosition && cascade->maxYPosition >= rows) {
                build_style(style, sizeof(style));
                f(cascade->lastChar, cascade->col, cascade->yPositionSet - 1, color_main, style);
            }
            if (cascade->yPositionSet > cascade->lineLength) {
                f(L' ', cascade->col, cascade->yPositionErased - 1, (Color){30, 0, 0, 0, false}, "");
                cascade->yPositionErased++;
            }
            cascade->finished = (cascade->yPositionErased > cascade->maxYPosition + 1);
            cascade->yPositionSet++;
        } else if (cascade->yPositionSet <= cascade->maxYPosition) {
            cascade->lastChar = ch;
            f(cascade->lastChar, cascade->col, cascade->yPositionSet - 1, color_peak, "");
        }
    } else {
        if (cascade->currentTick == cascade->speedTicks) {
            if (cascade->yPositionSet >= cascade->minYPosition) {
                build_style(style, sizeof(style));
                if (cascade->message_event && cascade->message_index < cascade->message_length &&
                    cascade->yPositionSet <= cascade->message_begin &&
                    cascade->yPositionSet > cascade->message_begin - cascade->message_length) {
                    cascade->lastChar = cascade->message_chars[cascade->message_index++];
                    f(cascade->lastChar, cascade->col, cascade->yPositionSet + 1, message_color(cascade), style);
                } else {
                    f(cascade->lastChar, cascade->col, cascade->yPositionSet + 1, color_main, style);
                }
                cascade->lastChar = ch;
                f(cascade->lastChar, cascade->col, cascade->yPositionSet, color_peak, "");
            } else if (cascade->yPositionSet + 1 == cascade->minYPosition && cascade->minYPosition <= 1) {
                build_style(style, sizeof(style));
                f(cascade->lastChar, cascade->col, cascade->yPositionSet + 1, color_main, style);
            }
            if (cascade->yPositionSet < rows - cascade->lineLength + 1) {
                f(L' ', cascade->col, cascade->yPositionErased + 1, (Color){30, 0, 0, 0, false}, "");
                cascade->yPositionErased--;
            }
            cascade->finished = (cascade->yPositionErased < cascade->minYPosition - 1);
            cascade->yPositionSet--;
        } else if (cascade->yPositionSet >= cascade->minYPosition) {
            cascade->lastChar = ch;
            f(cascade->lastChar, cascade->col, cascade->yPositionSet + 1, color_peak, "");
        }
    }
}
