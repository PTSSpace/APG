from typing import List, Any

from asn1_parser.asn1.grammar_elements.asn1_comment import Asn1Comment
from asn1_parser.asn1.grammar_elements.definitions import Definitions
from asn1_parser.asn1.grammar_elements.enumerated_item import EnumeratedItem


class Enumerated(Definitions):
    def __init__(
        self,
        type_name: str,
        comment: Asn1Comment,
        parent: Any,
        enum: List[EnumeratedItem],
    ) -> None:
        super().__init__(type_name, comment, parent)
        self._enum = enum

    def __str__(self) -> str:
        return self._type_name + ": " + str(self._enum)

    def get_enum(self) -> List[EnumeratedItem]:
        return self._enum

    def get_states(self) -> List[str]:
        return_list = []
        for enumerate_item in self._enum:
            return_list.append(enumerate_item.get_item()[0])
        return return_list

    def set_enum(self, outside_enum: List[EnumeratedItem]) -> None:
        self._enum = outside_enum

    def get_size_bits(self) -> int:
        """
        Returns the minimum size, in bits, needed to encode this object.
        """
        values = [e.get_pos() for e in self.get_enum()]
        last_value = max(values)
        return last_value.bit_length()  # int.bit_length() is a Python builtin
