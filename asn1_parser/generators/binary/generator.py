import os
import pathlib
import struct

from typing import Dict, List, Optional, Union

import cgen

from asn1_parser.asn1.asn1_bundle import ASN1Bundle
from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.asn1_type import Asn1Type
from asn1_parser.asn1.grammar_elements.choice import Choice
from asn1_parser.asn1.grammar_elements.components_item import ComponentsItem
from asn1_parser.asn1.grammar_elements.enumerated import Enumerated
from asn1_parser.asn1.grammar_elements.import_item import ImportItem
from asn1_parser.asn1.grammar_elements.key_type_pair import KeyTypePair
from asn1_parser.asn1.grammar_elements.sequence import Sequence
from asn1_parser.asn1.grammar_elements.simple_definition import SimpleDefinition
from asn1_parser.asn1.grammar_elements.with_components import WithComponents
from asn1_parser.c_data import CData
from asn1_parser.c_printer import CPrinter, HeaderType
from asn1_parser.cli.cli_arg_parser import GenerateBinaryCommandConfig
from asn1_parser.containers.sequence_specification_container import (
    SequenceSpecificationContainer,
)
from asn1_parser.generators.cfs.module_sorter import ModuleSorter
from asn1_parser.generators.generator import Generator
from asn1_parser.utils.size import TypeEnum, bit_to_bytes

from asn1_parser.utils.string import lowerize


