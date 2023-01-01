#include <assert.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "sample_module.h"

const char *path = "output/binary/sample_packet.bin";
const float tolerance_f = 0.000001;
const double tolerance_d = 0.00000000001;

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

typedef union
{
  double value;
  unsigned char byte_representation[8];
} Double_representation;

Double_representation swap_bytes_double(double float_number) {
  Double_representation value = {
    .value = float_number
  };

  unsigned char tmp = value.byte_representation[0];
  value.byte_representation[0] = value.byte_representation[7];
  value.byte_representation[7] = tmp;

  tmp = value.byte_representation[1];
  value.byte_representation[1] = value.byte_representation[6];
  value.byte_representation[6] = tmp;

  tmp = value.byte_representation[2];
  value.byte_representation[2] = value.byte_representation[5];
  value.byte_representation[5] = tmp;

  tmp = value.byte_representation[3];
  value.byte_representation[3] = value.byte_representation[4];
  value.byte_representation[4] = tmp;

  return value;
}

int main() {
  uint32_t size_sample_packet = sizeof(Sample_packet);
  Sample_packet *sample_packet = malloc(size_sample_packet);
  FILE * readfile = fopen(path, "rb");
  if (readfile != NULL) {
    fread(sample_packet, size_sample_packet, 1, readfile);
    fclose(readfile);
  }

  // TODO: uncomment the next lines if running on a big-endian machine
  //Float_representation tmp_value1 = swap_bytes(
  //  sample_packet->sample_packet_with_component.with_component_packet_number_1
  //);
  //sample_packet->sample_packet_with_component.with_component_packet_number_1 = tmp_value1.value;

  //Double_representation tmp_value2 = swap_bytes_double(
  //  sample_packet->sample_packet_with_component.with_component_packet_number_2
  //);
  //sample_packet->sample_packet_with_component.with_component_packet_number_2 = tmp_value2.value;

  assert(
    (sample_packet->sample_packet_with_component.with_component_packet_number_1 - 170141183460469231731687303715884105728.0) > -tolerance_f
    && (sample_packet->sample_packet_with_component.with_component_packet_number_1 - 170141183460469231731687303715884105728.0) < tolerance_f
  );

  assert(
    (sample_packet->sample_packet_with_component.with_component_packet_number_2 - 390000000000000000000000000000000000000.0) > -tolerance_d
    && (sample_packet->sample_packet_with_component.with_component_packet_number_2 - 390000000000000000000000000000000000000.0) < tolerance_d
  );

  free(sample_packet);

  return 0;
}