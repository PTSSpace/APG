from typing import Any

from asn1_parser.asn1.grammar_elements.asn1_type import Asn1Type


class Array:
    def __init__(self, asn_type: Asn1Type, length: int, parent: Any) -> None:
        self._asn_type = asn_type
        self._length = length
        self._parent = parent

    def __str__(self) -> str:
        return str(self._asn_type) + "(len: " + str(self._length) + ")"

    def get_length(self) -> int:
        return self._length

    def get_asn_type(self) -> Asn1Type:
        return self._asn_type

    def get_size_bits(self) -> int:
        # TODO: check if it has to be multiplied by the length of the type
        return self.get_length() * 8
