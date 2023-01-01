#include <assert.h>
#include <endian.h>
#include <stdio.h>
#include <stdlib.h>

#include "sample_module.h"

const char *path = "output/binary/sample_packet.bin";

int main() {
  uint32_t size_sample_packet = sizeof(Sample_packet);
  Sample_packet *sample_packet = malloc(size_sample_packet);
  FILE * readfile = fopen(path, "rb");
  if (readfile != NULL) {
    fread(sample_packet, size_sample_packet, 1, readfile);
    fclose(readfile);
  }

  sample_packet->sample_packet_with_component.with_component_packet_number_1
    = be32toh(sample_packet->sample_packet_with_component.with_component_packet_number_1);
  sample_packet->sample_packet_with_component.with_component_packet_number_2
    = be64toh(sample_packet->sample_packet_with_component.with_component_packet_number_2);

  assert(
    sample_packet->sample_packet_with_component.with_component_packet_number_1 == 23
  );

  assert(
    sample_packet->sample_packet_with_component.with_component_packet_number_2 == 42
  );

  free(sample_packet);

  return 0;
}