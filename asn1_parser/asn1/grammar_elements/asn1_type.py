from typing import Any, Optional, Union

from asn1_parser.utils.size import (
    TypeEnum,
    get_bit_size,
)


class Asn1Type:
    def __init__(
        self, begin: float, end: float, type_name: Any, parent: Any
    ) -> None:
        # avoid circular import
        # pylint: disable=import-outside-toplevel
        from asn1_parser.asn1.grammar_elements.asn1_string import Asn1String
        from asn1_parser.asn1.grammar_elements.array import Array

        self._type_name: str
        self._begin = begin
        self._end = end
        self._c_type: Optional[TypeEnum] = None
        self._type: Union[Array, Asn1String, None]
        if isinstance(type_name, Array):
            self._type = type_name
            self._type_name = type_name.get_asn_type().get_type_name()
        elif isinstance(type_name, Asn1String):
            self._type = type_name
            self._type_name = type_name.get_type_name()
        else:
            self._type = None
            self._type_name = type_name
        self._parent = parent

    def __str__(self) -> str:
        return (
            self._type_name
            + "("
            + str(self._begin)
            + " -> "
            + str(self._end)
            + ")"
        )

    def pprint(self, level: int = 0) -> None:
        indent = ("│   " * (level >= 1)) + ("    " * (level - 1))
        print(
            f"{indent}├─ Asn1Type type_name={self._type_name}"
            f" begin={self._begin} end={self._end}"
        )

    def get_begin(self) -> float:
        return self._begin

    def set_begin_if_none(self, begin: Union[int, float]) -> None:
        if self._begin is None:
            self._begin = begin

    def get_end(self) -> float:
        return self._end

    def set_end_if_none(self, end: Union[int, float]) -> None:
        if self._end is None:
            self._end = end

    def get_type(self) -> Any:
        return self._type

    def set_type(self, new_type: Any) -> None:
        self._type = new_type

    def get_type_name(self) -> str:
        return self._type_name

    def set_type_name(self, outside_type_name: str) -> None:
        self._type_name = outside_type_name

    def get_c_type(self) -> Optional[TypeEnum]:
        return self._c_type

    def set_c_type(self, c_type: Optional[TypeEnum]) -> None:
        self._c_type = c_type

    def get_size_bits(self) -> int:
        """
        Returns the minimal number of bits needed to encode this type.
        """
        if self.get_type() is not None:
            size: int = self.get_type().get_size_bits()
            return size

        c_type: Optional[TypeEnum] = self.get_c_type()
        if c_type is not None:
            return get_bit_size(c_type, self.get_begin(), self.get_end())

        raise NotImplementedError(
            "Should never be reached. Trying to get the bit size of a asn1 type"
            f" which is None or the c_type is None. [{self}]"
        )
