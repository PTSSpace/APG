#include "main_module_msg.h"

Sample_packet sample_packet;

_Static_assert(
  sizeof(sample_packet.number_0_100) == 4,
  "The size of the Sample_packet number_0_100 shall be 4 byte."
);

_Static_assert(
  sizeof(sample_packet.number_float) == 4,
  "The size of the Sample_packet number_float shall be 4 byte."
);

_Static_assert(
  sizeof(sample_packet.number_double) == 8,
  "The size of the Sample_packet number_double shall be 8 byte."
);

// no sizeof for bitfields
// _Static_assert(
//   sizeof(sample_packet.number_3_bit) == 1,
//   "The size of the Sample_packet number_3_bit shall be 1 byte."
// );

_Static_assert(
  sizeof(sample_packet.number_16_bit) == 2,
  "The size of the Sample_packet number_16_bit0 shall be 2 byte."
);

_Static_assert(
  // float + float + double + uint8 + uint16
  // 4 + 4 + 8 + 1 + 2 = 19
  sizeof(Sample_packet) == 19,
  "The size of the Sample_packet shall be 19 byte."
);
