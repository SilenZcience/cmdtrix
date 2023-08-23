#ifndef CA_ARRAYLIST_H_
#define CA_ARRAYLIST_H_

#include <stdio.h>

#include "cascade.h"

typedef struct ArrayList {
  Cascade** arr;      // eigentliche Liste
  int size;      // #Elemente in Liste
  int capacity;  // Größe von arr
} ArrayList;

/* Konstruktur; initialisiert l als leere Liste
 * mit einem Array der Größe initial_capacity.*/
void al_init(ArrayList* l);

/* Destruktor; gibt sämtlichen von der Arrayliste
 * dynamisch allokierten Speicher wieder frei */
void al_destroy(ArrayList* l);

/* Hängt den Schlüssel key an das Ende der
 * Arrayliste an. Wenn die aktuelle Kapazität
 * der Arrayliste nicht ausreicht, wird die Kapazität
 * der Arrayliste verdoppelt. */
int al_append(ArrayList* l, Cascade* cascade);

/* Fügt den Schlüssel key an Position pos ein.
 * Schiebt dazu die Elemente l->arr[pos,...,l->size-1]
 * um eine Position nach rechts. Wenn die aktuelle
 * Kapazität der Arrayliste nicht ausreicht,
 * wird die Kapazität der Arrayliste verdoppelt.
 *
 * Wenn pos == l->size ist die Funktion äquivalent
 * zu al_append. Es muss 0 <= pos <= l->size gelten.
 */
int al_insert(ArrayList* l, int pos, Cascade* cascade);

/* Löscht den Schlüssel an Position pos und
 * schiebt die Elemente l->arr[pos+1,...,l->size-1]
 * um eine Position nach links. Falls nach der
 * Operation die Kapazität mehr als dreimal so groß
 * wie die Anzahl der Elemente in der Liste ist,
 * wird die Kapazität der Liste halbiert.
 * Die Kapazität der Liste wird niemals unter 11
 * reduziert. Es muss 0 <= pos < l->size gelten.
 */
void al_delete(ArrayList* l, int pos);

/* Gibt die Liste in die Datei f aus */
void al_print(FILE* f, const ArrayList* l);

#endif
