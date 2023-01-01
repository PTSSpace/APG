from typing import Any


class Asn1Comment:
    def __init__(
        self, parent: Any, comment: str, unit: str, is_little_endian: bool
    ) -> None:
        self._comment = comment
        self._unit = unit
        self._is_little_endian = is_little_endian
        self._parent = parent

    def __str__(self) -> str:
        return f"[{self._unit}] {self._comment}"

    def get_unit(self) -> str:
        return self._unit

    def get_comment(self) -> str:
        return self._comment

    def is_item_little_endian(self) -> bool:
        return self._is_little_endian

    def set_little_endian(self, little_endian: bool) -> None:
        self._is_little_endian = little_endian

    def get_parent(self) -> Any:
        return self._parent
