/**
 * Copyright (c) 2018 emekoi
 *
 * This library is free software; you can redistribute it and/or modify it
 * under the terms of the MIT license. See LICENSE for details.
 */

#include <stdio.h>
#define _USE_MATH_DEFINES 
#include <math.h>
#include "value.h"

int main(int argc, char const *argv[]) {
  #if _WIN32
  setvbuf(stdout, NULL, _IONBF, BUFSIZ);
  #endif
  
  List *listptr = calloc(1, sizeof(List));
  listptr->head = NUM_VAL(M_PI);
  listptr->tail = NUM_VAL(M_PI_2);

  Value list = LIST_VAL(listptr);

  printf("%d %d\n", IS_NUM(listptr->head), IS_LIST(list));
  printf("%f %f\n", AS_NUM(AS_LIST(list)->head), AS_NUM(AS_LIST(list)->tail));
  listptr->tail = NUM_VAL(M_PI);
  printf("%f %f\n", AS_NUM(AS_LIST(list)->head), AS_NUM(AS_LIST(list)->tail));


  return 0;
}
