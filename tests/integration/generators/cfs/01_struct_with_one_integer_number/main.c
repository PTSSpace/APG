#include "sample_module_msg.h"

int main() {
  _Static_assert(
    sizeof(Sample_packet) == 1,
    "The size of the Sample_packet shall be 1 byte."
  );
  return 0;
}
