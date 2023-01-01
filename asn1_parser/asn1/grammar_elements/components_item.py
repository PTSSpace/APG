from typing import Any

from asn1_parser.asn1.grammar_elements.asn1_comment import Asn1Comment
from asn1_parser.log.logger import Logger


class ComponentsItem:
    _logger = Logger(__name__)

    def __init__(
        self, key: str, value: Any, comment: Asn1Comment, parent: Any
    ) -> None:
        self._key = key
        self._value = value
        self._comment = comment
        ComponentsItem._logger.debug(f"comment: {self._comment}")
        self._parent = parent

    def __str__(self) -> str:
        return self._key + " - " + str(self._value)

    def pprint(self, level: int = 0) -> None:
        # pylint: disable=import-outside-toplevel
        from asn1_parser.asn1.grammar_elements import with_components

        indent = ("│   " * (level >= 1)) + ("    " * (level - 1))

        vcn = self._value.__class__.__name__
        line = f"{indent}├─ ComponentsItem: key={self._key} value={vcn}"
        if isinstance(self._value, (int, float)):
            line += f" - value={self._value}"
            print(line)
        elif isinstance(self._value, with_components.WithComponents):
            print(line)
            self._value.pprint(level + 1)
        else:
            raise Exception(f"Unhandled type: {type(self._value)}")

    def get_comment(self) -> Asn1Comment:
        return self._comment

    def get_key(self) -> str:
        return self._key

    def get_value(self) -> Any:
        return self._value

    def set_value(self, outside_value: Any) -> None:
        self._value = outside_value


class ComponentsItemNotLast(ComponentsItem):
    pass


class ComponentsItemLast(ComponentsItem):
    pass
