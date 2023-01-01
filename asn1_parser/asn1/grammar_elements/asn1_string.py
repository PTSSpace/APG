from typing import Any


class Asn1String:
    def __init__(self, length: int, type_name: str, parent: Any) -> None:
        self._length = length
        self._type_name = type_name
        self._parent = parent

    def __str__(self) -> str:
        return self._type_name + " (size: " + str(self._length) + ")"

    def get_length(self) -> int:
        """
        Returns the length of the string in bytes.
        """
        return self._length

    def get_type_name(self) -> str:
        return self._type_name

    def get_size_bits(self) -> int:
        return self.get_length() * 8
