#include "sample_module_msg.h"

int main() {
  _Static_assert(
    sizeof(Sample_packet) == 4,
    "The size of the Sample_packet shall be 1 byte."
  );
  return 0;
}
