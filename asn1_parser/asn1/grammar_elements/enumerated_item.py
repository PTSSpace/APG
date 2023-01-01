from typing import Tuple, Any
from asn1_parser.asn1.grammar_elements.asn1_comment import Asn1Comment
from asn1_parser.log.logger import Logger


class EnumeratedItem:
    _logger = Logger(__name__)

    def __init__(
        self, key: str, pos: int, comment: Asn1Comment, parent: Any
    ) -> None:
        self._key = key
        self._pos = pos
        self._comment = comment
        EnumeratedItem._logger.debug(f"comment: {self._comment}")
        self._parent = parent

    def __str__(self) -> str:
        return self._key + "(" + str(self._pos) + ")"

    def get_key(self) -> str:
        return self._key

    def get_pos(self) -> int:
        return self._pos

    def get_comment(self) -> Asn1Comment:
        return self._comment

    def get_item(self) -> Tuple[str, int]:
        return (self._key, self._pos)

    def set_pos(self, outside_pos: int) -> None:
        self._pos = outside_pos


class EnumeratedItemNotLast(EnumeratedItem):
    pass


class EnumeratedItemLast(EnumeratedItem):
    pass
