from typing import List, Any

from asn1_parser.asn1.grammar_elements.asn1_comment import Asn1Comment
from asn1_parser.asn1.grammar_elements.definitions import Definitions
from asn1_parser.asn1.grammar_elements.key_type_pair import KeyTypePair


class Choice(Definitions):
    def __init__(
        self,
        type_name: str,
        comment: Asn1Comment,
        parent: Any,
        choice: List[KeyTypePair],
    ) -> None:
        super().__init__(type_name, comment, parent)
        self._choice = choice

    def __str__(self) -> str:
        return self._type_name + ": " + str(self._choice)

    def get_children(self) -> List[KeyTypePair]:
        return self._choice
