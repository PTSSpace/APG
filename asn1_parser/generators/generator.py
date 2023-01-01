import math
from typing import Any, List, Optional, Tuple, Union

import cgen
from asn1_parser.asn1.grammar_elements.array import Array
from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.asn1_string import Asn1String
from asn1_parser.asn1.grammar_elements.choice import Choice
from asn1_parser.asn1.grammar_elements.enumerated import Enumerated
from asn1_parser.asn1.grammar_elements.key_type_pair import KeyTypePair

from asn1_parser.asn1.grammar_elements.sequence import Sequence

from asn1_parser.asn1.grammar_elements.simple_definition import SimpleDefinition
from asn1_parser.c_data import CData
from asn1_parser.c_printer import CPrinter
from asn1_parser.utils.size import ASN1_POSIX_RANGE, TypeEnum, get_bit_size
from asn1_parser.utils.string import lowerize


class Generator:
    _C_SPACES = "  "

    _POSIX_DEFINED_TYPES = [
        posix.lower().replace("-", "_")
        for posix, _ in ASN1_POSIX_RANGE.items()
        if posix not in ["Float", "Double"]
    ]

    @classmethod
    def _map_simple_types_to_c(
        cls, definition: Union[SimpleDefinition, KeyTypePair]
    ) -> Tuple[str, str, bool, bool]:
        # map SimpleDefinitions to c typedef
        # if it's a POSIX defined type, use it instead of the
        # self defined
        # see: https://stackoverflow.com/a/44573281
        bit_length: str = ""
        valid_c_type: str = CPrinter.asn1_to_c_style_naming(
            definition.get_asn_type().get_type_name()
        )
        is_stdbool_needed = False
        is_stdint_needed = False

        if valid_c_type in ["INTEGER", "REAL"] or isinstance(
            definition, SimpleDefinition
        ):
            c_type: Optional[TypeEnum] = definition.get_asn_type().get_c_type()
            if c_type is None:
                raise NotImplementedError(
                    f"c_type is None for {definition}. "
                    "The value should never be None."
                )
            bit_size: int = get_bit_size(
                c_type,
                definition.get_asn_type().get_begin(),
                definition.get_asn_type().get_end(),
            )

            if c_type == TypeEnum.A_UINT and bit_size not in [8, 16, 32, 64]:
                bit_length = " : " + str(bit_size)

            # get smallest possible defined posix uint
            next_bit_size: int = bit_size
            mod: float = math.log(next_bit_size, 2)
            while mod % 1 != 0 or mod < 3:
                next_bit_size = next_bit_size + 1
                mod = math.log(next_bit_size, 2)
            valid_c_type = c_type.value.lower()
            if valid_c_type == "uint":
                if (
                    valid_c_type + str(next_bit_size) + "_t"
                ) in cls._POSIX_DEFINED_TYPES:
                    is_stdint_needed = True
                    valid_c_type = valid_c_type + str(next_bit_size) + "_t"
                else:
                    # TODO specify correctly (smallest uint)
                    # if not matching get something big
                    valid_c_type = "unsigned long long"
        elif valid_c_type == "BOOLEAN":
            # Note: booleans are encoded as uint8_t bitfilds of 1 bit
            bit_length = " : 1"
            valid_c_type = "uint8_t"
            is_stdint_needed = True
        elif isinstance(definition.get_asn_type().get_type(), Enumerated):
            # "Pack" enums using bitfields (needs __attribute__((packed)) too)
            bit_length = " : " + str(definition.get_size_bits())
        else:
            pass

        return bit_length, valid_c_type, is_stdbool_needed, is_stdint_needed

    @classmethod
    def _convert_sequence_to_c(
        cls,
        simple_definition_list: List[SimpleDefinition],
        definition: Sequence,
        module: Asn1Module,
    ) -> CData:
        cdata = CData.create_empty()
        comment_str: str = ""

        if definition.get_comment() and definition.get_comment().get_comment():
            comment_str += str(
                cgen.Comment(definition.get_comment().get_comment())
            )
            comment_str += "\n"

        # map Sequence to c struct
        sequence_list: List[Any] = []
        for seq_item in definition.get_children():
            if seq_item.get_comment():
                seq_comment: str = ""
                if seq_item.get_comment().get_unit():
                    seq_comment = (
                        seq_comment
                        + "["
                        + seq_item.get_comment().get_unit()
                        + "] "
                    )
                if seq_item.get_comment().get_comment():
                    seq_comment = (
                        seq_comment + seq_item.get_comment().get_comment()
                    )
                sequence_list.append(cgen.LineComment(seq_comment))

            (
                bit_length,
                struct_c_type,
                is_stdbool,
                is_stdint,
            ) = cls._map_simple_types_to_c(seq_item)
            # prevent overriding with false
            cdata.set_stdbool_if_needed(is_stdbool)
            cdata.set_stdint_if_needed(is_stdint)

            # Note: booleans are encoded as 1 bit bitfields
            if lowerize(struct_c_type) in cls._POSIX_DEFINED_TYPES:
                struct_c_type = lowerize(struct_c_type)
                cdata.set_stdint_if_needed(True)

            simple_definition: List[SimpleDefinition] = [
                sd
                for sd in simple_definition_list
                if CPrinter.asn1_to_c_style_naming(sd.get_type_name())
                == struct_c_type
            ]
            if len(simple_definition) > 0:
                (
                    bit_length,
                    struct_c_type,
                    is_stdbool,
                    is_stdint,
                ) = cls._map_simple_types_to_c(simple_definition[0])
                # prevent overriding with false
                cdata.set_stdbool_if_needed(is_stdbool)
                cdata.set_stdint_if_needed(is_stdint)

            seq_key = CPrinter.asn1_to_c_style_naming(seq_item.get_key())

            if bit_length:
                seq_key += bit_length

            seq_item_type = seq_item.get_asn_type().get_type()
            if isinstance(seq_item_type, (Array, Asn1String)):
                # array or string (char array)

                sequence_list.append(
                    cgen.ArrayOf(
                        cgen.Value(
                            struct_c_type,
                            seq_key,
                        ),
                        seq_item_type.get_length(),
                    )
                )
            else:
                sequence_list.append(
                    cgen.Value(
                        struct_c_type,
                        seq_key,
                    )
                )
            definition_type_name_c: str = CPrinter.asn1_to_c_style_naming(
                definition.get_type_name()
            )
            # WITH COMPONENTS
            if seq_item.get_with_components():
                cdata.extend_with_cdata(
                    cls._with_components_handling(
                        definition_type_name_c=definition_type_name_c,
                        seq_item=seq_item,
                        module=module,
                    )
                )
        cdata.add_data(
            comment_str
            + str(
                cgen.Typedef(
                    cgen.Struct(
                        "",
                        sequence_list,
                        definition_type_name_c,
                    )
                )
            )
        )

        return cdata

    @classmethod
    def _convert_enumerated_to_c(cls, definition: Enumerated) -> CData:
        cdata = CData.create_empty()
        data_str: str = ""

        if definition.get_comment() and definition.get_comment().get_comment():
            data_str += str(
                cgen.Comment(definition.get_comment().get_comment())
            )
            data_str += "\n"
        # map Enumerated to c enum
        data_str += "typedef enum {\n"
        for enum_item in definition.get_enum():
            enum_item_comment: str = ""
            if enum_item.get_comment():
                if enum_item.get_comment().get_unit():
                    enum_item_comment = (
                        enum_item_comment
                        + "["
                        + enum_item.get_comment().get_unit()
                        + "] "
                    )
                if enum_item.get_comment().get_comment():
                    enum_item_comment = (
                        enum_item_comment
                        + enum_item.get_comment().get_comment()
                    )
                enum_item_comment = "     " + str(
                    cgen.LineComment(enum_item_comment)
                )
            data_str += (
                cls._C_SPACES
                + CPrinter.asn1_to_c_style_naming(enum_item.get_key())
                + " = "
                + str(enum_item.get_pos())
                + ","
                + enum_item_comment
                + "\n"
            )
        data_str += (
            "} __attribute__((packed)) "
            + CPrinter.asn1_to_c_style_naming(definition.get_type_name())
            + ";"
        )

        cdata.add_data(data_str)

        return cdata

    @classmethod
    def _convert_choice_to_c(cls, definition: Choice) -> CData:
        cdata = CData.create_empty()
        data_str: str = ""

        if definition.get_comment() and definition.get_comment().get_comment():
            data_str += str(
                cgen.Comment(definition.get_comment().get_comment())
            )
            data_str += "\n"
        # map Choice to c union
        data_str += (
            "union "
            + CPrinter.asn1_to_c_style_naming(definition.get_type_name())
            + " {\n"
        )
        for choice_item in definition.get_children():
            choice_comment: str = ""
            if choice_item.get_comment():
                if choice_item.get_comment().get_unit():
                    choice_comment = (
                        choice_comment
                        + "["
                        + choice_item.get_comment().get_unit()
                        + "] "
                    )
                if choice_item.get_comment().get_comment():
                    choice_comment = (
                        choice_comment + choice_item.get_comment().get_comment()
                    )
                choice_comment = "     " + str(cgen.LineComment(choice_comment))

            if (
                choice_item.get_asn_type().get_type_name()
                in cls._POSIX_DEFINED_TYPES
            ):
                cdata.set_stdint_if_needed(True)
            data_str += (
                cls._C_SPACES
                + CPrinter.asn1_to_c_style_naming(
                    choice_item.get_asn_type().get_type_name()
                )
                + " "
                + CPrinter.asn1_to_c_style_naming(choice_item.get_key())
                + ";"
                + choice_comment
            )
        data_str += (
            "} "
            + lowerize(
                CPrinter.asn1_to_c_style_naming(definition.get_type_name())
            )
            + ";"
        )

        cdata.add_data(data_str)

        return cdata

    @classmethod
    def _with_components_handling(
        cls,
        definition_type_name_c: str,
        seq_item: KeyTypePair,
        module: Optional[Asn1Module],
    ) -> CData:
        raise NotImplementedError(
            "This method must be implemented by subclasses."
        )
