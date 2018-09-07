/**
 * Copyright (c) 2018 emekoi
 *
 * This library is free software; you can redistribute it and/or modify it
 * under the terms of the MIT license. See LICENSE for details.
 */

#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

typedef uint64_t Value;

typedef union {
  uint64_t bits64;
  uint32_t bits32[2];
  double num;
} ValueBits;

typedef struct List {
  Value head, tail;
} List;

// A mask that selects the sign bit.
#define SIGN_BIT ((uint64_t)1 << 63)

// The bits that must be set to indicate a quiet NaN.
#define QNAN ((uint64_t)0x7ffc000000000000)

// If the NaN bits are set, it's not a number.
#define IS_NUM(value) (((value) & QNAN) != QNAN)

// An list pointer is a NaN with a set sign bit.
#define IS_LIST(value) (((value) & (QNAN | SIGN_BIT)) == (QNAN | SIGN_BIT))

// Value -> double
#define AS_NUM(num) (valueToNum(num))

// Value -> Object*.
#define AS_LIST(value) ((List*)(uintptr_t)((value) & ~(SIGN_BIT | QNAN)))

#define NUM_VAL(num) (numToValue(num))             // double

#define LIST_VAL(list) (listToValue(list))             // List


// Converts the raw object pointer [list] to a [Value].
static inline Value listToValue(List* list) {
  // The triple casting is necessary here to satisfy some compilers:
  // 1. (uintptr_t) Convert the pointer to a number of the right size.
  // 2. (uint64_t)  Pad it up to 64 bits in 32-bit builds.
  // 3. Or in the bits to make a tagged Nan.
  // 4. Cast to a typedef'd value.
  return (Value)(SIGN_BIT | QNAN | (uint64_t)(uintptr_t)(list));
}

// Interprets [value] as a [double].
static inline double valueToNum(Value value) {
  ValueBits data;
  data.bits64 = value;
  return data.num;
}

// Converts [num] to a [Value].
static inline Value numToValue(double num) {
  ValueBits data;
  data.num = num;
  return data.bits64;
}
