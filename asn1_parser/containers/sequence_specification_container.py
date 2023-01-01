from typing import Optional
from asn1_parser.utils.size import TypeEnum


class SequenceSpecificationContainer:
    def __init__(
        self, c_type: Optional[TypeEnum], bitsize: int, seq_type: str
    ) -> None:
        self._c_type = c_type
        self._bitsize = bitsize
        self._seq_type = seq_type

    def __str__(self) -> str:
        return (
            f"c_type: {self._c_type}, {self._bitsize} bits, seq_type: "
            f"{self._seq_type}"
        )

    def get_c_type(self) -> Optional[TypeEnum]:
        return self._c_type

    def get_bitsize(self) -> int:
        return self._bitsize

    def get_seq_type(self) -> str:
        return self._seq_type
