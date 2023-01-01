from typing import List, Any

from asn1_parser.asn1.grammar_elements.asn1_comment import Asn1Comment
from asn1_parser.asn1.grammar_elements.definitions import Definitions
from asn1_parser.asn1.grammar_elements.key_type_pair import KeyTypePair


class Sequence(Definitions):
    def __init__(
        self,
        type_name: str,
        comment: Asn1Comment,
        parent: Any,
        seq: List[KeyTypePair],
    ) -> None:
        super().__init__(type_name, comment, parent)
        self._seq = seq

    def __str__(self) -> str:
        return self._type_name + ": " + str(self._seq)

    def pprint(self, level: int = 0) -> None:
        indent = ("│   " * (level >= 1)) + ("    " * (level - 1))
        print(f"{indent}├─ Sequence name={self._type_name}")
        for item in self._seq:
            assert isinstance(item, KeyTypePair)
            item.pprint(level + 1)

    def get_children(self) -> List[KeyTypePair]:
        return self._seq

    def get_size_bits(self) -> int:
        """
        Returns the minimum size, in bits, needed to encode this object.
        """
        bit_size = 0

        for member in self.get_children():
            bit_size += member.get_size_bits()

        return bit_size
