#include <stdio.h>
#include <signal.h>
#include <wchar.h>
#include <locale.h>
#include <stdlib.h>
#include <stdbool.h>
#include <sys/ioctl.h>

#include "chars.h"
#include "arraylist.h"
#include "cascade.h"
#include "delay.h"

struct winsize w;
bool running = true;

void sigint_handler(int signum) {
    running = false;
}

void init() {
    fprintf(stdout, "\x1b[?25l\x1b[2J"); //hide cursor, clear screen
    fflush(stdout);
}

void deinit() {
    fprintf(stdout, "\x1b[m\x1b[2J\x1b[?25h"); //reset attributes, clear screen, show cursor
    fflush(stdout);
    system("clear");
}

void printAtPosition(wchar_t s, int x, int y, int color) {
    fprintf(stdout, "\x1b[%dm\x1b[%d;%df%lc", color, y, x, s);
    fflush(stdout);
}

void addCascade(ArrayList* al) {
    Cascade* c = cascade_init(rand() % (w.ws_col + 1), w.ws_row);
    al_append(al, c);
}

void destroyCascades(ArrayList* al) {
    for (int i = 0; i < al->size; i++) {
        cascade_destroy(al->arr[i]);
    }
}

void updateCascades(ArrayList* al, Chars* chars) {
    for (int i = 0; i < al->size; i++) {
        cascade_update(al->arr[i], w.ws_row, chars->chars[rand() % chars->length], printAtPosition);
        
        if (al->arr[i]->finished) {
            cascade_reset(al->arr[i], rand() % (w.ws_col + 1), w.ws_row);
        }
    }
}

int main(void) {
    // handle interrupt-event
    signal(SIGINT, sigint_handler);

    // setup
    setlocale(LC_ALL, "");
    
    ioctl(0, TIOCGWINSZ, &w);

    Chars* chars = chars_init();
    
    ArrayList al;
    al_init(&al);
    for (int i = 0; i < w.ws_col; i++) {
        addCascade(&al);
    }
    
    init();

    //main loop (exit via (keyboard) interupt)
    while (running) {
        msleep(25);
        updateCascades(&al, chars);
    }

    //cleanup
    deinit();

    destroyCascades(&al);
    al_destroy(&al);

    chars_destroy(chars);

    return 0;
}
