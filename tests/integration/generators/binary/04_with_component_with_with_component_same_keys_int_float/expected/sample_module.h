#ifndef ASN1_PARSER_SAMPLE_MODULE_H_INCLUDED
#define ASN1_PARSER_SAMPLE_MODULE_H_INCLUDED

/*
This file was autogenerated from ASN.1 model.
*/

#include <stdint.h>

typedef struct
{
  float my_value;
} __attribute__((packed)) Seq2;

typedef struct
{
  uint8_t my_value;
  Seq2 inner_with_component;
} __attribute__((packed)) Seq1;

typedef struct
{
  Seq1 value;
} __attribute__((packed)) Seq0;

#endif // ASN1_PARSER_SAMPLE_MODULE_H_INCLUDED
