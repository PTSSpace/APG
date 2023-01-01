from typing import Any

from asn1_parser.asn1.grammar_elements.asn1_comment import Asn1Comment
from asn1_parser.asn1.grammar_elements.asn1_type import Asn1Type
from asn1_parser.asn1.grammar_elements.definitions import Definitions


class SimpleDefinition(Definitions):
    def __init__(
        self,
        type_name: str,
        comment: Asn1Comment,
        parent: Any,
        asn_type: Asn1Type,
    ) -> None:
        super().__init__(type_name, comment, parent)
        self._asn_type = asn_type

    def __str__(self) -> str:
        return self._type_name + " ::= " + str(self._asn_type)

    def pprint(self, level: int = 0) -> None:
        indent = ("│   " * (level >= 1)) + ("    " * (level - 1))
        print(
            f"{indent}├─ SimpleDefinition name={self._type_name}"
            f" type={self._asn_type}"
        )
        self._asn_type.pprint(level + 1)

    def get_asn_type(self) -> Asn1Type:
        return self._asn_type

    def get_size_bits(self) -> int:
        """
        Returns the minimum size, in bits, needed to encode this object.
        """
        return self.get_asn_type().get_size_bits()
