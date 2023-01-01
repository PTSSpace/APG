from typing import Any

from asn1_parser.asn1.grammar_elements.asn1_comment import Asn1Comment
from asn1_parser.log.logger import Logger


class Definitions:
    _logger = Logger(__name__)

    def __init__(
        self, type_name: str, comment: Asn1Comment, parent: Any
    ) -> None:
        self._type_name = type_name
        self._comment = comment
        Definitions._logger.debug(f"comment: {self._comment}")
        self._parent = parent

    def __str__(self) -> str:
        return self._type_name

    def get_type_name(self) -> str:
        return self._type_name

    def get_comment(self) -> Asn1Comment:
        return self._comment

    def pprint(self, level: int = 0) -> None:
        indent = ("│   " * (level >= 1)) + ("    " * (level - 1))
        print(f"{indent}├─ Definition: {self._type_name}")
