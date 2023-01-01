from typing import List

from asn1_parser.generators.cosmos.telemetry import (
    TelemetryEntry,
    RedYellowRange,
)
from asn1_parser.utils.size import TypeEnum


INDENT = "    "
FMT_ITEM = (
    INDENT
    + " ".join(
        (
            "{id_or_array:19s}",
            "{name:31s}",
            "{bitsize:>7s}",
            "{cos_type:7s}",
            "{specific_value:>7s}",
            '"{comment}"',
            "{endianness}",
        )
    )
    + "\n"
)
FMT_STATE = 2 * INDENT + "STATE {state_name:31s} {state_val}\n"
FMT_LIMITS = (
    2 * INDENT
    + "LIMITS DEFAULT 5 ENABLED {err_start} {warn_start} {warn_end} {err_end}"
    + "\n"
)
FMT_UNITS = 2 * INDENT + "UNITS {unit} {unit}\n"


def cosmos_telemetry(
    target_name: str,
    target_comment: str,
    pkt_name: str,
    telemetry: List[TelemetryEntry],
) -> str:
    telemetry_pkt: str = (
        f'TELEMETRY {target_name} {pkt_name} BIG_ENDIAN "{target_comment}"\n'
    )

    telemetry_packet: TelemetryEntry
    for telemetry_packet in telemetry:
        name = telemetry_packet.name
        bitsize = str(telemetry_packet.bitsize)
        cosmos_type = telemetry_packet.cosmos_type
        specific_value = telemetry_packet.specific_value
        comment = telemetry_packet.comment
        unit = telemetry_packet.unit
        states = telemetry_packet.state_list
        is_array = telemetry_packet.is_array
        is_little_endian = telemetry_packet.is_little_endian

        # Prepare logic

        cos_type = cosmos_type.value
        if cosmos_type == TypeEnum.A_BOOL:
            # change c_bool to UINT
            cos_type = "UINT"
            if specific_value == "True":
                specific_value = "1"
            else:
                specific_value = "0"
        elif cosmos_type == TypeEnum.A_DOUBLE:
            # change c_double to FLOAT
            cos_type = "FLOAT"

        if is_array:
            id_or_array = "APPEND_ARRAY_ITEM"
        elif (specific_value is not None) and (specific_value != ""):
            id_or_array = "APPEND_ID_ITEM"
        else:
            id_or_array = "APPEND_ITEM"

        # Format

        telemetry_pkt += FMT_ITEM.format(
            id_or_array=id_or_array,
            name=name,
            bitsize=bitsize,
            cos_type=cos_type,
            specific_value=specific_value,
            comment=comment,
            endianness="LITTLE_ENDIAN" if is_little_endian else "",
        ).replace(" \n", "\n")

        for state_val, state_name in enumerate(states):
            telemetry_pkt += FMT_STATE.format(
                state_name=state_name,
                state_val=state_val,
            )

        if telemetry_packet.red_yellow_range:
            red_yellow_range: RedYellowRange = telemetry_packet.red_yellow_range
            telemetry_pkt += FMT_LIMITS.format(
                err_start=red_yellow_range.range_start_red,
                warn_start=red_yellow_range.range_start_yellow,
                warn_end=red_yellow_range.range_end_yellow,
                err_end=red_yellow_range.range_end_red,
            )

        if unit:
            telemetry_pkt += FMT_UNITS.format(unit=unit)

    return telemetry_pkt