class BinaryGenerator(Generator):
    # https://docs.python.org/3/library/struct.html#format-strings
    ENDIANNESS: Dict[str, str] = {"little-endian": "<", "big-endian": ">"}
    FORMAT: Dict[TypeEnum, Dict[int, str]] = {
        # TODO: boolean handling not yet implemented
        # TypeEnum.A_BOOL: {
        #     1: "?",  # 1 byte, boolean
        # },
        TypeEnum.A_DOUBLE: {
            8: "d",  # 8 bytes, double
        },
        TypeEnum.A_FLOAT: {
            4: "f",  # 4 bytes, float
        },
        TypeEnum.A_INT: {
            1: "b",  # 1 byte, signed char
            2: "h",  # 2 bytes, signed short
            4: "i",  # 4 bytes, signed int
            8: "q",  # 8 bytes, signed long long
        },
        # TODO: string handling not yet implemented
        # TypeEnum.A_STRING: {
        #     "c",  # 1 byte, char
        #     "s",  # 1 byte, string
        # },
        TypeEnum.A_UINT: {
            1: "B",  # 1 byte, unsigned char
            2: "H",  # 2 bytes, unsigned short
            4: "I",  # 4 bytes, unsigned int
            8: "Q",  # 8 bytes, unsigned long long
        },
    }
    # TODO: currently no spare used
    # SPARE: str = "x"

    endianness: str = ""

    @classmethod
    def get_filename(cls, module: Union[Asn1Module, ImportItem]) -> str:
        return CPrinter.asn1_to_c_style_naming(module.get_module_name())

    @classmethod
    def generate_binary(
        cls, config: GenerateBinaryCommandConfig, bundle: ASN1Bundle
    ) -> None:
        cls.endianness = config.endianness
        output_folder = config.output_dir
        if not os.path.isdir(output_folder):
            pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

        module_list_ordered: List[Asn1Module] = bundle.get_modules_ordered()

        for module in module_list_ordered:
            module_cdata = CData.create_empty()

            # Include

            comment = module.get_comment_import()
            if comment is not None:
                module_cdata.add_include(
                    str(cgen.LineComment(comment.get_comment()))
                )

            simple_definition_list_imported: List[SimpleDefinition] = []
            for imported_module in module.get_imported_modules():
                simple_definition_list_imported.extend(
                    [
                        d
                        for d in imported_module.get_definitions()
                        if isinstance(d, SimpleDefinition)
                    ]
                )

            for module_imported_item in module.get_import_items():
                module_cdata.add_include(
                    str(
                        cgen.Include(
                            cls.get_filename(module_imported_item),
                            system=False,
                        )
                    )
                )

            # Definitions

            simple_definition_list: List[SimpleDefinition] = [
                d
                for d in module.get_definitions()
                if isinstance(d, SimpleDefinition)
            ]
            simple_definition_list.extend(simple_definition_list_imported)

            for definition in ModuleSorter.get_definitions_sorted_by_dependency(
                module
            ):
                if isinstance(definition, SimpleDefinition):
                    if definition.get_type_name() not in ["Float", "Double"]:
                        # is used directly where needed
                        module_cdata.add_include(
                            f"\n// NOTE: {definition.get_type_name()} is "
                            "embedded directly where it is used. Rationale: "
                            "Bitfields cannot be typedef'd."
                        )
                elif isinstance(definition, Sequence):
                    sequence_cdata = cls._convert_sequence_to_c(
                        simple_definition_list, definition, module
                    )
                    module_cdata.extend_with_cdata(sequence_cdata)
                elif isinstance(definition, Enumerated):
                    enum_cdata = cls._convert_enumerated_to_c(definition)
                    module_cdata.extend_with_cdata(enum_cdata)
                elif isinstance(definition, Choice):
                    choice_cdata = cls._convert_choice_to_c(definition)
                    module_cdata.extend_with_cdata(choice_cdata)
                else:
                    raise NotImplementedError(
                        f"binary code generation for '{definition}' not yet "
                        + "implemented."
                    )

            comment = module.get_comment()
            file_documentation = comment and comment.get_comment()
            if file_documentation:
                module_cdata.set_header_comment(file_documentation)

            filename = cls.get_filename(module)
            CPrinter.print_to_file(
                cdata=module_cdata,
                filename=filename,
                output_folder=output_folder,
                header_type=HeaderType.STORED_DATA_BINARY,
            )

    # Override
    @classmethod
    def _with_components_handling(
        cls,
        definition_type_name_c: str,
        seq_item: KeyTypePair,
        module: Optional[Asn1Module],
    ) -> CData:
        if not module:
            raise AttributeError("This method needs the 'module' attribute.")

        cdata: CData = CData.create_empty()
        bin_data_list: List[bytes] = []

        # get sequences with their defined keys and types
        definitions: Dict[str, Dict[str, SequenceSpecificationContainer]] = {}
        for definition in module.get_definitions():
            # only sequences can have WITH COMPONENTS
            # ignore other ASN.1 definitions
            if isinstance(definition, Sequence):
                seq_specifications: Dict[
                    str, SequenceSpecificationContainer
                ] = {}
                for sequence in definition.get_children():
                    if sequence.get_with_components() is None:
                        seq_specifications[
                            sequence.get_key()
                        ] = SequenceSpecificationContainer(
                            # None if a WITH COMPONENTS otherwise TypeEnum
                            c_type=sequence.get_asn_type().get_c_type(),
                            # needed for correct (u)int assignement
                            bitsize=sequence.get_size_bits(),
                            # ASN.1 type, either simple definition or own
                            # definition (Sequence, Choice, ...)
                            seq_type=sequence.get_asn_type().get_type_name(),
                        )
                definitions[definition.get_type_name()] = seq_specifications

        bin_data_list.extend(cls._values_to_bytes_list(seq_item, definitions))

        cdata.add_binary_init(
            lowerize(definition_type_name_c),
            bin_data_list,
        )
        return cdata

    @classmethod
    def _values_to_bytes_list(
        cls,
        key_type_pair: KeyTypePair,
        definitions: Dict[str, Dict[str, SequenceSpecificationContainer]],
    ) -> List[bytes]:
        bin_data_list: List[bytes] = []

        with_component: WithComponents = key_type_pair.get_with_components()
        asn_type: Asn1Type = key_type_pair.get_asn_type()
        if asn_type is None:
            raise NotImplementedError(
                "asn_type is None. Should never be reached."
            )
        asn_type_name: str = asn_type.get_type_name()

        for component in with_component.get_components():
            bin_data = cls._component_to_bytes(
                component,
                asn_type_name,
                definitions,
            )
            bin_data_list.extend(bin_data)

        return bin_data_list

    @classmethod
    def _component_to_bytes(  # pylint: disable=too-many-arguments
        cls,
        component: ComponentsItem,
        asn_type_name: str,
        definitions: Dict[str, Dict[str, SequenceSpecificationContainer]],
    ) -> List[bytes]:
        bin_data_list: List[bytes] = []
        value = component.get_value()

        definition_by_type_name: Dict[
            str, SequenceSpecificationContainer
        ] = definitions[asn_type_name]

        key: SequenceSpecificationContainer = definition_by_type_name[
            component.get_key()
        ]

        if isinstance(value, WithComponents):
            inner_asn_type_name: str = key.get_seq_type()
            for inner_component in value.get_components():
                bin_data = cls._component_to_bytes(
                    inner_component,
                    inner_asn_type_name,
                    definitions,
                )
                bin_data_list.extend(bin_data)
        else:
            c_type: Optional[TypeEnum] = key.get_c_type()
            if c_type is None:
                raise NotImplementedError(
                    f"c_type is None for {component.get_key()}. "
                    "Should never be reached, because the value should only be "
                    "None if it is a WithComponents. This case is handled "
                    "separately."
                )

            byte_size: int = bit_to_bytes(key.get_bitsize())

            # TODO: implement boolean handling
            if c_type is TypeEnum.A_BOOL:
                raise NotImplementedError("TODO: implement handling of boolean")

            # TODO: implement string handling
            if c_type is TypeEnum.A_STRING:
                raise NotImplementedError(
                    "TODO: implement handling of strings and chars"
                )

            # TODO: implement array handling

            bin_format_c_type: Dict[int, str] = cls.FORMAT[c_type]
            bin_format: str = bin_format_c_type[byte_size]
            endianness: str = cls.ENDIANNESS[cls.endianness]

            bin_data_list.append(
                struct.pack(f"{endianness}{bin_format}", value)
            )

        return bin_data_list
