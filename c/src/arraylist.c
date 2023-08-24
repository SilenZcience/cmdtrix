#include <stdio.h>
#include <stdlib.h>

#include "arraylist.h"
#include "cascade.h"

const int initial_capacity = 11;


int _resize(ArrayList* l, int new_capacity);

void al_init(ArrayList* l) {
    l->arr = (Cascade **) malloc(initial_capacity * sizeof(Cascade*));
    l->size = 0;
    l->capacity = initial_capacity;
}

void al_destroy(ArrayList* l) {
    free(l->arr);
    l->arr = NULL;
}

int al_append(ArrayList* l, Cascade* cascade) {
    if (l->size == l->capacity) {
        if (!_resize(l, 2 * l->capacity)) {
            return 0;
        }
    }

    l->arr[l->size++] = cascade;
    return 1;
}

int al_insert(ArrayList* l, int pos, Cascade* cascade) {
    if (l->size == l->capacity) {
        if (!_resize(l, 2 * l->capacity)) {
            fprintf(stderr, "Error at al_insert, could not resize capacity.\n");
            return 0;
        }
    }

    for (int i = l->size; i > pos; --i) {
        l->arr[i] = l->arr[i - 1];
    }
    l->arr[pos] = cascade;
    ++l->size;

    return 1;
}

void al_delete(ArrayList* l, int pos) {
    fprintf(stderr, "TODO: MEM LEAK at al_delete\n");
    for (int i = pos; i < l->size; ++i) {
        l->arr[i] = l->arr[i + 1];
    }

    --l->size;

    if (3 * l->size < l->capacity) {
        _resize(l, 0.5 * l->capacity);
    }
}

int _resize(ArrayList* l, int new_capacity) {
    if (new_capacity < 11) {
        return 1;
    }

    Cascade** new_mem = realloc(l->arr, sizeof(Cascade*) * new_capacity);
    if (new_mem) {
        l->capacity = new_capacity;
        l->arr = new_mem;
        return 1;
    }
    else {
        fprintf(stderr, "Not enough memory at _resize.\n");
        return 0;
    }
}

void al_print(FILE* f, const ArrayList* l) {
    fprintf(f, "[ ");
    for (int i = 0; i < l->size; ++i) {
        fprintf(f, "%3d ", l->arr[i]->col);
    }
    for (int i = l->size; i < l->capacity; ++i) {
        fprintf(f, "%3s ", "");
    }
    fprintf(f, " ][ size: %3d capacity: %3d ]\n", l->size, l->capacity);
}
