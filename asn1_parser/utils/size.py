import sys
from typing import Dict, Union

from enum import Enum

FLOAT_MIN = -3.4e38
FLOAT_MAX = 3.4e38
DOUBLE_MIN = -sys.float_info.max
DOUBLE_MAX = sys.float_info.max


ASN1_POSIX_RANGE: Dict[str, Dict[str, Union[int, float]]] = {
    "Int8-t": {"begin": (-pow(2, 7)), "end": (pow(2, 7) - 1)},
    "Int16-t": {"begin": (-pow(2, 15)), "end": (pow(2, 15) - 1)},
    "Int32-t": {"begin": (-pow(2, 31)), "end": (pow(2, 31) - 1)},
    "Int64-t": {"begin": (-pow(2, 63)), "end": (pow(2, 63) - 1)},
    "Uint8-t": {"begin": 0, "end": (pow(2, 8) - 1)},
    "Uint16-t": {"begin": 0, "end": (pow(2, 16) - 1)},
    "Uint32-t": {"begin": 0, "end": (pow(2, 32) - 1)},
    "Uint64-t": {"begin": 0, "end": (pow(2, 64) - 1)},
    "Float": {"begin": FLOAT_MIN, "end": FLOAT_MAX},
    "Double": {"begin": DOUBLE_MIN, "end": DOUBLE_MAX},
}


class TypeEnum(str, Enum):
    A_BOOL = "BOOL"
    A_UINT = "UINT"
    A_INT = "INT"
    A_STRING = "STRING"
    A_FLOAT = "FLOAT"
    A_DOUBLE = "DOUBLE"


def get_bit_size(
    c_type: TypeEnum, begin: Union[float, int], end: Union[float, int]
) -> int:
    bitsize: int = 0
    if c_type is TypeEnum.A_BOOL:
        bitsize = 1
    elif c_type is TypeEnum.A_UINT:
        assert isinstance(end, int), f"Expected int, got {type(end)} ({end})"
        bitsize = end.bit_length()  # int.bit_length() is a Python builtin
    elif c_type is TypeEnum.A_INT:
        assert isinstance(
            begin, int
        ), f"Expected int, got {type(end)} ({begin})"
        assert isinstance(end, int), f"Expected int, got {type(end)} ({end})"
        if (
            begin >= ASN1_POSIX_RANGE["Int8-t"]["begin"]
            and end <= ASN1_POSIX_RANGE["Int8-t"]["end"]
        ):
            bitsize = 8
        elif (
            begin >= ASN1_POSIX_RANGE["Int16-t"]["begin"]
            and end <= ASN1_POSIX_RANGE["Int16-t"]["end"]
        ):
            bitsize = 16
        elif (
            begin >= ASN1_POSIX_RANGE["Int32-t"]["begin"]
            and end <= ASN1_POSIX_RANGE["Int32-t"]["end"]
        ):
            bitsize = 32
        elif (
            begin >= ASN1_POSIX_RANGE["Int64-t"]["begin"]
            and end <= ASN1_POSIX_RANGE["Int64-t"]["end"]
        ):
            bitsize = 64
        else:
            raise ValueError(
                f"One of {begin} and {end} is out of stdint definition."
            )
    elif c_type is TypeEnum.A_FLOAT:
        bitsize = 32
    elif c_type is TypeEnum.A_DOUBLE:
        bitsize = 64
    elif c_type is TypeEnum.A_STRING:
        assert isinstance(end, int), f"Expected int, got {type(end)} ({end})"
        bitsize = end * 8  # byte -> bit
    else:
        raise NotImplementedError

    return bitsize


def bit_to_bytes(bits: int) -> int:
    if bits % 8 != 0:
        raise ValueError(
            f"The bits ({bits}) cannot be fully represented as bytes."
        )
    return int(bits / 8)
