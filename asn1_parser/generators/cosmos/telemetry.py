from typing import List, Optional
from asn1_parser.utils.size import TypeEnum


class RedYellowRange:
    def __init__(
        self,
        range_start_red: float,
        range_start_yellow: float,
        range_end_yellow: float,
        range_end_red: float,
    ) -> None:
        self.range_start_red = range_start_red
        self.range_start_yellow = range_start_yellow
        self.range_end_yellow = range_end_yellow
        self.range_end_red = range_end_red


class TelemetryEntry:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        bitsize: int,
        cosmos_type: TypeEnum,
        specific_value: str,
        comment: str,
        unit: str,
        red_yellow_range: Optional[RedYellowRange],
        state_list: List[str],
        is_array: bool,
        is_little_endian: Optional[bool],
    ) -> None:
        self.name = name
        self.bitsize = bitsize
        self.cosmos_type = cosmos_type
        self.specific_value = specific_value
        self.comment = comment
        self.unit = unit
        self.red_yellow_range = red_yellow_range
        self.state_list = state_list
        self.is_array = is_array
        self.is_little_endian = is_little_endian
