#ifndef ARRAYLIST_H_
#define ARRAYLIST_H_

#include <stdio.h>
#include "cascade.h"

typedef struct ArrayList {
    Cascade** arr;
    int size;
    int capacity;
} ArrayList;

void al_init(ArrayList* l);
void al_destroy(ArrayList* l);
int al_append(ArrayList* l, Cascade* cascade);
int al_insert(ArrayList* l, int pos, Cascade* cascade);
void al_delete(ArrayList* l, int pos);
void al_print(FILE* f, const ArrayList* l);

#endif
