#define led 13
#include <Xbox_lib.h>


void setup();
void loop();

bool powerOn = 0;

int Lx, Ly, Rx, Ry;
Xbox xb4(Serial1);
