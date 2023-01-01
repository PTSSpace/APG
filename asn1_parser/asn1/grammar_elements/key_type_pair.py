from typing import Any

from asn1_parser.asn1.grammar_elements.asn1_comment import Asn1Comment
from asn1_parser.asn1.grammar_elements.asn1_type import Asn1Type
from asn1_parser.asn1.grammar_elements.with_components import WithComponents
from asn1_parser.log.logger import Logger


class KeyTypePair:
    _logger = Logger(__name__)

    def __init__(  # pylint: disable=too-many-arguments
        self,
        key: str,
        asn_type: Asn1Type,
        comment: Asn1Comment,
        with_components: WithComponents,
        parent: Any,
    ) -> None:
        self._key = key
        self._asn_type = asn_type
        self._comment = comment
        KeyTypePair._logger.debug(f"comment: {self._comment}")
        self._with_components = with_components
        self._parent = parent

    def __str__(self) -> str:
        return str(self._asn_type) + ": " + self._key

    def pprint(self, level: int = 0) -> None:
        indent = ("│   " * (level >= 1)) + ("    " * (level - 1))

        line = f"{indent}├─ KeyTypePair key={self._key} type={self._asn_type}"
        if self._with_components:
            line += " value=WithComponents"
        else:
            line += " value=None"
        print(line)

        if self._with_components:
            self._with_components.pprint(level + 1)

    def get_comment(self) -> Asn1Comment:
        return self._comment

    def get_key(self) -> str:
        return self._key

    def get_asn_type(self) -> Asn1Type:
        return self._asn_type

    def get_with_components(self) -> WithComponents:
        return self._with_components

    def get_size_bits(self) -> int:
        """
        Returns the minimum size, in bits, needed to encode this object.
        """
        return self.get_asn_type().get_size_bits()

    @property
    def asn_type(self) -> Asn1Type:
        return self._asn_type


class KeyTypePairNotLast(KeyTypePair):
    pass


class KeyTypePairLast(KeyTypePair):
    pass
