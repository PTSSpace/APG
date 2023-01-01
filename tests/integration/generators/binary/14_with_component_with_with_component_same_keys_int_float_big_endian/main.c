#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include "sample_module.h"

const char *path = "output/binary/seq0.bin";
const float tolerance = 0.000001;

typedef union
{
  float value;
  unsigned char byte_representation[4];
} Float_representation;

Float_representation swap_bytes(float float_number) {
  Float_representation value = {
    .value = float_number
  };

  unsigned char tmp = value.byte_representation[0];
  value.byte_representation[0] = value.byte_representation[3];
  value.byte_representation[3] = tmp;

  tmp = value.byte_representation[1];
  value.byte_representation[1] = value.byte_representation[2];
  value.byte_representation[2] = tmp;

  return value;
}


int main() {
  uint32_t size_seq0 = sizeof(Seq0);
  Seq0 *seq0 = malloc(size_seq0);
  FILE * readfile = fopen(path, "rb");
  if (readfile != NULL) {
    fread(seq0, size_seq0, 1, readfile);
    fclose(readfile);
  }

  // TODO: comment the next lines if running on a big-endian machine
  Float_representation tmp_my_value = swap_bytes(
    seq0->value.inner_with_component.my_value
  );
  seq0->value.inner_with_component.my_value = tmp_my_value.value;

  assert(
    seq0->value.my_value == 3
  );
  
  assert(
    (seq0->value.inner_with_component.my_value - 3.14) > -tolerance
    && (seq0->value.inner_with_component.my_value - 3.14) < tolerance
  );

  free(seq0);

  return 0;
}