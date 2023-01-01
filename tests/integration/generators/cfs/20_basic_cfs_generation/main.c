#include <stdio.h>

#include "sandbox_hk_pc_msg.h"
#include "sandbox_hk_pc_msgids.h"

int main() {
  // TODO check assertions
  // 4 + 4 + 4 + 4 + 8 + 8 + 8 = 40
  _Static_assert(
    sizeof(Payload_sandbox_hk_pc) == 40,
    "The size of the Payload_sandbox_hk_pc shall be 40 bytes."
  );
  // printf("%ld\n", sizeof(Sandbox_hk_pc));  // -> 57
  // Cfe_tlm_header
  //   Ccsds_primary_header
  //     2 + 2 + 2
  //   Cfe_tm_secondary_header
  //     6
  //   4
  // Payload_sandbox_hk_pc
  //   40
  // -> 6 + 6 + 4 + 40 = 56
  _Static_assert(
    sizeof(Sandbox_hk_pc) == 56,
    "The size of the Sandbox_hk_pc shall be 56 bytes."
  );
  // printf("%ld\n", sizeof(Sequence_flag));  // -> 1
  _Static_assert(
    sizeof(Sequence_flag) == 1,
    "The size of the Sequence_flag shall be 1 byte."
  );
  _Static_assert(
    sizeof(Packet_identification) == 2,
    "The size of the Packet_identification shall be 2 bytes."
  );
  // 4 + 2 (+2) + 4 = 10 (+2)
  // _Static_assert(
  //   sizeof(Cfe_tm_secondary_header) == 12,
  //   "The size of the Cfe_tm_secondary_header shall be 12 byte."
  // );
  // printf("%ld\n", sizeof(Packet_sequence_control));  // -> 2
  // seq_fl +
  // 1 + 1 = 2
  _Static_assert(
    sizeof(Packet_sequence_control) == 2,
    "The size of the Packet_sequence_control shall be 2 bytes."
  );
  printf("%ld\n", sizeof(Ccsds_primary_header));  // -> 7
  // + Packet_id + Packet_seq_contr +
  // 2 + 2 + 2 = 6
  _Static_assert(
    sizeof(Ccsds_primary_header) == 6,
    "The size of the Ccsds_primary_header shall be 6 bytes."
  );
  return 0;
}
