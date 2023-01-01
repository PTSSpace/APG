#include <assert.h>
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

  With_component_packet sample_packet_with_component = sample_packet->sample_packet_with_component;

  sample_packet_with_component.with_component_packet_number_1
    = le32toh(sample_packet_with_component.with_component_packet_number_1);
  sample_packet_with_component.with_component_packet_number_2
    = le64toh(sample_packet_with_component.with_component_packet_number_2);

  Inner_with_component_packet with_component_packet_inner_with_component
    = sample_packet_with_component.with_component_packet_inner_with_component;

  with_component_packet_inner_with_component.inner_with_component_packet_number_1
    = le16toh(with_component_packet_inner_with_component.inner_with_component_packet_number_1);
  with_component_packet_inner_with_component.inner_with_component_packet_number_2
    = le16toh(with_component_packet_inner_with_component.inner_with_component_packet_number_2);

  assert(
    sample_packet_with_component.with_component_packet_number_1 == 23
  );

  assert(
    sample_packet_with_component.with_component_packet_number_2 == 42
  );
  
  assert(
    with_component_packet_inner_with_component.inner_with_component_packet_number_1 == 1
  );

  assert(
    with_component_packet_inner_with_component.inner_with_component_packet_number_2 == 9
  );

  free(sample_packet);

  return 0;
}